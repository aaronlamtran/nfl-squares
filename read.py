import os
import glob
import time
from datetime import date
import app

scrape = app.Scrape()

today = date.today()

start = time.time()

# print('hello')
def check_if_today_has_football():

    d1 = today.strftime("%B %d, %Y")
    print('d1', d1)
    scrape.keep_looping_week(year=2022, week=1)
    pass


def try_this():
    team_one = 'raiders'
    path = 'all-seasons/txt/2021/*/*/'
    file_counter = 0
    found = []
    for filename in glob.glob(path + '*' + team_one + '*'):
        seasons, filetype, year, season_type, week_num, filename_w_ext = filename.split(
            '/')
        print(seasons, filetype, year, season_type, week_num, filename_w_ext)

        file_counter += 1
        file = open(filename, 'r')
        line = file.readline()
        line_two = file.readline()
        print(line)
        print(line_two)
        payload = {
            'filename': filename,
            'filetype': filetype,
            'year': year,
            'season_type': season_type,
            'week_num': week_num,
            'filename_w_ext': filename_w_ext,
            'line_one_away': line,
            'line_two_home': line_two
            # need team_one_away
            # need team_two_home,
            # need away_q1, q2, 3, 4, f
            # need home_q1, q2, 3, 4, f
            # need game_done
        }
        found.append(payload)
    print(found)
    print(file_counter, 'files')

    end = time.time()

    # print('query for ', "seconds")
    total_time = end - start
    print(total_time, "seconds")
    # print(found)
    return found


if __name__ == "__main__":
#     try_this()
    check_if_today_has_football()