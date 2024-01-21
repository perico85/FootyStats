from logging import exception
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup, element
import re
import pandas as pd
import os
import time
import csv
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, wait
import random
import pyodbc
import collections

def database_insert(query):
    conn_params = 'driver={SQL Server};server=TS-SOFTWARE7\SQLEXPRESS;database=FootyStats;uid=sa;pwd=TrekScale2094'
    #conn_params = 'driver={SQL Server};server=DESKTOP-4G5NRUL\SQLEXPRESS;database=FootyStats;uid=IMDev;pwd=IMDev'
    try:
        conn = pyodbc.connect(conn_params)
    except pyodbc.Error as e:
        print(str(e))
    else:
        db = conn.cursor()
        db.execute(query).commit()       
    finally:
        if conn:
            conn.close()

def database_delete(query):
    conn_params = 'driver={SQL Server};server=TS-SOFTWARE7\SQLEXPRESS;database=FootyStats;uid=sa;pwd=TrekScale2094'
    #conn_params = 'driver={SQL Server};server=DESKTOP-4G5NRUL\SQLEXPRESS;database=FootyStats;uid=IMDev;pwd=IMDev'
    try:
        conn = pyodbc.connect(conn_params)
    except pyodbc.Error as e:
        print(str(e))
    else:
        db = conn.cursor()
        db.execute(query).commit()
    finally:
        if conn:
            conn.close()

SQL_DELETE_QUERY_H2H = "DELETE FROM FootyStats_League_Fixtures"
database_delete(SQL_DELETE_QUERY_H2H)

USERNAME = 'aumbreymsane' # Your username
PASSWORD = 'Majoka2010@' # Your password

collections.Callable = collections.abc.Callable
driver = webdriver.Edge("C:\\Scraping drivers\msedgedriver.exe")  

driver.get('https://footystats.org/login')

headers = ["League Fixtures"]
time.sleep(5) # Let the user actually see something!


search_box = driver.find_element_by_name('username')
search_box.send_keys(USERNAME)
search_box = driver.find_element_by_name('password')

search_box.send_keys(PASSWORD)

driver.find_element_by_id('register_account').submit()

time.sleep(5) # Let the user actually see something!

j = 0
driver.maximize_window()

elem = driver.switch_to.active_element
buttons = []
button_cri = driver.find_elements(By.XPATH, '(//a[@class="white dropDownMenu linkBtn dBlock icon-wrapper pr slide-menu-toggle"])')
element = driver.find_element(By.XPATH, '(//a[@class="white dropDownMenu linkBtn dBlock icon-wrapper pr slide-menu-toggle"])')
actions = ActionChains(driver)
actions.move_to_element(element)
actions.perform()
button_200 = driver.find_element_by_partial_link_text("Leagues").click()

league = []

driver.implicitly_wait(2)
time.sleep(2)
soup = BeautifulSoup(driver.page_source, 'lxml')
league_teams =  soup.find_all('div', attrs={'class':'team'})
for l in league_teams[1:]:
    href = l.find('a')
    league.append(href.get('href'))

stringss = []

end = '/zimbabwe/premier-soccer-league'
count = 0
for i in league:
    if i != end:
        url = 'https://footystats.org' + i +"/fixtures"
        driver.get(url)
        waitTime = random.randrange(1,5)
        time.sleep(waitTime)
        count = count + 1
        soup = BeautifulSoup(driver.page_source, 'lxml')
        progress = [k.get_text() for k in soup.find_all('div', attrs={'class':'detail lh03e progress-text-double-line-fix'})]
        gdp = soup.find_all('div', attrs={'class':'full-matches-table mt1e '})
        print("Number of tables: ", len(gdp))
        try:
            if len(gdp)>0:
                for j in gdp[0]:
                    home_team = []
                    away_team = []
                    dates = [k.get_text() for k in j.find_all('td', attrs={'class':'date'})] 
                    
                    home = [k.get_text(",") for k in j.find_all('td', attrs={'class':'team-home'})]
                    for k in range(len(home) - 1):
                        try:
                            home_team_pos = home[k+1].index(",")
                            home_team.append(home[k+1][0:home_team_pos])
                        except:
                            home_team.append(home[k+1])

                    away = [k.get_text(",") for k in j.find_all('td', attrs={'class':'team-away'})] 
                    for k in range(len(away) - 1):
                        try:
                            away_team_pos = away[k+1].index(",")
                            away_team.append(away[k+1][0:away_team_pos])
                        except:
                            away_team.append(away[k+1])

                for p in range(len(home_team)):
                    try:
                        SQL_INSERT_BTTS_ROW = "INSERT INTO FootyStats_League_Fixtures (Dates, Home, Away, Country_League, League_Progress) VALUES ('" + dates[p + 1][:15] + "','" + str(home_team[p]).replace("'", "") + "','" + str(away_team[p]).replace("'", "") + "','" + str(i).replace("'", "") + "','" + str(progress[0]).replace("'", "") + "')"
                        database_insert(SQL_INSERT_BTTS_ROW)
                    except Exception as e:
                        print(e)
        except:
            next

