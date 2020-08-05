from DimensionTable import DimensionTable
import os
from Config import OUTPUT_DIR
from utils import utils

class SummaryDimension(DimensionTable):

    def __init__(self, sum_dict):

        DimensionTable.__init__(self, os.path.join(OUTPUT_DIR, 'summary.csv'),
                                ["DescriptionKey", "Summary",
                                 "Keyword1", "Keyword2", "Keyword3"])
        self.row_counter = 0

        self.sum_dic = sum_dict

    def parse(self, record, head):

        summary = utils.extract_str(record, head['COMMENTS'])
        keywords = utils.extract_keywords(summary, 3)

        key = str(summary)

        if key in self.sum_dic.keys():
            return self.sum_dic[key]
        else:
            self.row_counter += 1
            self.sum_dic[key] = self.row_counter
            self.write_row((self.row_counter,
                            summary,
                            keywords[0][0] if len(keywords) > 0 else 'unknown',
                            keywords[1][0] if len(keywords) > 1 else 'unknown',
                            keywords[2][0] if len(keywords) > 2 else 'unknown'))
            return (self.row_counter)