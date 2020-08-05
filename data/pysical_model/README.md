Using the script `pysical_model.sql` to create a database schema and tables as data mart. 

When running `main.py`, the database will be populated.

The input data for machine learning are retrieved using the following script in `physical_model.sql`. 

```sql
use disaster_DB;

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
```

