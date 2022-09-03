cat scores.txt | while read line; do echo $line | tr -cd , | wc -c | grep 4; done
