from DimensionTable import DimensionTable
from Config import OUTPUT_DIR
import os
from CSVTable import CSVTable
from utils import utils


class LocationDimension(DimensionTable):

    def __init__(self, location_dict, pop_dict, city_pop_dict):

        DimensionTable.__init__(self, os.path.join(OUTPUT_DIR, 'location.csv'),
                                ["LocationKey", "City", "Province", "Country", "Canada"])

        self.population_dimension = CSVTable(os.path.join(OUTPUT_DIR, 'population.csv'),
                                             ["Population_key", "City", "Population"])
        self.population_dimension.write_row([1, None, None])

        # store location id
        self.group_key = 0
        # store population dimension id, use to match with a location in city_pop dictionary;
        self.pop_key = 1
        self.location_dic=location_dict
        self.pop_dic = pop_dict
        self.city_pop_dic = city_pop_dict

    def extract(self, record, head):
        # Extract data from the record
        locations = utils.get_location(record[head['PLACE']])

        if len(locations) == 0:
            # if in the dictionary, return value
            if ('unknown', 'unknown', 'unknown', 'unknown') in self.location_dic.keys():
                return [self.location_dic[('unknown', 'unknown', 'unknown', 'unknown')]]
            else:
                # if not, insert it;
                self.group_key += 1
                self.location_dic[('unknown', 'unknown', 'unknown', 'unknown')] = self.group_key
                row = [self.group_key]
                row.extend(('unknown', 'unknown', 'unknown', 'unknown'))
                self.write_row(row)
                return [self.group_key]

        location_keys = []
        for location in locations:
            # there is a hit in population dictionary, write it to dimension
            # add it to dictionary for fact table pop key look up
            if location[0] in self.pop_dic.keys():
                if location[0] not in self.city_pop_dic.keys():
                    self.pop_key += 1
                    self.population_dimension.write_row([self.pop_key, location[0], self.pop_dic[location[0]]])
                    self.city_pop_dic[location[0]] = [self.pop_key, None]

            if (location[0], location[1], location[2]) in self.location_dic.keys():
                location_keys.append(self.location_dic[(location[0], location[1], location[2])])
                if location[0] in self.city_pop_dic.keys():
                    self.city_pop_dic[location[0]][1] = self.location_dic[(location[0], location[1], location[2])]
            else:
                self.group_key += 1
                self.location_dic[(location[0], location[1], location[2])] = self.group_key
                row = [self.group_key]
                row.extend(location)
                self.write_row(row)
                location_keys.append(self.group_key)
                if location[0] in self.city_pop_dic.keys():
                    self.city_pop_dic[location[0]][1] = self.group_key

        return location_keys