#detailed stats
table_names = ["Form Table", "Form Last 5", "Form Home", "Form Away"]

end = '/zimbabwe/premier-soccer-league'

SQL_DELETE_FORM = "DELETE FROM FootyStats_League_Detail_Stats"
database_delete(SQL_DELETE_FORM)

for i in league:
    if i != end:
        url = 'https://footystats.org' + i +"/form-table"
        driver.get(url)
        waitTime = random.randrange(1,5)
        time.sleep(waitTime)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        gdp = soup.find_all('table', attrs={'class':'full-league-table'})
        print("Number of tables: ", len(gdp))
        for j in range(len(gdp)):

            home_team = []

            team = [k.get_text(",") for k in gdp[j].find_all('td', attrs={'class':'team'})]
            for k in range(len(team) - 1):
                        try:
                            home_team_pos = team[k+1].index(",")
                            home_team.append(team[k+1][0:home_team_pos])
                        except:
                            home_team.append(team[k+1])

            values1 = [k.get_text(" ") for k in soup.find_all('td', attrs={'data-mobify-page':'1'})]
            values2 = [k.get_text(" ") for k in soup.find_all('td', attrs={'data-mobify-page':'2'})]
            values3 = [k.get_text(" ") for k in soup.find_all('td', attrs={'data-mobify-page':'3'})]
            
            index = 0
            index2 = 0
            index3 = 0

            for k in range(len(home_team)):
                if j == 0:
                    SQL_INSERT_FORM = "INSERT INTO FootyStats_League_Detail_Stats (Team, MP, Win, Draw, Loss, GF, GA, GD, PTS, Last_6, PPG, CS, FTS, BTTS, Over_2_5, Next_Match, Table_Name, Country_League) VALUES ('" + str(home_team[k]).replace("'", "") + "','" + str(values1[index]).replace("'", "") + "','" + str(values1[index+1]).replace("'", "") + "','" + str(values1[index+2]).replace("'", "") + "','" + str(values1[index+3]).replace("'", "") + "','" + str(values1[index+4]).replace("'", "") + "','" + str(values1[index+5]).replace("'", "") + "','" + str(values1[index+6]).replace("'", "") + "','" + str(values1[index+7]).replace("'", "") + "','" + str(values2[index2]).replace("'", "") + "','" + str(values2[index2+1]).replace("'", "") + "','" + str(values2[index2+2]).replace("'", "") + "','" + str(values2[index2+3]).replace("'", "") + "','" + str(values3[index3]).replace("'", "") + "','" + str(values3[index3+1]).replace("'", "") + "','" + str(values3[index3+2]).replace("'", "") + "','" + table_names[j] + "','" + str(i).replace("'", " ") + "')" 
                else:
                    SQL_INSERT_FORM = "INSERT INTO FootyStats_League_Detail_Stats (Team, MP, Win, Draw, Loss, GF, GA, GD, PTS, Last_6, PPG, CS, FTS, BTTS, Over_2_5, Next_Match, Table_Name, Country_League) VALUES ('" + str(home_team[k]).replace("'", "") + "','" + str(values1[index]).replace("'", "") + "','" + str(values1[index+1]).replace("'", "") + "','" + str(values1[index+2]).replace("'", "") + "','" + str(values1[index+3]).replace("'", "") + "','" + str(values1[index+4]).replace("'", "") + "','" + str(values1[index+5]).replace("'", "") + "','" + str(values1[index+6]).replace("'", "") + "','" + " " + "','" + str(values2[index2]).replace("'", "") + "','" + str(values2[index2+1]).replace("'", "") + "','" + str(values2[index2+2]).replace("'", "") + "','" + str(values2[index2+3]).replace("'", "") + "','" + str(values3[index3]).replace("'", "") + "','" + str(values3[index3+1]).replace("'", "") + "','" + str(values3[index3+2]).replace("'", "") + "','" + table_names[j] + "','" + str(i).replace("'", " ") + "')"
                
                database_insert(SQL_INSERT_FORM)
                index = index + 8
                index2 = index2 + 4
                index3 =  index3 + 4

