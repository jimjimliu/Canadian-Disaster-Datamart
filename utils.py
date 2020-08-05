from collections import Counter
from Config import MISSINGVALUE, MISSINGDATE, ALL_CA_PROVINCES, province_dic, \
    CA_REGIONS,PLACE_PREPOSITIONS, STOP_WORDS
import re
from datetime import datetime
import string
import mysql.connector

class utils(object):

    def extract_int(record, field_name):
        value = record[field_name]
        if len(value) == 0:
            return MISSINGVALUE

        try:
            return int(value)
        except ValueError:

            return MISSINGVALUE

    def extract_float(record, field_name):
        value = record[field_name]
        if len(value) == 0:
            return MISSINGVALUE

        try:
            return float(value)
        except ValueError:

            return MISSINGVALUE

    def extract_str(record, field_name):
        value = record[field_name]
        if len(value) == 0:
            return 'unknown'
        else:
            return value

    def extract_date(record, field_name):
        date_format = '%m/%d/%Y'
        value = record[field_name]
        if len(value) == 0:
            return MISSINGDATE

        try:
            return datetime.strptime(value, date_format)
        except ValueError:

            return MISSINGDATE

    def get_location(place):
        # version 2

        locations = []

        place = place.replace("(", "").replace(")", "")

        while len(place) > 0:
            found = False

            # Search in provinces and territories
            for province_abbr, province in ALL_CA_PROVINCES:

                if province_abbr in place:
                    idx1 = place.index(province_abbr)
                    idx2 = idx1 + len(province_abbr)
                elif province in place:
                    idx1 = place.index(province)
                    idx2 = idx1 + len(province)
                else:
                    continue

                cities_info = place[0:idx1].strip()
                if cities_info.startswith("and "):
                    cities_info = cities_info[4:]
                place = place[idx2:].strip()

                cities = []
                for city in cities_info.replace(" and ", ",").replace(";", ",").split(","):
                    city = city.strip()
                    if len(city) > 0 and city[0] in string.ascii_uppercase:
                        cities.append(city)

                if len(cities) > 0:
                    for city in cities:
                        locations.append([city, province, 'Canada', 'y'])
                else:
                    maincity = 'unknown'
                    if province in province_dic.keys():
                        maincity = province_dic[province]
                    locations.append([maincity, province, 'Canada', 'y'])

                found = True
                break

            if found:
                continue

            # Search in region list
            for region in CA_REGIONS:

                if region in place:
                    idx1 = place.index(region)
                    idx2 = idx1 + len(region)
                    place = place[idx2:]

                    provinces = CA_REGIONS[region]
                    if provinces is not None:
                        for province in provinces:
                            # parse regions to provinces and their main cities
                            maincity = 'unknown'
                            if province in province_dic.keys():
                                maincity = province_dic[province]
                            locations.append([maincity, province, 'Canada', 'y'])
                    else:
                        locations.append([region, region, 'Canada', 'y'])

                    found = True
                    break

            if found:
                continue

            # Assume the place is in from City, State, Country or City,Country or Country
            for prep in PLACE_PREPOSITIONS:
                place = place.replace(prep, ",")
            cities_info = []
            for t in place.split(","):
                t = t.strip()
                if len(t) > 0 and t[0].isupper():
                    cities_info.append(t)

            if 0 < len(cities_info) <= 3:
                country = cities_info[-1]
                valid_country = True
                for term in country.split():
                    if not term[0].isupper():
                        valid_country = False
                        break

                if valid_country:
                    place = ""
                    found = True

                    if len(cities_info) == 3:
                        is_canada = ''
                        if country == 'Canada':
                            is_canada = 'y'
                        else:
                            is_canada = 'n'
                            if country == 'City': country = 'unknown'
                        locations.append([cities_info[0], cities_info[1], country, is_canada])
                    elif len(cities_info) == 2:
                        is_canada = ''
                        if country == 'Canada':
                            is_canada = 'y'
                        else:
                            is_canada = 'n'
                            if country == 'City': country = 'unknown'
                        locations.append([cities_info[0], 'unknown', country, is_canada])
                    elif len(cities_info) == 1:
                        is_canada = ''
                        if country == 'Canada':
                            is_canada = 'y'
                        else:
                            is_canada = 'n'
                            if country == 'City': country = 'unknown'
                        locations.append(['unknown', 'unknown', country, is_canada])

            if not found:
                break

        # final filtering
        for location in locations:
            for key in province_dic.keys():
                # if city information cannot be parsed from input string, use its main city
                if key.lower() in location[0].lower():
                    if 'and' in location[0].lower():
                        result = [province_dic[location[1]], location[1], 'Canada', 'y']
                        locations.append(result)
                    location[0] = province_dic[key]
                    location[1] = key
            if location[1] == 'Québec': location[1] = 'Quebec'

        return locations

    def extract_keywords(text, num_keywords=3):
        counter = Counter(w for w in re.split('\W+', text.lower())
                          if len(w) > 2 and w not in STOP_WORDS)

        return counter.most_common(num_keywords)

    def sql_connection(pwd):
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd=""
        )
        return db_connection

    def check_balanced(df, column):
        '''
        check if the data set is balanced using the given column as label.
        Return each label's distribution percentage to see if the dataset is balanced.
        :return:
            (Dict): dictionary has key=label_name, value=label percentage
        '''

        # vc is pandas series
        vc = df[column].value_counts()
        # row counts of df
        row_count = df.shape[0]

        result_dict = {}
        for i, v in vc.items():
            result_dict[i] = v, v/row_count

        return result_dict

    def print_info(text=None):
        print("================================================")
        print("|                                              |")
        print("|", text, " "*(len("================================================")-len(text)-5) , "|")
        print("|                                              |")
        print("================================================")

