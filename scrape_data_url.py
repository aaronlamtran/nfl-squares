from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from dotenv import load_dotenv
from re import search
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
driver.execute_cdp_cmd('Emulation.setScriptExecutionDisabled', {'value': True})
#driver.execute_script("window.stop();");

# driver.get("data:text/html;charset=utf-8," + html_string)
# driver.execute_script("$(document.body).trigger('load');")
result = driver.find_element(
    By.XPATH, """//*[@id="fittPageContainer"]/div[3]/div/div/div[1]/section/div/div/h1""")
boxes = driver.find_elements(By.CLASS_NAME, "Card.gameModules")
def get_current_quarter(scoreline):
    if scoreline.split(' ')[0] == "FINAL":
        return scoreline.split(' ')[0]
    return scoreline.split(' ')[2]

for box in boxes:
    date = box.find_element(
        By.CLASS_NAME, 'Card__Header__Title.Card__Header__Title--no-theme')
    matches = box.find_elements(By.CLASS_NAME, 'Scoreboard__Column.flex-auto.Scoreboard__Column--1.Scoreboard__Column--Score')
    for match in matches:
        competitors = match.find_elements(By.TAG_NAME, 'li')

        current_match = []
        for competitor in competitors:
            current_match.append(competitor.text.split('\n')[0])
        print('current match', current_match)
        scoreboard_score_cell = match.find_elements(By.CLASS_NAME, """ScoreboardScoreCell__Overview.flex.pb3.w-100""")
        # if each.text contains a time, it is either ongoing or scheduled and not yet started
        # if each.text has 1st 2nd 3rd 4th or OT in it, it is ongoing
        # if each.text has FINAL in it, it is over
        # try:
        is_match_live = False
        is_match_completed = False
        match_not_started = False
        with open('each-text.txt', "a") as f:
            f.write(scoreboard_score_cell[0].text.replace('\n', ' ') + "\n")
        scoreline = scoreboard_score_cell[0].text.replace('\n', ' ')
        # print('scoreline', scoreline) # keep scoreline 9:31 - 2nd 1 2 3 4 T
        if search("1st", scoreline) or search("2nd", scoreline) or search("3rd", scoreline) or search("4th", scoreline) or search("OT", scoreline):
            is_match_live = True
        if search("FINAL",scoreline):
            is_match_completed = True
        if search("PM", scoreline) or search("AM", scoreline):
            match_not_started=True

        # print('is_match_live', is_match_live) #keep
        # print('is_match_completed', is_match_completed) #keep
        # print('match_not_started', match_not_started) #keep
        if is_match_live or is_match_completed:
            current_quarter = get_current_quarter(scoreline)
            print('current_quarter', current_quarter)
            for competitor in competitors:
                current_competitor = competitor.text.split('\n')[0]
                print('competitor: ',current_competitor)
                team_scores_all_quarters = competitor.find_elements(By.CLASS_NAME, 'ScoreboardScoreCell_Linescores.football.flex.justify-end')
                quarters = competitor.find_elements(By.CLASS_NAME, 'ScoreboardScoreCell__Value.flex.justify-center.pl2.football')

                row_scores = ''
                for each_score_B in quarters: # will iterate at least 4 times
                    # print('each_score_B',each_score_B.text)
                    delimiter = '|'
                    quarter_score = each_score_B.text
                    if len(quarter_score) == 1:
                        quarter_score = "0" + quarter_score + delimiter
                    if len(quarter_score) == 2:
                        quarter_score = quarter_score + delimiter
                    if quarter_score == '':
                        quarter_score = "00" + delimiter
                    row_scores += quarter_score
                    # print("   each_score_B.text == ''", each_score_B.text == '') # keep. TRUE when quarter has not started yet!
                print('row_scores: ', row_scores)
        elif match_not_started:
            print('   match has not started!')
            pass
        print('')
print(result.text)
driver.quit()

# driver.executeScript("$(document.body).trigger('load');")