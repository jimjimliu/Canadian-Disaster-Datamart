from Config import MISSINGVALUE, MISSINGDATE, ALL_CA_PROVINCES, province_dic, \
    CA_REGIONS,PLACE_PREPOSITIONS, STOP_WORDS, OUTPUT_DIR, population_file
from CSVTable import CSVTable
import os
from DateDimension import DateDimension
from CostDimension import CostsDimension
from LocationDimension import LocationDimension
from DisasterDimension import DisasterDimension
from SummaryDimension import SummaryDimension
import csv
from itertools import islice
from utils import utils


class FactTable(CSVTable):
    def __init__(self):

        CSVTable.__init__(self, os.path.join(OUTPUT_DIR, 'fact.csv'),
                          ["StartDateKey", "EndDateKey", "LocationKey",
                          "DisasterKey", "DescriptionKey", "CostsKey",
                           "PopStatsKey",# "WheatherKey",
                          "NumFatalities", "NumInjured", "NumEvacuated"])

        # dictionary
        self.date_dic = {}
        self.cost_dic = {}
        self.disaster_dic = {}
        self.sum_dic = {}
        self.location_dic = {}
        # key: city name, value[population id, location id]
        self.city_pop_dic = {}
        self.pop_dic = {}

        print('loading population into dictionary')
        with open(population_file) as f:
            reader = csv.reader(f, delimiter=',', quotechar='"')
            for row in islice(reader, 1, None):
                if row[0] not in self.pop_dic.keys():
                    self.pop_dic[row[0]] = row[1]
        f.close()
        print('finish loading')


        self.date = DateDimension(self.date_dic)
        self.costs = CostsDimension(self.cost_dic)
        self.location = LocationDimension(self.location_dic, self.pop_dic, self.city_pop_dic)
        self.disaster = DisasterDimension(self.disaster_dic)
        self.summary = SummaryDimension(self.sum_dic)

    def extract(self, record,head):

        # Extract date
        start_date_key = self.date.parse(record, head['EVENT START DATE'])

        end_date_key = self.date.parse(record, head['EVENT END DATE'])

        # Extract costs
        costs_key = self.costs.parse(record,head)

        # Extract location
        location_key = self.location.extract(record,head)

        # Extract Disaster
        disaster_key = self.disaster.parse(record,head)
        if disaster_key is None: return

        # Extract summary
        description_key = self.summary.parse(record,head)

        # TODO Extract Whether info from additional source
        wheather_key = 'NULL'

        if location_key is not None:
            for index in location_key:
                # if city population can be found in dictionary, give fact table a pop key
                for key in self.city_pop_dic.keys():
                    if index == self.city_pop_dic[key][1]:
                        pop_stats_key = self.city_pop_dic[key][0]
                        break
                    else:
                        #in fact table, 1: indicates no population statistics found;
                        pop_stats_key = 1

                self.write_row((start_date_key, end_date_key, index,
                                disaster_key, description_key, costs_key,
                                pop_stats_key, #wheather_key,
                                utils.extract_int(record, head['FATALITIES']),
                                utils.extract_int(record, head['INJURED / INFECTED']),
                                utils.extract_int(record, head['EVACUATED'])))
