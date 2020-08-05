from DimensionTable import DimensionTable
import os
from utils import utils
from Config import OUTPUT_DIR


class CostsDimension(DimensionTable):

    def __init__(self, cost_dict):

        DimensionTable.__init__(self, os.path.join(OUTPUT_DIR, 'costs.csv'),
                                ["CostsKey",
                                 "EstimatedTotalCost", "NormalizedTotalCost",
                                 "FederalPayments",
                                 "ProvincialDeptPayments",
                                 "ProvincialDFAAPayments",
                                 "InsurancePayments"])
        self.row_counter = 0
        self.cost_dic = cost_dict

    def parse(self, record, head):
        """Extract cost values from the record"""
        etc = utils.extract_float(record, head['ESTIMATED TOTAL COST'])
        ntc = utils.extract_float(record, head['NORMALIZED TOTAL COST'])
        fdp = utils.extract_float(record, head['FEDERAL DFAA PAYMENTS'])
        pdp = utils.extract_float(record, head['PROVINCIAL DEPARTMENT PAYMENTS'])
        pdap = utils.extract_float(record, head['PROVINCIAL DFAA PAYMENTS'])
        ip = utils.extract_float(record, head['INSURANCE PAYMENTS'])
        string = str(etc) + "," + str(ntc) + "," + str(fdp) + "," + str(pdp) + "," + str(pdap) + "," + str(ip)
        if string in self.cost_dic.keys():
            return self.cost_dic[string]
        else:
            self.row_counter += 1
            self.cost_dic[string] = self.row_counter;
            self.write_row((self.row_counter, etc, ntc, fdp, pdp, pdap, ip))
            return (self.row_counter)
