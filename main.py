import argparse

parser = argparse.ArgumentParser()
parser.add_argument('file', type=argparse.FileType('r'))
parser.add_argument('-medals', dest='medals', nargs=2)
parser.add_argument('-output', '--output', type=argparse.FileType('w'))

args = parser.parse_args()

with args.file as file:
    next_line = file.readline()
    while next_line != '':
        next_line = file.readline()

