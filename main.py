import argparse

parser = argparse.ArgumentParser()
parser.add_argument('file', type=argparse.FileType('r'))
parser.add_argument('-medals', dest='medals', nargs=2)
parser.add_argument('-output', '--output', type=argparse.FileType('w'))


def medals(line, user_country, user_year, k):
    sep_info = line.split('\t')
    if (sep_info[6] == user_country or sep_info[7] == user_country) and sep_info[9] == user_year and sep_info[14] != 'NA\n':
        print(sep_info[1], sep_info[12], sep_info[14])
        k += 1

    return k


args = parser.parse_args()

with args.file as file:
    next_line = file.readline()
    count = 0
    while next_line != '':
        next_line = file.readline()
        if args.medals is not None and count < 10:
            count = medals(next_line, args.medals[0], args.medals[1], count)


