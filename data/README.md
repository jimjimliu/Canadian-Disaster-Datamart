## Raw input data

1, `CanadianDisasterDatabase.csv` was exported from [Canadian disaster database](https://www.publicsafety.gc.ca/cnt/rsrcs/cndn-dsstr-dtbs/index-en.aspx) , it contians instances of each individual disasters occured during past years.

2, `population.csv` was gathered manurally from a [website](https://worldpopulationreview.com/countries/cities/canada), describing the population information of each city in Canada.



## Database

1, `pysical_model` folder contains `.sql` script that creates a schema and tables for constructing a datamart.

2, `datamart` folders contians the fact table and dimention tables constructed using star schema.



## Supervised learning

`execution_output.txt` contains the runing output produced by main.py. It shows trainning and testing accuracy of different classifiers.



## Un-supervised learning

`clustering` folder contains the visulized clusters based on different features.



## Visulization

dashboard folder contains some data visulizations, describes how the data is like using several graphs.