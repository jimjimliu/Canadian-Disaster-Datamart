from CSVTable import CSVTable


class DimensionTable(CSVTable):

    def __init__(self, output_fn, field_names, allow_duplicated=False):

        CSVTable.__init__(self, output_fn, field_names)

        if allow_duplicated:
            self.data_map = None
        else:
            # Use a dict to keep track which data as been added to the table
            # to avoid duplicated data
            self.data_map = dict()

        # Count how many rows have been extracted so far
        self.row_count = 0