import mysql.connector
from Config import OUTPUT_DIR, DB_SCHEMA
import os
from itertools import islice
from utils import utils
import csv

class Database():

    def __init__(self):
        self.db_connection = utils.sql_connection('')
        self.cursor = self.db_connection.cursor()

    def populate_tables(self):
        print("Populating database.")
        self.cursor.execute('''
            drop schema if exists disaster_DB;
        ''')
        self.create_schema()
        self.populate_date()
        self.populate_cost()
        self.populate_location()
        self.populate_disaster()
        self.populate_description()
        self.populate_population()
        self.populate_fact()
        self.db_connection.close()
        print("Database population complete.")

    def create_schema(self):
        schema = DB_SCHEMA
        for sql in schema:
            try:
                self.cursor.execute(sql)
            except Exception as e:
                self.db_connection.rollback()  # 事务回滚
                print('Event Failed', e)
            else:
                self.db_connection.commit()  # 事务提交
                print('Event successful', self.cursor.rowcount)

    def populate_date(self):
        with open(os.path.join(OUTPUT_DIR, 'date.csv')) as f:
            f_csv = csv.reader(f, delimiter=',', quotechar='"')

            for row in islice(f_csv, 1, None):
                for i in range(0, len(row)):
                    # According to professor herna's words, substituting missing values to null
                    if row[i] == '': row[i] = None

                self.cursor.execute("insert into disaster_DB.date values(%s,%s,%s,%s,%s,%s,%s,%s)",
                            [row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]])
            self.db_connection.commit()

    def populate_cost(self):
        with open(os.path.join(OUTPUT_DIR, 'costs.csv')) as f:
            f_csv = csv.reader(f, delimiter=',', quotechar='"')

            for row in islice(f_csv, 1, None):

                for i in range(0, len(row)):
                    # According to professor herna's words, substituting missing values to null
                    if row[i] == '': row[i] = None

                self.cursor.execute("insert into disaster_DB.costs values(%s,%s,%s,%s,%s,%s,%s)",
                            [row[0], row[1], row[2], row[3], row[4], row[5], row[6]])
            self.db_connection.commit()

    def populate_location(self):
        with open(os.path.join(OUTPUT_DIR, 'location.csv')) as f:
            f_csv = csv.reader(f, delimiter=',', quotechar='"')

            for row in islice(f_csv, 1, None):
                self.cursor.execute("insert into disaster_DB.location values(%s,%s,%s,%s,%s)",
                            [row[0], row[1], row[2], row[3], row[4]])
            self.db_connection.commit()

    def populate_disaster(self):
        with open(os.path.join(OUTPUT_DIR, 'disaster.csv')) as f:
            f_csv = csv.reader(f, delimiter=',', quotechar='"')

            for row in islice(f_csv, 1, None):
                for i in range(0, len(row)):
                    # According to professor herna's words, substituting missing values to null
                    if row[i] == '': row[i] = None
                self.cursor.execute("insert into disaster_DB.disaster values(%s,%s,%s,%s,%s,%s,%s)",
                            [row[0], row[1], row[2], row[3], row[4], row[5], row[6]])
            self.db_connection.commit()

    def populate_description(self):
        with open(os.path.join(OUTPUT_DIR, 'summary.csv')) as f:
            f_csv = csv.reader(f, delimiter=',', quotechar='"')

            for row in islice(f_csv, 1, None):
                self.cursor.execute("insert into disaster_DB.summary values(%s,%s,%s,%s,%s)",
                            [row[0], row[1], row[2], row[3], row[4]])
            self.db_connection.commit()

    def populate_population(self):
        with open(os.path.join(OUTPUT_DIR, 'population.csv')) as f:
            f_csv = csv.reader(f, delimiter=',', quotechar='"')

            for row in islice(f_csv, 1, None):
                for i in range(0, len(row)):
                    # According to professor herna's words, substituting missing values to null
                    if row[i] == '': row[i] = None

                self.cursor.execute("insert into disaster_DB.population values(%s,%s,%s)",
                            [row[0], row[1], row[2]])
            self.db_connection.commit()

    def populate_fact(self):
        with open(os.path.join(OUTPUT_DIR, 'fact.csv')) as f:
            f_csv = csv.reader(f, delimiter=',', quotechar='"')

            for row in islice(f_csv, 1, None):
                for i in range(0, len(row)):
                    # According to professor herna's words, substituting missing values to null
                    if row[i] == '': row[i] = None
                self.cursor.execute("insert into disaster_DB.fact values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                            [row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]])
            self.db_connection.commit()


if __name__ == '__main__':
    Database()