#League 1st Half

table_names = ["Half Time Table", "Home Half Time Table", "Away Half Time Table"]

end = '/zimbabwe/premier-soccer-league'

SQL_DELETE_FORM = "DELETE FROM FootyStats_1st_Half_League_Table_Detail_Stats"
database_delete(SQL_DELETE_FORM)

for i in league:
    if i != end:
        url = 'https://footystats.org' + i +"/half-time-table"
        driver.get(url)
        waitTime = random.randrange(1,5)
        time.sleep(waitTime)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        gdp = soup.find_all('table', attrs={'class':'full-league-table'})
        print("Number of tables: ", len(gdp))
        for j in range(len(gdp)):

            home_team = []

            team = [k.get_text(",") for k in gdp[j].find_all('td', attrs={'class':'team'})]
            for k in range(len(team) - 1):
                        try:
                            home_team_pos = team[k+1].index(",")
                            home_team.append(team[k+1][0:home_team_pos])
                        except:
                            home_team.append(team[k+1])

            values1 = [k.get_text(" ") for k in soup.find_all('td', attrs={'data-mobify-page':'1'})]
            values2 = [k.get_text(" ") for k in soup.find_all('td', attrs={'data-mobify-page':'2'})]
            values3 = [k.get_text(" ") for k in soup.find_all('td', attrs={'data-mobify-page':'3'})]
            
            index = 0
            index2 = 0
            index3 = 0

            for k in range(len(home_team)):
                SQL_INSERT_FORM = "INSERT INTO FootyStats_1st_Half_League_Table_Detail_Stats (Team, MP, WDL, GF, GA, GD, PTS, Last_5, PPG, CS, BTTS, FTS, Plus_0_5, Plus_1_5, Plus_2_5, AVG, Table_Name, Country_League) VALUES ('" + str(home_team[k]).replace("'", "") + "','" + str(values1[index]).replace("'", "") + "','" + str(values1[index+1]).replace("'", "") + "','" + str(values1[index+2]).replace("'", "") + "','" + str(values1[index+3]).replace("'", "") + "','" + str(values1[index+4]).replace("'", "") + "','" + str(values1[index+5]).replace("'", "") + "','" + str(values2[index2]).replace("'", "") + "','" + str(values2[index2+1]).replace("'", "") + "','" + str(values2[index2+2]).replace("'", "") + "','" + str(values3[index3]).replace("'", "") + "','" + str(values3[index3+1]).replace("'", "") + "','" + str(values3[index3+2]).replace("'", "") + "','" + str(values3[index3+3]).replace("'", "") + "','" + str(values3[index3+4]).replace("'", "") + "','" + str(values3[index3+5]).replace("'", "") + "','" + table_names[j] + "','" + str(i).replace("'", " ") + "')" 
                database_insert(SQL_INSERT_FORM)
                index = index + 6
                index2 = index2 + 3
                index3 =  index3 + 6

#League 2nd Half

table_names = ["2nd Half Table", "Home 2nd Half Table", "Away 2nd Half Table"]

end = '/zimbabwe/premier-soccer-league'

SQL_DELETE_FORM = "DELETE FROM FootyStats_2nd_Half_League_Table_Detail_Stats"
database_delete(SQL_DELETE_FORM)

team_refs = []

