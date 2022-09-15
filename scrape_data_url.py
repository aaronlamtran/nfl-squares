from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from dotenv import load_dotenv
import os
import app
load_dotenv()
CHROME_DRIVER_PATH = os.getenv('CHROME_DRIVER_PATH') + "/chromedriver"

with open('test.html', 'r', encoding='utf-8') as f:
    html_string = f.read()

# print(html_string)
chrome_options = Options()
# chrome_options.headless = True
service = Service(executable_path=CHROME_DRIVER_PATH)
driver = webdriver.Chrome(options=chrome_options, service=service)
driver.implicitly_wait(50)
url = 'http://127.0.0.1:5500/live-2nd-q.html'
# url = 'https://www.espn.com/nfl/scoreboard/_/week/1/year/2021/seasontype/2' #OT
# url = 'https://www.espn.com/nfl/scoreboard/_/week/1/year/2022/seasontype/2'
driver.get(url)

# driver.get("data:text/html;charset=utf-8," + html_string)
# driver.execute_script("$(document.body).trigger('load');")
result = driver.find_element(
    By.XPATH, """//*[@id="fittPageContainer"]/div[3]/div/div/div[1]/section/div/div/h1""")
boxes = driver.find_elements(By.CLASS_NAME, "Card.gameModules")

for box in boxes:
    date = box.find_element(
        By.CLASS_NAME, 'Card__Header__Title.Card__Header__Title--no-theme')
    matches = box.find_elements(By.CLASS_NAME, 'Scoreboard__Column.flex-auto.Scoreboard__Column--1.Scoreboard__Column--Score')
    for match in matches:
        scoreboard_score_cell = match.find_elements(By.CLASS_NAME, """ScoreboardScoreCell__Overview.flex.pb3.w-100""")
        competitors = match.find_elements(By.TAG_NAME, 'li')

        current_match = []
        for competitor in competitors:
            current_match.append(competitor.text.split('\n')[0])
        print('current match', current_match)
        try:
            print('scoreboard_score_cell.text', scoreboard_score_cell.text)
        except:
            pass
        try:
            for each in scoreboard_score_cell:
                time = each.text.split(' ')[0]
                quarter = each.text.split(' ')[2].split('\n')[0]
                print('time: ', time, 'quarter: ', quarter)
        except:
            pass

        is_game_live = time is not None and quarter is not None
        if is_game_live:
            for competitor in competitors:
                print('competitor: ',competitor.text.split('\n')[0] , '\n')
                team_scores_all_quarters = competitor.find_elements(By.CLASS_NAME, 'ScoreboardScoreCell_Linescores.football.flex.justify-end')
                quarters = competitor.find_elements(By.CLASS_NAME, 'ScoreboardScoreCell__Value.flex.justify-center.pl2.football')

                print('line 64', time, quarter)
                print('quarters length:', len(quarters))
                for each_score_B in quarters:
                    print('each_score_B',each_score_B.text)
            time = None
            quarter = None
        else:
            pass
print(result.text)
driver.quit()

# driver.executeScript("$(document.body).trigger('load');")
