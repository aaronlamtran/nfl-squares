from dotenv import load_dotenv
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
import os
import time
import logging

logging.basicConfig(level=logging.INFO, filename='app.log', filemode='a',
                    format='[%(levelname)s] : %(asctime)s - %(message)s', datefmt='%d-%m-%Y %H:%M:%S')


load_dotenv()


CHROME_DRIVER_PATH = os.getenv('CHROME_DRIVER_PATH') + "/chromedriver"
SOURCE_ONE = os.getenv('SOURCE_ONE')
SOURCE_TWO = os.getenv('SOURCE_TWO')
BASE = os.getenv('BASE')


class Scrape:
    def __init__(self, season_type='pre', week=1, team_one='raiders', team_two='packers', year=2022, headless=False, single_year=None, mode='all'):
        self.seasons = {
            "1": list(range(1, 5)),
            "2": list(range(1, 19)),
            "3": list(range(1, 6))
        }
        self.pre_reg_post = {
            "1": "preseason",
            "2": "regular",
            "3": "postseason"
        }
        self.boxes = ''
        self.matches = ''
        self.competitors = ''
        self.day_count = 1
        self.year = year
        self.single_year = single_year
        self.week = week
        self.current_week_match_counter = 0
        self.team_one = team_one
        self.team_two = team_two
        self.season_type = season_type
        self.mode = mode
        self.headless = headless
        self.season_type_string = ''
        self.score_file = open("scores.txt", 'a')
        self.init_driver()
        self.main()

    def init_driver(self):
        self.chrome_options = Options()
        self.chrome_options.headless = self.headless
        self.service = Service(executable_path=CHROME_DRIVER_PATH)
        self.driver = webdriver.Chrome(
            options=self.chrome_options, service=self.service)
        self.driver.implicitly_wait(50)

    def get_box(self):
        self.boxes = self.driver.find_elements(
            By.CLASS_NAME, "Card.gameModules")
        self.get_matches()

    def get_matches(self):
        for box in self.boxes:
            date = box.find_element(
                By.CLASS_NAME, 'Card__Header__Title.Card__Header__Title--no-theme')
            print(f'Day {self.day_count}: {date.text}')
            logging.info(f'Day {self.day_count}: {date.text}')

            self.matches = box.find_elements(
                By.CLASS_NAME, 'ScoreboardScoreCell__Competitors')
            self.get_competitors()

    def get_competitors(self):
        for match in self.matches:
            # print(match.text + '\n\n')
            logging.info('new match')
            self.competitors = match.find_elements(By.TAG_NAME, 'li')
            self.current_match = []
            for each_competitor in self.competitors:
                self.current_match.append(each_competitor.text.split('\n')[0])
            print('self.current_match', self.current_match)
            self.current_week_match_counter += 1

            self.season_type_string = self.pre_reg_post[self.season_type]
            path = f'{self.year}/{self.season_type_string}/week{self.week}'

            is_dir_exist = os.path.exists(path)
            if not is_dir_exist:
                os.makedirs(path)
            file_extension = '.csv'
            file_pre_name_counter = str(self.current_week_match_counter)
            if len(file_pre_name_counter) == 1:
                file_pre_name_counter = ''.join(('0', file_pre_name_counter))
            filename = f'{file_pre_name_counter}-{self.current_match[0].lower()}-{self.current_match[1].lower() + file_extension}'
            absolute_path = os.path.join(path, filename)
            logging.info(f'writing to {absolute_path}')

            self.current_match_file = open(absolute_path, 'w')
            self.get_quarter_scores()

        self.day_count += 1

    def get_quarter_scores(self):

        for competitor in self.competitors:
            team = competitor.find_element(
                By.CLASS_NAME, 'ScoreCell__TeamName.ScoreCell__TeamName--shortDisplayName.truncate.db')
            print(team.text)

            self.score_file.write(team.text + ' ')

            self.team_scores_all_quarters = competitor.find_elements(
                By.CLASS_NAME, 'ScoreboardScoreCell_Linescores.football.flex.justify-end')
            self.format_quarter_scores()

    def format_quarter_scores(self):
        row_scores = []
        for quarter_score in self.team_scores_all_quarters:
            text = quarter_score.text.replace("\n", ",")
            text = text.replace("'", '')
            row_scores.append(text)
        row_scores = " ".join(str(x) for x in row_scores)
        logging.info('quarter scores formatted')
        print(row_scores)

        self.score_file.write(row_scores + '\n')
        # logging.info(f'score_file: new row added')
        self.current_match_file.write(row_scores + '\n')
        # logging.info(f'score_file: new row added')

    def process_single_week(self):
        link = f'{BASE}{self.week}/year/{self.single_year}/seasontype/'
        self.driver.get(link)
        self.get_box()
    def reset_week_game_counter(self):
        self.current_week_match_counter = 0

    def process_season(self):
        for season_type, weeks in self.seasons.items():
            logging.info('new season type')
            for week in weeks:
                self.week = week
                self.season_type = season_type
                link = f'{BASE}{self.week}/year/{self.year}/seasontype/{self.season_type}'
                print(link)
                self.driver.get(link)
                self.reset_week_game_counter()
                self.get_box()

    def main(self):
        if self.mode == 'all':
            print('skipping single year processing because mode == all')
            self.process_season()
        else:
            self.process_single_week()


def script():
    start_time = time.time()

    scrape = Scrape(year=2021, week=2)

    end_time = time.time()
    execution_time = str(end_time - start_time)

    print('Execution time in seconds: ' + execution_time)

    time_file = open("time.txt", "a")

    output = f"headless: " + str(scrape.chrome_options.headless) + \
        " - " + execution_time + "\n"

    logging.info(output)

    time_file.write(output)


if __name__ == "__main__":
    script()
