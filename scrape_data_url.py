import ast
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from dotenv import load_dotenv
from re import search
import os
import time
import app
load_dotenv()
CHROME_DRIVER_PATH = os.getenv('CHROME_DRIVER_PATH') + "/chromedriver"


line_break = '\n'

def construct_header(quarter, time_left_in_q):
    header = 'Q1|Q2|Q3|Q4|F/OT'
    is_game_ended = search("FINAL", time_left_in_q)
    if is_game_ended:
        quarter_for_header = quarter
    else:
        quarter_for_header = quarter + '-' + time_left_in_q
    quarter_for_header = quarter_for_header.ljust(20, '-')
    header = quarter_for_header + header + line_break
    return header

def construct_row(quarter, competitor, scores):
    # tack on placeholder 0's for no OT
    delimiter = '|'
    no_ot = len(scores) == 12
    no_ot_placeholder = '--'
    quarter_yet_to_happen_ph = '--'
    if no_ot:
        scores = scores + no_ot_placeholder + delimiter
    # add competitor to row
    competitor = competitor.ljust(20, '-') + scores
    # Raiders-------------00|10|00|17|00
    # calc total scores and add to row
    if scores[12:14] != no_ot_placeholder:
        ot=int(scores[12:14])
    else:
        ot=0
    if quarter == '1st':
        q1=int(scores[:2])
        q2='--'
        q3='--'
        q4='--'
        pos1 = str(q1).rjust(2, '0')
        pos2 = '--'
        pos3 = '--'
        pos4 = '--'
        pos5 = '--'
    if quarter == '2nd' or quarter == 'Halftime' or quarter == '2':
        q1=int(scores[:2])
        q2=int(scores[3:5])
        q3='--'
        q4='--'
        pos1 = str(q1).rjust(2, '0')
        pos2 = str(q1 + q2).rjust(2, '0')
        pos3 = '--'
        pos4 = '--'
        pos5 = '--'
    if quarter == '3rd':
        q1=int(scores[:2])
        q2=int(scores[3:5])
        q3=int(scores[6:8])
        q4='--'
        pos1 = str(q1).rjust(2, '0')
        pos2 = str(q1 + q2).rjust(2, '0')
        pos3 = str(q1 + q2 + q3).rjust(2, '0')
        pos4 = '--'
        pos5 = '--'
    if quarter == '4th':
        q1=int(scores[:2])
        q2=int(scores[3:5])
        q3=int(scores[6:8])
        q4=int(scores[9:11])
        pos1 = str(q1).rjust(2, '0')
        pos2 = str(q1 + q2).rjust(2, '0')
        pos3 = str(q1 + q2 + q3).rjust(2, '0')
        pos4 = str(q1 + q2 + q3 + q4).rjust(2, '0')
        pos5 = '--'

    if quarter == 'FINAL' or quarter == 'FINAL/OT':
        q1=int(scores[:2])
        q2=int(scores[3:5])
        q3=int(scores[6:8])
        q4=int(scores[9:11])
        pos1 = str(q1).rjust(2, '0')
        pos2 = str(q1 + q2).rjust(2, '0')
        pos3 = str(q1 + q2 + q3).rjust(2, '0')
        pos4 = str(q1 + q2 + q3 + q4).rjust(2, '0')
        pos5 = str(q1 + q2 + q3 + q4 + ot).rjust(2, '0')


    # pos1 = str(q1).rjust(2, '0')
    # pos2 = str(q1 + q2).rjust(2, '0')
    # pos3 = str(q1 + q2 + q3).rjust(2, '0')
    # pos4 = str(q1 + q2 + q3 + q4).rjust(2, '0')
    # pos5 = str(q1 + q2 + q3 + q4 + ot).rjust(2, '0')

    if quarter == '1st':
        quarter_scores = pos1 + delimiter + quarter_yet_to_happen_ph + delimiter + quarter_yet_to_happen_ph + delimiter + quarter_yet_to_happen_ph + delimiter + quarter_yet_to_happen_ph + delimiter
    if quarter == '2nd':
        quarter_scores = pos1 + delimiter + pos2 + delimiter + quarter_yet_to_happen_ph + delimiter + quarter_yet_to_happen_ph + delimiter + quarter_yet_to_happen_ph + delimiter
    if quarter == 'Halftime' or quarter == '2':
        quarter_scores = pos1 + delimiter + pos2 + delimiter + pos3 + delimiter + quarter_yet_to_happen_ph + delimiter + quarter_yet_to_happen_ph + delimiter
    if quarter == '3rd':
        quarter_scores = pos1 + delimiter + pos2 + delimiter + pos3 + delimiter + quarter_yet_to_happen_ph + delimiter + quarter_yet_to_happen_ph + delimiter
    if quarter == '4th':
        quarter_scores = pos1 + delimiter + pos2 + delimiter + pos3 + delimiter + pos4 + delimiter + quarter_yet_to_happen_ph + delimiter
    if quarter == 'FINAL' or quarter == 'FINAL/OT':
        quarter_scores = pos1 + delimiter + pos2 + delimiter + pos3 + delimiter + pos4 + delimiter + pos5 + delimiter
    quarter_scores = "-" * 20 +  quarter_scores

    # print('header', header)
    # print('competitor', competitor)
    # print('quarter_scores', quarter_scores)
    # line_break = '\n'
    # header + line_break +
    line = competitor + line_break + quarter_scores + line_break
    return line
