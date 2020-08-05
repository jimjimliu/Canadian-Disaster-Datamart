from DimensionTable import DimensionTable
import os
from Config import OUTPUT_DIR
from utils import utils


class DisasterDimension(DimensionTable):

    def __init__(self, disaster_dict):

        DimensionTable.__init__(self, os.path.join(OUTPUT_DIR, 'disaster.csv'),
                                ["DisasterKey", "DisasterType",
                                 "DisasterSubgroup", "DisasterGroup",
                                 "DisasterCategory", "Magnitude",
                                 "UtilityPeopleAffected"])
        self.row_counter = 0

        self.disaster_dic = disaster_dict

    def parse(self, record, head):

        type = utils.extract_str(record, head['EVENT TYPE'])
        subgroup = utils.extract_str(record, head['EVENT SUBGROUP'])
        egroup = utils.extract_str(record, head['EVENT GROUP'])
        cat = utils.extract_str(record, head['EVENT CATEGORY'])
        if len(cat) > 15: return None
        mag = utils.extract_float(record, head['MAGNITUDE'])
        paffacted = utils.extract_int(record, head['UTILITY - PEOPLE AFFECTED'])

        key = str(type) + "," + str(subgroup) + "," + str(egroup) + "," + str(cat) + "," + str(mag) + "," + str(
            paffacted)
        if key in self.disaster_dic.keys():
            return self.disaster_dic[key];
        else:
            self.row_counter += 1
            self.disaster_dic[key] = self.row_counter
            self.write_row((self.row_counter, type, subgroup, egroup, cat, mag, paffacted))
            return (self.row_counter)