for i in league:
    if i != end:
        url = 'https://footystats.org' + i +"/2nd-half-table"
        driver.get(url)
        waitTime = random.randrange(1,5)
        time.sleep(waitTime)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        gdp = soup.find_all('table', attrs={'class':'full-league-table'})
        print("Number of tables: ", len(gdp))
        for j in range(len(gdp)):

            team_links =  soup.find_all('td', attrs={'class':'team'})
            for l in team_links:
                a = l.find('a')
                href = a.get('href')
                if href not in team_refs:
                    team_refs.append(href)

            home_team = []

            team = [k.get_text(",") for k in gdp[j].find_all('td', attrs={'class':'team'})]
            for k in range(len(team) - 1):
                        try:
                            home_team_pos = team[k+1].index(",")
                            home_team.append(team[k+1][0:home_team_pos])
                        except:
                            home_team.append(team[k+1])

            values1 = [k.get_text(" ") for k in soup.find_all('td', attrs={'data-mobify-page':'1'})]
            values2 = [k.get_text(" ") for k in soup.find_all('td', attrs={'data-mobify-page':'2'})]
            values3 = [k.get_text(" ") for k in soup.find_all('td', attrs={'data-mobify-page':'3'})]
            
            index = 0
            index2 = 0
            index3 = 0

            for k in range(len(home_team)):
                SQL_INSERT_FORM = "INSERT INTO FootyStats_2nd_Half_League_Table_Detail_Stats (Team, MP, WDL, GF, GA, GD, PTS, Last_5, PPG, CS, BTTS, FTS, Plus_0_5, Plus_1_5, Plus_2_5, AVG, Table_Name, Country_League) VALUES ('" + str(home_team[k]).replace("'", "") + "','" + str(values1[index]).replace("'", "") + "','" + str(values1[index+1]).replace("'", "") + "','" + str(values1[index+2]).replace("'", "") + "','" + str(values1[index+3]).replace("'", "") + "','" + str(values1[index+4]).replace("'", "") + "','" + str(values1[index+5]).replace("'", "") + "','" + str(values2[index2]).replace("'", "") + "','" + str(values2[index2+1]).replace("'", "") + "','" + str(values2[index2+2]).replace("'", "") + "','" + str(values3[index3]).replace("'", "") + "','" + str(values3[index3+1]).replace("'", "") + "','" + str(values3[index3+2]).replace("'", "") + "','" + str(values3[index3+3]).replace("'", "") + "','" + str(values3[index3+4]).replace("'", "") + "','" + str(values3[index3+5]).replace("'", "") + "','" + table_names[j] + "','" + str(i).replace("'", " ") + "')" 
                database_insert(SQL_INSERT_FORM)
                index = index + 6
                index2 = index2 + 3
                index3 =  index3 + 6

#League Teams Detail Stats overall

table_names = ["2nd Half Table", "Home 2nd Half Table", "Away 2nd Half Table"]

end = '/zimbabwe/premier-soccer-league'

SQL_DELETE_FORM = "DELETE FROM FootyStats_Team_Detail_Stats"
database_delete(SQL_DELETE_FORM)

for i in team_refs:
    if i != end:
        url = 'https://footystats.org' + i 
        driver.get(url)
        waitTime = random.randrange(1,5)
        time.sleep(waitTime)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        country_league = soup.find('div', attrs={'class':'bbox dropdown fl'}).get_text()
        gdp = soup.find('table', attrs={'class':'miniTableNeo'})
        print("Number of tables: ", len(gdp))
        for j in range(len(gdp)):
            home_team = []

            team = [k.get_text(" ") for k in gdp.find_all('td', attrs={'class':'leagueTableTeamName al'})]
            values = [k.get_text(" ") for k in gdp.find_all('p', attrs={'class':'mild-small'})]
            
            index = 0

            for k in range(len(team)):
                SQL_INSERT_FORM = "INSERT INTO FootyStats_Team_Detail_Stats (Team, MP, Win, GF, GA, GD, PTS, AVG, Country_League) VALUES ('" + str(team[k]).replace("'", "") + "','" + str(values[index+1]).replace("'", "") + "','" + str(values[index+2]).replace("'", "") + "','" + str(values[index+3]).replace("'", "") + "','" + str(values[index+4]).replace("'", "") + "','" + str(values[index+5]).replace("'", "") + "','" + str(values[index+6]).replace("'", "") + "','" + str(values[index+7]).replace("'", "") + "', '" + str(country_league).replace("'", "") + "')" 
                database_insert(SQL_INSERT_FORM)
                index = index + 8

