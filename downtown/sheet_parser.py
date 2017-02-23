#! /usr/bin/env python

import csv
import requests


# Shandy's Test URL
URL = 'https://docs.google.com/spreadsheets/d/1MhY-qCFE4gyxfwpFjnA0bM6uoi8ZFI6AKhJjBXT8F9E/pub?gid=789892116&single=true&output=csv'

# Live URL
URL = 'https://docs.google.com/spreadsheets/d/1KuIeWepieysZf-f4C0FkB3oa1V9jGKe6DilThTNYdEE/pub?gid=0&single=true&output=csv'

def load_csv():
    csv_content = requests.get(URL).content

    lines = csv_content.split('\r\n')

    # ignore empty lines
    lines = [x for x in lines
             if x.strip(',')]

    reader = csv.DictReader(lines)

    return reader

def get_dims(cell_value):
    dims = cell_value.strip()
    if dims:
        try:
            dims = [float(measure) for measure in dims.split('x')]
            return dims
        except ValueError:
            print 'Had trouble with %s (%s)' % (m_dims)

def parse(reader):
    result = []
    for item in reader:
        m_dims = get_dims(item['Dimensions (metric)'])
        if not m_dims:
            i_dims = get_dims(item['Dimensions (imperial)'])
            if i_dims:
                m_dims = [measure * 0.305 for measure in i_dims]

        if not m_dims:
            print 'Had trouble with: ', item['Use']
        else:
            result.append([item['Use'], m_dims])
    return result


def main():
    csv_reader = load_csv()
    rectangles = parse(csv_reader)
    print rectangles

if __name__ == '__main__':
    main()
