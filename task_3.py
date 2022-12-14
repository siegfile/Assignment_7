import argparse

parser = argparse.ArgumentParser()
parser.add_argument('file', type=argparse.FileType('r'))
parser.add_argument('-medals', nargs=2)
parser.add_argument('-output', '--output', type=argparse.FileType('w'))
parser.add_argument('-overall', nargs='*')


def medals(line, user_country, user_year, dict):
    sep_info = line.split('\t')
    if (sep_info[6] == user_country or sep_info[7] == user_country) and sep_info[9] == user_year and sep_info[14] != 'NA\n':
        print(sep_info[1], sep_info[12], sep_info[14])
        dict['sportsman_info'] = dict['sportsman_info'] + sep_info[1] + ' ' + sep_info[12] + ' ' + sep_info[14] + ';'
        if sep_info[14] == 'Gold\n': dict['gold'] += 1
        if sep_info[14] == 'Silver\n': dict['silver'] += 1
        if sep_info[14] == 'Bronze\n': dict['bronze'] += 1
        dict['index'] += 1

    return dict


def overall(line, dict):
    sep_info = line.split('\t')
    for i in dict:
        if i == sep_info[6] and sep_info[14] != 'NA\n':
            dict[i] = dict[i] + sep_info[9] + ';'

    return dict


args = parser.parse_args()

with args.file as file:
    next_line = file.readline()
    sport_dict = {'index': 0, 'sportsman_info': '', 'gold': 0, 'silver': 0, 'bronze': 0}
    overall_medals = dict.fromkeys(args.overall, '')
    while next_line != '':
        next_line = file.readline()
        if args.medals is not None and sport_dict['index'] < 10:
            sport_dict = medals(next_line, args.medals[0], args.medals[1], sport_dict)
        if args.overall is not None and next_line != '':
          overall_medals = overall(next_line, overall_medals)
    if args.medals is not None: print(sport_dict['gold'], sport_dict['silver'], sport_dict['bronze'])
    if args.output is not None:
        medalists = sport_dict['sportsman_info'].split(';')
        for name in medalists:
            args.output.writelines(name)
        args.output.writelines(str(sport_dict['gold']) + ' ' + str(sport_dict['silver']) + ' ' + str(sport_dict['bronze']) + ' ')
    if args.medals is not None and sport_dict['index'] == 0:
        print('Введена країна не існує або у введений рік не проводилась олімпіада')
    if args.overall is not None:
        for i in overall_medals:
            top_medals = 0
            top_year = 0
            overall_years = overall_medals[i].split(';')
            print(overall_medals[i])
            for j in range(2022):
                if overall_years.count(str(j)) > top_medals:
                    top_medals = overall_years.count(str(j))
                    top_year = j
            print(i, top_year, top_medals)