# construct_row('FINAL', 'Raiders', '05|05|05|05|05')
# print('sleeping')
# time.sleep(50)
def app():
    print('working...')
    chrome_options = Options()
    chrome_options.headless = True
    service = Service(executable_path=CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(options=chrome_options, service=service)
    driver.implicitly_wait(50)
    url = 'http://127.0.0.1:5500/live-2nd-q.html'
    # url = 'https://www.espn.com/nfl/scoreboard/_/week/1/year/2021/seasontype/2' #OT
    # url = 'https://www.espn.com/nfl/scoreboard/_/week/1/year/2022/seasontype/2'
    # url = 'https://www.espn.com/nfl/scoreboard/_/week/2/year/2022/seasontype/2' #Live
    # handle canceled games
    driver.get(url)
    driver.execute_cdp_cmd('Emulation.setScriptExecutionDisabled', {'value': True})
    #driver.execute_script("window.stop();");


    def get_current_quarter(scoreline):
        if scoreline.split(' ')[0] == "FINAL" or scoreline.split(' ')[0] == "FINAL/OT":
            return scoreline.split(' ')[0]
        return scoreline.split(' ')[2]

    with open('live_scores.txt', 'w') as f:
        f.write('hello')
        boxes = driver.find_elements(By.CLASS_NAME, "Card.gameModules")
        for box in boxes:
            date = box.find_element(
                By.CLASS_NAME, 'Card__Header__Title.Card__Header__Title--no-theme').text.center(40) + line_break
            matches = box.find_elements(By.CLASS_NAME, 'Scoreboard__Column.flex-auto.Scoreboard__Column--1.Scoreboard__Column--Score')
            for match in matches:
                competitors = match.find_elements(By.TAG_NAME, 'li')
                print("*".ljust(40, '*'))

                current_match = []
                for competitor in competitors:
                    current_match.append(competitor.text.split('\n')[0])
                team_at_team_string = current_match[0] + ' @ ' + current_match[1]

                print(team_at_team_string.center(41))
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
                time_stamp = scoreboard_score_cell[0].text.replace('\n', ' ').split(' ')[0]
                # print(time_stamp)
                # print('scoreline', scoreline) # keep scoreline 9:31 - 2nd 1 2 3 4 T
                if search("1st", scoreline) or search("2nd", scoreline) or search("3rd", scoreline) or search("4th", scoreline) or search("OT", scoreline) or search("Halftime", scoreline):
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

                    with open('live_scores.txt', 'a') as f:
                        asterisks = "*" * 40 + line_break
                        team_line = team_at_team_string.center(40) + line_break
                        header = construct_header(current_quarter, time_stamp)
                        f.write(asterisks)
                        f.write(team_line)
                        f.write(date)
                        f.write(header)

                    with open('live_scores.txt', 'a') as f:
                        data_row = ''
                        for competitor in competitors:
                            current_competitor = competitor.text.split('\n')[0]
                            quarters = competitor.find_elements(By.CLASS_NAME, 'ScoreboardScoreCell__Value.flex.justify-center.pl2.football')

                            row_scores = ''
                            for each_score_B in quarters: # will iterate at least 4 times
                                delimiter = '|'
                                quarter_score = each_score_B.text
                                if len(quarter_score) == 1:
                                    quarter_score = "0" + quarter_score + delimiter
                                if len(quarter_score) == 2:
                                    quarter_score = quarter_score + delimiter
                                if quarter_score == '':
                                    quarter_score = "--" + delimiter
                                row_scores += quarter_score

                            data_row +=  construct_row(current_quarter, current_competitor, row_scores)
                        print(data_row)
                        f.write(data_row)

                elif match_not_started:
                    match_not_started_str = 'has not started'.center(40) + line_break
                    asterisks = "*" * 40 + line_break
                    team_line = team_at_team_string.center(40) + line_break
                    starting_at_time = scoreline.center(40) + line_break
                    with open('live_scores.txt', 'a') as f:
                        f.write(asterisks)
                        f.write(team_line)
                        f.write(date)
                        # f.write(match_not_started_str)
                        f.write(starting_at_time)
                    # print(match_not_started_str)
                    print(date)
                    print(starting_at_time)
                    pass
    driver.quit()



    # driver.executeScript("$(document.body).trigger('load');")
if __name__ == '__main__':
    while True:
        app()
        interval = 60
        print(f'sleeping for {interval}s..')
        time.sleep(interval)