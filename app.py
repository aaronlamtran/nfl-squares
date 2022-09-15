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
import lineclass
import os
import time
import logging

logging.basicConfig(level=logging.INFO, filename='app.log', filemode='a',
                    format='[%(levelname)s] : %(asctime)s - %(message)s', datefmt='%m-%d-%y %H:%M:%S')


load_dotenv()


CHROME_DRIVER_PATH = os.getenv('CHROME_DRIVER_PATH') + "/chromedriver"
SOURCE_ONE = os.getenv('SOURCE_ONE')
SOURCE_TWO = os.getenv('SOURCE_TWO')
BASE = os.getenv('BASE')


class Scrape:
    def __init__(self, season_type='2', week=1, team_one='raiders', team_two='packers', year=2022, headless=False, single_year=None, mode='season'):
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
        self.row_template = ["00", "00", "00", "00", "00"]
        self.team_one = team_one
        self.team_two = team_two
        self.season_type = season_type
        self.mode = mode
        self.headless = headless
        self.season_type_string = ''
        self.score_file = open("scores.txt", 'a')
        self.log_pre_string = f'Y:{self.year}-W:{self.week}-ST:{self.season_type}'
        self.current_quarter = ''
        self.init_driver()
        # self.main()
    def grab_quarter(self):
        self.current_quarter = self.driver.find_element(By.CLASS_NAME, 'ScoreCell__Time.ScoreboardScoreCell__Time.h9.clr-gray-01').text
        print("self.current_quarter", self.current_quarter)
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
            logging.info(
                f'{self.log_pre_string}: Day {self.day_count}: {date.text}')


            self.matches = box.find_elements(
                By.CLASS_NAME, 'ScoreboardScoreCell__Competitors')
            self.get_competitors()

    def get_competitors(self):
        for match in self.matches:
            self.grab_quarter()
            logging.info(f'{self.log_pre_string}: new match')
            self.competitors = match.find_elements(By.TAG_NAME, 'li')
            self.current_match = []
            for each_competitor in self.competitors:
                self.current_match.append(each_competitor.text.split('\n')[0])
            print('self.current_match', self.current_match)



            self.current_week_match_counter += 1

            self.season_type_string = self.pre_reg_post[str(self.season_type)]

            path = f'all-seasons/csv/{self.year}/{self.season_type_string}/week{self.week}'
            path_flattened = f'all-seasons/txt/{self.year}/{self.season_type_string}/week{self.week}'

            is_dir_exist = os.path.exists(path)
            is_dir_exist_flattened = os.path.exists(path_flattened)

            if not is_dir_exist:
                os.makedirs(path)
            if not is_dir_exist_flattened:
                os.makedirs(path_flattened)

            file_extension = '.txt'
            file_extension_flattened = '.txt'
            file_pre_name_counter = str(self.current_week_match_counter)

            if len(file_pre_name_counter) == 1:
                file_pre_name_counter = ''.join(('0', file_pre_name_counter))

            filename = f'{file_pre_name_counter}-{self.current_match[0].lower()}-{self.current_match[1].lower() + file_extension}'
            filename_flattened = f'{file_pre_name_counter}-{self.current_match[0].lower()}-{self.current_match[1].lower() + file_extension_flattened}'

            absolute_path = os.path.join(path, filename)
            absolute_path_flattened = os.path.join(
                path_flattened, filename_flattened)

            logging.info(f'{self.log_pre_string}: creating {absolute_path}')
            logging.info(
                f'{self.log_pre_string}: creating {absolute_path_flattened}')

            self.current_match_file = open(absolute_path, 'w')
            self.flattened_match_file = open(absolute_path_flattened, 'w')

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

            try:
                self.team_scores_all_quarters = self.team_scores_all_quarters[0].text.split("\n")
            except Exception as error:
                logging.error(error)

            try:
                for i in range(len(self.team_scores_all_quarters)):

                    if len(self.team_scores_all_quarters[i]) == 1:

                        self.team_scores_all_quarters[i] = "0" + self.team_scores_all_quarters[i]
                        self.row_template[i] = self.team_scores_all_quarters[i]
                    else:
                        self.row_template[i] = self.team_scores_all_quarters[i]
                temporary = "".join(self.row_template)
                self.team_scores_all_quarters = temporary

            except Exception as error:
                logging.error(error)
            self.format_quarter_scores()


    def format_quarter_scores(self):
        row_scores = self.team_scores_all_quarters
        self.row_template = ["00", "00", "00", "00", "00"] #reset
        row_scores = "".join(str(x) for x in row_scores)
        logging.info(f'{self.log_pre_string}: quarter scores formatted')
        # print('ROW_SCORES', row_scores)
        line = lineclass.WLine(row_scores)
        print(line.get_line())
        self.score_file.write(row_scores + '\n')
        self.score_file.write(f'from Wline:{line.get_line()}\n')


        self.current_match_file.write(row_scores + '\n')
        self.flattened_match_file.write(line.get_line() + '\n')
        logging.info(
            f'{self.log_pre_string}: score_file: new formatted row added')

    def process_single_week(self, year=2022, week=1):
        self.year = year
        self.week = week  # TODO handle season_type
        self.update_log_string()
        # link = f'{BASE}{self.week}/year/{self.year}/seasontype/{self.season_type}'
        link = 'http://127.0.0.1:5500/live-2nd-q.html'
        print(link)
        self.driver.get(link)
        self.reset_week_game_counter()
        self.get_box()
        # self.close_driver()

    def reset_week_game_counter(self):
        self.current_week_match_counter = 0
        logging.info(f'{self.log_pre_string}::week_game_counter reset')

    def update_log_string(self):
        self.log_pre_string = f'Y:{self.year}-W:{self.week}-ST:{self.season_type}'

    def process_season(self):
        if self.year < 2021:
            self.seasons = {
                "1": list(range(1, 5)),
                "2": list(range(1, 18)),
                "3": list(range(1, 6))
            }
        for season_type, weeks in self.seasons.items():
            logging.info(f'{self.log_pre_string}:new season type')
            for week in weeks:
                self.week = week
                self.season_type = season_type
                self.update_log_string()
                link = f'{BASE}{self.week}/year/{self.year}/seasontype/{self.season_type}'
                print(link)
                self.driver.get(link)
                self.reset_week_game_counter()
                self.get_box()
        # self.close_driver()


    def keep_looping_week(self, year, week):
        self.year = year
        self.week = week
        while True:
            self.process_single_week(year, week)

    def close_driver(self):
        self.driver.close()

    def process_years(self, from_year=2002, to_year=2021):
        print(f'processing seasons from {from_year} to {to_year}')
        for year in range(from_year, to_year):
            print(year)
            self.year = year
            self.process_season()
        self.close_driver()
        # scrape = Scrape(year=year, headless=True)

    def main(self):
        if self.mode == 'season':
            print('prcoessing whole season')
            self.process_season()
        else:
            print('prcoessing single week')
            self.process_single_week()


def script():
    try:
        start_time = time.time()

        scrape = Scrape(headless=True)
        # scrape.process_years(from_year=2010, to_year=2022)
        scrape.process_single_week(year=2017, week=1)

        end_time = time.time()
        execution_time = str(end_time - start_time)

        print('Execution time in seconds: ' + execution_time)

        time_file = open("time.txt", "a")

        output = f"headless: " + str(scrape.chrome_options.headless) + \
            " - " + execution_time + "\n"

        logging.info(output)

        time_file.write(output)
    except Exception as error:
        print(error)
        logging.error(error)


if __name__ == "__main__":
    script()
