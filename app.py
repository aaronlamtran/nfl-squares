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
    def __init__(self, season_type='pre', week=1, team_one='raiders', team_two='packers', year=2022, headless=False, single_year=None):
        self.seasons = {"1": list(range(1, 5)),
                        "2": list(range(1, 19)),
                        "3": list(range(1, 6))}
        self.boxes = ''
        self.matches = ''
        self.competitors = ''
        self.day_count = 1
        self.year = year
        self.single_year = single_year
        self.week = week
        self.team_one = team_one
        self.team_two = team_two
        self.season_type = season_type
        self.score_file = open("scores.txt", 'a')
        self.chrome_options = Options()
        self.chrome_options.headless = headless
        self.service = Service(executable_path=CHROME_DRIVER_PATH)
        self.driver = webdriver.Chrome(
            options=self.chrome_options, service=self.service)
        self.driver.implicitly_wait(50)
        self.main()

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
        logging.info('date formatted')
        print(row_scores)

        self.score_file.write(row_scores + '\n')

    def process_single_week(self):
        link = f'{BASE}{self.week}/year/{self.single_year}/seasontype/'
        self.driver.get(link)
        self.get_box()

    def process_season(self):
        for season_type, weeks in self.seasons.items():
            logging.info('new season type')
            for week in weeks:
                link = f'{BASE}{week}/year/{self.year}/seasontype/{season_type}'
                print(link)
                self.driver.get(link)
                self.get_box()

    def main(self):
        if self.single_year and self.week:
            self.process_single_week()
        else:
            print('skipping because none')
            self.process_season()

def script():
    start_time = time.time()

    scrape = Scrape(single_year=2021, week=2, headless=True)

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