#League Teams Over Under Goal Stats
SQL_DELETE_FORM = "DELETE FROM FootyStasts_Team_Over_Under_Goals_Stats"
database_delete(SQL_DELETE_FORM)

for i in team_refs:
    if i != end:
        url = 'https://footystats.org' + i 
        driver.get(url)
        waitTime = random.randrange(1,5)
        time.sleep(waitTime)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        team = [k.get_text(" ") for k in soup.find('h1', attrs={'class':'row white heroh1'})]
        country_league = soup.find('div', attrs={'class':'bbox dropdown fl'}).get_text()
        gdp = soup.find('div', attrs={'class':'w96 cf m0Auto rmt15e'})
        print("Number of tables: ", len(gdp))
            
        values = [k.get_text(" ") for k in gdp.find_all('td', attrs={'class':'item'})]
        avg = values[1] + "," + values[2] + "," + values[3]
        team = team[1]
        Over_0_5 = values[5] + "," + values[6] + "," + values[7]
        Over_1_5 = values[9] + "," + values[10] + "," + values[11]
        Over_2_5 = values[13] + "," + values[14] + "," + values[15]
        Over_3_5 = values[17] + "," + values[18] + "," + values[19]
        Over_4_5 = values[21] + "," + values[22] + "," + values[23]
        Over_5_5 = values[25] + "," + values[26] + "," + values[27]
        Under_0_5 = values[29] + "," + values[30] + "," + values[31]
        Under_1_5 = values[33] + "," + values[34] + "," + values[35]
        Under_2_5 = values[37] + "," + values[38] + "," + values[39]
        Under_3_5 = values[41] + "," + values[42] + "," + values[43]
        Under_4_5 = values[45] + "," + values[46] + "," + values[47]
        Under_5_5 = values[49] + "," + values[50] + "," + values[51]

        SQL_INSERT_FORM = "INSERT INTO FootyStasts_Team_Over_Under_Goals_Stats (Team, Country_League, AVG, Over_0_5, Over_1_5, Over_2_5, Over_3_5, Over_4_5, Over_5_5, Under_0_5, Under_1_5, Under_2_5, Under_3_5, Under_4_5, Under_5_5) VALUES ('" + str(team).replace("'", "") + "','" + str(country_league).replace("'","") +  "','" +str(avg).replace("'", "") + "','" + str(Over_0_5).replace("'", "") + "','" + str(Over_1_5).replace("'", "") + "','" + str(Over_2_5).replace("'", "") + "','" + str(Over_3_5).replace("'", "") + "','" + str(Over_4_5).replace("'", "") + "','" + str(Over_5_5).replace("'", "") + "','" + str(Under_0_5).replace("'", "") + "','" + str(Under_1_5).replace("'", "") + "','" + str(Under_2_5).replace("'", "") + "','" + str(Under_3_5).replace("'", "") + "','" + str(Under_4_5).replace("'", "") + "','" + str(Under_5_5).replace("'", "") + "')" 
        database_insert(SQL_INSERT_FORM)

#League Teams Scores and Fixtures Stats
SQL_DELETE_FORM = "DELETE FROM FootyStats_Team_Scores_Fixtures_Stats"
database_delete(SQL_DELETE_FORM)

