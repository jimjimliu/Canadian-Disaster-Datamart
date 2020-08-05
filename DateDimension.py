from DimensionTable import DimensionTable
import os
from utils import utils
from Config import MISSINGVALUE, MISSINGDATE, ALL_CA_PROVINCES, province_dic, \
    CA_REGIONS,PLACE_PREPOSITIONS, STOP_WORDS, OUTPUT_DIR

class DateDimension(DimensionTable):

    def __init__(self, date_dict):

        DimensionTable.__init__(self, os.path.join(OUTPUT_DIR, 'date.csv'),
                                ["DateKey", "Day", "Month", "Year",
                                 "Weekend", "SeasonCA", "SeasonOther", "date"])
        # date attribute is used to compare and remove duplicate row;
        # to be deleted later.
        self.row_counter = 0
        self.weekend = ''
        self.date_dic = date_dict

    def parse(self, record, extra_data):

        date = utils.extract_date(record, extra_data)

        if record[extra_data] in self.date_dic.keys():
            return self.date_dic[record[extra_data]]

        elif date == MISSINGDATE:
            if date in self.date_dic.keys():
                return self.date_dic[date]
            else:
                self.row_counter += 1
                self.date_dic[MISSINGDATE] = self.row_counter
                self.write_row((self.row_counter, MISSINGVALUE, MISSINGVALUE, MISSINGVALUE, MISSINGVALUE, 'unknown'
                                , 'unknown', 'unknown'))
                return self.row_counter

        else:

            # accmulate row number;
            self.row_counter += 1

            # Find out which season in Canada for the given date
            if 3 <= date.month <= 5:
                season_in_ca = 'spring'
            elif 6 <= date.month <= 8:
                season_in_ca = 'summer'
            elif 9 <= date.month <= 11:
                season_in_ca = 'autumn'
            else:
                season_in_ca = 'winter'

            # Find out which season (international) for the given date
            if 1 <= date.month <= 3:
                season_inter = 'spring'
            elif 4 <= date.month <= 6:
                season_inter = 'summer'
            elif 7 <= date.month <= 9:
                season_inter = 'autumn'
            else:
                season_inter = 'winter'

            if date.weekday() >= 5:
                self.weekend = 'y'
            else:
                self.weekend = 'n'

            self.date_dic[record[extra_data]] = self.row_counter

            self.write_row((self.row_counter, date.day, date.month, date.year, self.weekend, season_in_ca, season_inter,
                            record[extra_data]))
            return (self.row_counter)