import csv


class CSVTable:

    def __init__(self, output_fn, field_names):
        self.field_names = field_names

        # create file
        self.csvfile = open(output_fn, 'w')
        # create writer of the file
        self.writer = csv.DictWriter(self.csvfile, field_names)

        # write the header row first
        self.writer.writeheader()

    def write_row(self, data):
        # make the data in a dictionary, the keys are filed names;
        row = dict(zip(self.field_names, data))
        # write the row
        self.writer.writerow(row)

    def close(self):
        self.csvfile.close()
