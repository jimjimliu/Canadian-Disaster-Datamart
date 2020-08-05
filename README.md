<p align="center">
<img src="https://github.com/jimjimliu/Fake-News-Stance-Detection/blob/master/img/uw.png" alt="uw" width="35%"/>
</p>



<h1 align = "center">UWaterloo - Canadian Disaster Machine Learning Analysis</h1>
<p align="center">
</p>



## Introduction

The project aims to predict a disaster type [natural, technology, conflict, unknown] from features such as [money spent on recovering, fatalities, people evacuated, etc]. The first step performed is following an ETL(extract, transfer, load). The data is extracted from across the Internet and sources will be cited in the following subsections. The data mart is loaded into MySQL database. Both supervised and unsupervised learnings are performed. 

### Data

------

The input data sets are composed of two files which are located in `../data` folder:

- [CanadianDisasterDatabase.csv](https://www.publicsafety.gc.ca/cnt/rsrcs/cndn-dsstr-dtbs/index-en.aspx)
- [population.csv](https://worldpopulationreview.com/countries/cities/canada)

### To Run

------

- Locate `utils.py -> sql_connection()`, configure the `passwd` parameter to your own MySQL database.
- The driver script is `main.py`, to run the project, simply run `python3 main.py`.

While running `main.py`, a MySQL database named `disaster_DB` is created. This is the data mart we create.

### Folders

------

Every input & output files are stored inside `../data` folder.

- `data/physical_model` contains the .sql script to create a MySQL database schema. The script is automatically run by `main.py` so you do not need to perform additional step to create a database. 
- `data/datamart` is a pysical representation of the data mart in .txt files, which contains a fact table and according dimension tables. 
- `data/clustering` contains screenshots of clusterings run by python.
- `data/dashboard` contains Tableau screenshots to summarize the input data in a compact representation.
- `data/model_accuracy` contains a screenshot which compares the accuracies of several classifiers.

### Visulization

------

<p align="center">
<img src="https://github.com/jimjimliu/Canadian-Disaster-Datamart/blob/master/data/dashboard/dashboard.png" alt="fnc" width="100%"/>
</p>



















