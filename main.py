import argparse

parser = argparse.ArgumentParser()
parser.add_argument('file', type=argparse.FileType('r'))
parser.add_argument('-medals', nargs=2)
parser.add_argument('-output', '--output', type=argparse.FileType('w'))
parser.add_argument('-overall', nargs='*')
parser.add_argument('-total', nargs=1)

def total(line, year, dict):
    line = line[:-1]
    sep_info = line.split('\t')
    country = sep_info[6]
    medal = sep_info[14]
    if year == sep_info[9]:
        if medal != 'NA':
            if country in dict:
                if medal in dict[country]:
                    dict[country][medal] += 1
                else:
                    dict[country][medal] = 1
            else:
                dict[country] = {}
                dict[country][medal] = 1
    return dict


def medals(line, user_country, user_year, dict):
    sep_info = line.split('\t')
    if (sep_info[6] == user_country or sep_info[7] == user_country) and sep_info[9] == user_year and sep_info[14] != 'NA\n' and dict['index'] < 10:
        print(sep_info[1], sep_info[12], sep_info[14])
        dict['sportsman_info'] = dict['sportsman_info'] + sep_info[1] + ' ' + sep_info[12] + ' ' + sep_info[14] + ';'
        dict['index'] += 1
    if sep_info[14] == 'Gold\n' and sep_info[6] == user_country or sep_info[7] == user_country and sep_info[9] == user_year: dict['gold'] += 1
    if sep_info[14] == 'Silver\n' and sep_info[6] == user_country or sep_info[7] == user_country and sep_info[9] == user_year: dict['silver'] += 1
    if sep_info[14] == 'Bronze\n' and sep_info[6] == user_country or sep_info[7] == user_country and sep_info[9] == user_year: dict['bronze'] += 1
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
    if args.overall is not None: overall_medals = dict.fromkeys(args.overall, '')
    if args.total is not None: total_dict = dict()
    next_line = file.readline()
    while next_line != '':
        if args.medals is not None:
            sport_dict = medals(next_line, args.medals[0], args.medals[1], sport_dict)
        if args.overall is not None:
          overall_medals = overall(next_line, overall_medals)
        if args.total is not None:
            total_dict = total(next_line, args.total[0], total_dict)
        next_line = file.readline()
    if args.medals is not None: print(sport_dict['gold'], sport_dict['silver'], sport_dict['bronze'])
    if args.output is not None:
        medalists = sport_dict['sportsman_info'].split(';')
        for name in medalists:
            args.output.writelines(name)
        args.output.writelines(str(sport_dict['gold']) + ' ' + str(sport_dict['silver']) + ' ' + str(sport_dict['bronze']) + ' ')
    if args.medals is not None and sport_dict['index'] == 0:
        print('Введена країна не існує або у введений рік не проводилась олімпіада')
    if args.total is not None:
        for country, medals in total_dict.items():
            print(f'{country}')
            for medal, amount in medals.items():
                print(f'\t {medal}, {amount}')
    if args.overall is not None:
        for i in overall_medals:
            top_medals = 0
            top_year = 0
            overall_years = overall_medals[i].split(';')
            for j in range(2022):
                if overall_years.count(str(j)) > top_medals:
                    top_medals = overall_years.count(str(j))
                    top_year = j
            print(i, top_year, top_medals)

