
create schema disaster_DB;

create table disaster_DB.date(
	date_key int,
	day int,
	month int,
	year numeric(4,0) ,
	weekend text,
	season_ca text ,
	season_intel text ,
	date text,
	primary key(date_key)
);

create table disaster_DB.location(
	location_key int,
	city text not null,
	province text not null,
	country text not null,
	canada text not null,
	primary key(location_key)
);

create table disaster_DB.disaster(
	disaster_key int,
	disaster_type text not null,
	disaster_subgroup text not null,
	disaster_group text not null,
	disaster_category text not null,
	magnitude numeric(2,1),
	utility_people_affected numeric,
	primary key(disaster_key)
);

create table disaster_DB.summary(
	description_key int,
	summary text not null,
	keyword1 text not null,
	keyword2 text not null,
	keyword3 text not null,
	primary key(description_key)
);

create table disaster_DB.costs(
	cost_key int,
	estimated_total_cost numeric,
	normalized_total_cost numeric,
	federal_payments numeric,
	provincial_payments numeric,
	provicial_dfaa_payments numeric,
	insurance_payments numeric,
	primary key(cost_key)
);

create table disaster_DB.population(
	population_key int,
	city text,
	population numeric,
	primary key(population_key)
);

create table disaster_DB.fact(
	start_date_key int not null  references disaster_DB.date(date_key),
	end_date_key int not null references disaster_DB.date(date_key),
	location_key int not null  references disaster_DB.location(location_key),
	disaster_key int not null  references disaster_DB.disaster(disaster_key),
	description_key int not null  references disaster_DB.summary(description_key),
	cost_key int not null  references disaster_DB.costs(cost_key),
	popstats_key int references disaster_DB.population(population_key),
	fatalities bigint,
	injured bigint,
	evacuated bigint
);
	


-----------------------------------------------------------------------------------------
	
-- Select out relevant columns out from the datamart

-----------------------------------------------------------------------------------------

	
use disaster_DB;

SELECT 
DI.disaster_category, DI.disaster_group,DI.disaster_subgroup,
DI.disaster_type, L.city, P.population, L.province,L.country, D.date as start_day, D.season_ca,F.fatalities,
F.evacuated, D2.date as end_day into temperate
FROM 
	fact F, location L, date D,date D2, disaster DI, summary S, costs C, population P
WHERE 
	F.start_date_key=D.date_key and F.end_date_key=D2.date_key and 
F.location_key=L.location_key and F.disaster_key=DI.disaster_key and
F.description_key=S.description_key and F.cost_key=C.cost_key and F.popstats_key=P.population_key;





















	
	