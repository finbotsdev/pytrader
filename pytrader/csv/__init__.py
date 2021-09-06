# encoding: utf-8

import csv

# Real comments are more complicated ...
def is_comment(line):
    return line.startswith('#')

# Kind of sily wrapper
def is_whitespace(line):
    return line.isspace()

def iter_filtered(in_file, *filters):
    for line in in_file:
        if not any(fltr(line) for fltr in filters):
            yield line

# A dis-advantage of this approach is that it requires storing rows in RAM
# However, the largest CSV files I worked with were all under 100 Mb
def read_and_filter_csv(csv_path, *filters):
    with open(csv_path, 'r') as fin:
        iter_clean_lines = iter_filtered(fin, *filters)
        reader = csv.DictReader(iter_clean_lines, delimiter=',')
        return [row for row in reader]
