from utils import utils
import csv
from FactTable import FactTable
from Config import INPUT_SOURCE_FILE
from Database import Database
import numpy as np
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
import pandas as pd
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
from sklearn.cluster import KMeans
from sklearn.datasets import make_classification
import matplotlib.pyplot as plt
from numpy import unique
from numpy import where
from tqdm import tqdm

LABELS = ['Technology', 'Natural', 'Conflict', 'unknown']

class main():

    def __init__(self):
        self.path = "path"
        self.__model_score = {}

    def run(self):
        '''

        :return:
        '''
        "building data mart from raw data"
        utils.print_info("Buidling Datamart")
        # build a data mart from raw input data files
        self.build_data_mart()
        # # read in local files and populate database
        Database().populate_tables()

        # get input data file from data mart
        "loading input data from database"
        utils.print_info("loading input data from database")
        print("Making connection to database.")
        db_con = utils.sql_connection("")
        cursor = db_con.cursor()
        print("Retriving input data from database.")
        cursor.execute('use disaster_DB;')
        cursor.execute('''
            SELECT 
            DI.disaster_category, DI.disaster_group,DI.disaster_subgroup,
            DI.disaster_type, L.city, P.population, L.province,L.country, D.date as start_day, D.season_ca,F.fatalities,
            F.evacuated, D2.date as end_day, C.estimated_total_cost
            FROM 
                fact F, location L, date D,date D2, disaster DI, summary S, costs C, population P
            WHERE 
                F.start_date_key=D.date_key and F.end_date_key=D2.date_key and 
            F.location_key=L.location_key and F.disaster_key=DI.disaster_key and
            F.description_key=S.description_key and F.cost_key=C.cost_key and F.popstats_key=P.population_key;
        ''')
        data = cursor.fetchall()
        df = np.array(data)
        df = pd.DataFrame(df, columns=['disaster_category','disaster_group','disaster_subgroup','disaster_type',
                                       'city','population','province','country','start_day','season_ca','fatalities',
                                       'evacuated', 'end_day', 'estimated_total_cost'])

        df['target'] = -1
        for i in range(len(LABELS)):
            df.loc[df['disaster_group'] == LABELS[i], 'target'] = i
        # print(df.isnull().sum())

        # filling missing values using mean value of each column
        print("Processing missing values.")
        df = df.fillna(df.mean())
        df['population']= df['population'].astype(float)
        df['estimated_total_cost'] = df['estimated_total_cost'].astype(float)
        # unremove unwanted columns
        df = df[['population','fatalities','evacuated','estimated_total_cost', 'target']]
        X = df[['population','fatalities','evacuated','estimated_total_cost']]
        y = df[['target']]

        # split train, test set
        print("Preparing training and testing data.")
        X_train, X_test, y_train, y_test =  train_test_split(X, y, train_size=0.8, random_state=0)
        X_train = np.array(X_train)
        y_train =  np.array([item[0] for item in y_train.to_numpy()])
        X_test = np.array(X_test)
        y_test = np.array([item[0] for item in y_test.to_numpy()])

        # # over-sampling
        print("Over-sampling.")
        # sm = SMOTE(random_state=0, k_neighbors=4)
        # X_train, y_train = sm.fit_resample(X_train, y_train)

        # classify
        utils.print_info("Supervised learning")
        self.clf_comparison(X_train, y_train, X_test, y_test)

        # unsupervised learning, clustering
        utils.print_info("Un-supervised learning")
        # X =  df[['population','evacuated']].to_numpy()
        # X = df[['fatalities', 'evacuated']].to_numpy()
        X = df[['estimated_total_cost', 'evacuated']].to_numpy()
        clf = KMeans(n_clusters=8)
        clf.fit(X)
        p = clf.predict(X)
        # Generate scatter plot for training data
        colors = list(map(lambda x: '#3b4cc0' if x == 1 else '#b40426', p))
        plt.scatter(X[:, 0], X[:, 1], marker="o", picker=True, c=p)
        plt.title('clusters of data')
        plt.xlabel('estimated_total_cost')
        plt.ylabel('evacuated')
        plt.show()

        self.show_plot()



    def build_data_mart(self):

        with open(INPUT_SOURCE_FILE) as source_file:
            reader = csv.reader(source_file, delimiter=',', quotechar='"')

            # make head a dictionary with keys the field names;
            # head = ['fieldname':index, ...]
            head = dict(reversed(field) for field in enumerate(next(reader)))

            fact = FactTable()

            # record: type is list;
            # record: [data, data, ...]
            for record in tqdm(reader, desc="Buidling datamart: "):
                # pass (head) as a look up dictionary for record list;
                # use the value of key in head as index of record list;
                fact.extract(record, head)

            source_file.close()

        return

    def classifiers(self):
        return [
            (SVC(C=50.0, cache_size=200, class_weight=None, coef0=0.0,
                 decision_function_shape='ovr', degree=3, gamma='auto', kernel='rbf',
                 max_iter=-1, probability=True, random_state=None, shrinking=True,
                 tol=0.001, verbose=False), 'SVM', 'SVM'),

            (GradientBoostingClassifier(random_state=0), 'GBDT', 'GBDT'),

            (KNeighborsClassifier(1), "K NN ", 'KNN'),

            # (QuadraticDiscriminantAnalysis(), 'Qudratic Discriminant Analysis', 'QD'),

            (RandomForestClassifier(max_depth=50, n_estimators=10, max_features=1), 'Random Forest Classifier', 'RF'),

            (AdaBoostClassifier(base_estimator=None, n_estimators=50, learning_rate=0.01,
                                algorithm='SAMME.R', random_state=None), 'Adaboost Classifier', 'Ada'),
            # (SGDClassifier(), 'SGD Classifier', 'SGD'),

            (DecisionTreeClassifier(max_depth=5), 'Decision Tree Classifier', 'DT'),

            (LinearDiscriminantAnalysis(solver='svd', shrinkage=None, priors=None, n_components=None,
                                        store_covariance=False, tol=0.00001), 'Linear Discriminant Analysis', 'LDA'),

            # (GaussianNB(), 'Gaussian Naive Bayes ', 'GNB')
        ]

    def clf_comparison(self, X, y, X_test, y_test):

        for model, name, initial in self.classifiers():
            print("Fitting...")
            clf = model.fit(X, y)
            print("Predicting...")
            predictions = clf.predict(X_test)
            test_score = clf.score(X_test, y_test)
            print(name, " Testing score: ", test_score)
            self.__model_score[initial] = [float(test_score)]

    def show_plot(self):

        fig = plt.figure()
        ax = fig.add_subplot(111)
        metrics = np.array(list(self.__model_score.values()))
        accu = metrics[:, 0] #accuracy
        plt.plot(accu)
        for i, label in enumerate(list(self.__model_score.keys())):
            plt.text(i, accu[i], label)
        plt.show()


if __name__ == '__main__':

    main().run()