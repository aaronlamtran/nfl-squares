import os
import glob
path = 'all-seasons/2020/regular/week12/'
team = 'raiders'
for filename in glob.glob(path + '*' + team + '*'):
  file = open(filename, 'r')
  line = file.readline()
  print(line)
  away = line.split('\n')[0].split(',')
  # away = away
  print(away)
  line = file.readline()
  print(line)