for i in team_refs:
    if i != end:
        url = 'https://footystats.org' + i 
        driver.get(url)
        waitTime = random.randrange(1,5)
        time.sleep(waitTime)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        try:
            team = [k.get_text(" ") for k in soup.find('h1', attrs={'class':'row white heroh1'})]
            country_league = soup.find('div', attrs={'class':'bbox dropdown fl'}).get_text()
            gdp = soup.find('ul', attrs={'id':'matchHistoryList'})
            print("Number of tables: ", len(gdp))
            
            dates = [k.get_text(" ") for k in gdp.find_all('span', attrs={'class':'monthAndDay'})]    
            home = [k.get_text(" ") for k in gdp.find_all('div', attrs={'class':'homeTeamInfo'})]
            score = [k.get_text(" ") for k in gdp.find_all('div', attrs={'class':'scoreline'})]
            away = [k.get_text(" ") for k in gdp.find_all('div', attrs={'class':'awayTeamInfo'})]
            analytics = [k.get_text(" ") for k in gdp.find_all('div', attrs={'class':'in-play-analytics'})]
            totalGoals = [k.get_text(" ") for k in gdp.find_all('div', attrs={'class':'totalGoals'})]
            team = team[1]

            for k in range(len(home)):
                SQL_INSERT_FORM = "INSERT INTO FootyStats_Team_Scores_Fixtures_Stats (Team, Country_League, Dates, Home, Score, Away, Analytics, Total_Goals) VALUES ('" + str(team).replace("'", "") + "','" + str(country_league).replace("'","") +  "','" +str(dates[k]).replace("'", "") + "','" + str(home[k]).replace("'", "") + "','" + str(score[k]).replace("'", "") + "','" + str(away[k]).replace("'", "") + "','" + str(analytics[k]).replace("'", "") + "','" + str(totalGoals[k]).replace("'","") + "')" 
                database_insert(SQL_INSERT_FORM)
        except Exception as e:
            print(e)
            next

#Team Statistics
SQL_DELETE_FORM = "DELETE FROM FootyStats_Team_Statistics"
database_delete(SQL_DELETE_FORM)

for i in team_refs:
    if i != end:
        url = 'https://footystats.org' + i 
        driver.get(url)
        waitTime = random.randrange(1,5)
        time.sleep(waitTime)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        statistics = []
        try:
            team = [k.get_text(" ") for k in soup.find('h1', attrs={'class':'row white heroh1'})]
            country_league = soup.find('div', attrs={'class':'bbox dropdown fl'}).get_text()
            gdp = soup.find_all('div', attrs={'class':'flex-center bbox club-data-table br4 fww flex'})
            print("Number of tables: ", len(gdp))
            values = [k.get_text(" ") for k in gdp[2].find_all('div', attrs={'class':'club-data-table-row'})]
            team = team[1]
            for j in range(len(values)):
                statistics.append(str(values[j]).split(" "))
                
                if j != 2:
                    SQL_INSERT_FORM = "INSERT INTO FootyStats_Team_Statistics (P_D, Win, Draw, Loss, GF, GA, GD, PPG, Form, Team, Country_League) VALUES ('" + str(statistics[j][2]).replace("'", "") + "','" + str(statistics[j][3]).replace("'","") +  "','" +str(statistics[j][4]).replace("'", "") + "','" + str(statistics[j][5]).replace("'", "") + "','" + str(statistics[j][6]).replace("'", "") + "','" + str(statistics[j][7]).replace("'", "") + "','" + str(statistics[j][8]).replace("'", "") + "','" + str(statistics[j][9]).replace("'","") + "','" + str(statistics[j][0]).replace("'","") + "','" + str(team).replace("'","") + "','" + str(country_league).replace("'","") + "')" 
                    database_insert(SQL_INSERT_FORM)
                else:
                    SQL_INSERT_FORM = "INSERT INTO FootyStats_Team_Statistics (P_D, Win, Draw, Loss, GF, GA, GD, PPG, Form, Team, Country_League) VALUES ('" + str(statistics[j][1]).replace("'", "") + "','" + str(statistics[j][2]).replace("'","") +  "','" +str(statistics[j][3]).replace("'", "") + "','" + str(statistics[j][4]).replace("'", "") + "','" + str(statistics[j][5]).replace("'", "") + "','" + str(statistics[j][6]).replace("'", "") + "','" + str(statistics[j][7]).replace("'", "") + "','" + str(statistics[j][8]).replace("'","") + "','" + str(statistics[j][0]).replace("'","") + "','" + str(team).replace("'","") + "','" + str(country_league).replace("'","") + "')" 
                    database_insert(SQL_INSERT_FORM)
        except Exception as e:
            print(e)
            next

driver.close()
