#! /usr/bin/env python

import csv
import requests

URL = 'https://docs.google.com/spreadsheets/d/1MhY-qCFE4gyxfwpFjnA0bM6uoi8ZFI6AKhJjBXT8F9E/pub?gid=789892116&single=true&output=csv'

csv_content = requests.get(URL).content

lines = csv_content.split('\r\n')

reader = csv.DictReader(lines)

for item in reader.next():
    print item


