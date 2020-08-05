import os

# Value substituted for unknown metric
UNKNOWN_METRIC = 'unknown'

# List of all provinces and territories in Canada
ALL_CA_PROVINCES = [
    ('ON', 'Ontario'),
    ('QC', 'Quebec'),
    ('QC', 'Québec'),
    ('NS', 'Nova Scotia'),
    ('NB', 'New Brunswick'),
    ('MB', 'Manitoba'),
    ('BC', 'British Columbia'),
    ('PE', 'Prince Edward Island'),
    ('SK', 'Saskatchewan'),
    ('AB', 'Alberta'),
    ('NL', 'Newfoundland and Labrador'),
    # Territories
    ('NT', 'Northwest Territories'),
    ('YT', 'Yukon'),
    ('NU', 'Nunavut')
    ]

# dictionary to store province name as keys, and main city as values
province_dic = {
    'Alberta': 'Edmonton',
    'Saskatchewan': 'Regina',
    'Manitoba': 'Winnipeg',
    'New Brunswick': 'Fredericton',
    'Nova Scotia': 'Halifax',
    'Prince Edward Island': 'Charlottetown',
    'Newfoundland and Labrador': 'St. Johns',
    'Ontario': 'Toronto',
    'Quebec': 'Quebec City',
    'Québec': 'Quebec City',
    'British Columbia': 'Victoria',
    'Northwest Territories': 'Northwest Territories',
    'Yukon': 'Yukon',
    'Nunavut': 'Nunavut'
}

province_code_dic={
    'AB': 'Edminton',
    'SK': 'Regina',
    'MB': 'Winnipeg',
    'NB': 'Fredericton',
    'NS': 'Halifax',
    'PEI': 'Charlottetown',
    'PE': 'Charlottetown',
    'NL': 'St. Johns',
    'ON': 'Toronto',
    'QC': 'Quebec City',
    'BC': 'Victoria',
    'NT': 'Northwest Territories',
    'YT': 'Yukon',
    'NU': 'Nunavut',
}

# Special locations
CA_REGIONS = {
    'Prairie Provinces': ['Alberta', 'Saskatchewan', 'Manitoba'],
    'Prairies': ['Alberta', 'Saskatchewan', 'Manitoba'],
    'Maritime Provinces': ['New Brunswick', 'Nova Scotia', 'Prince Edward Island'],
    'Maritime provinces': ['New Brunswick', 'Nova Scotia', 'Prince Edward Island'],
    'Maritimes': ['New Brunswick', 'Nova Scotia', 'Prince Edward Island'],
    'Martime provinces': ['New Brunswick', 'Nova Scotia', 'Prince Edward Island'],
    'Martime Provinces': ['New Brunswick', 'Nova Scotia', 'Prince Edward Island'],
    'Newfoundland': ['Newfoundland and Labrador'],
    'Labrador': ['Newfoundland and Labrador'],
    'Across Canada': ['Alberta','Saskatchewan','Manitoba','New Brunswick','Nova Scotia','Prince Edward Island',
                     'Newfoundland and Labrador','Ontario', 'Quebec','British Columbia','Northwest Territories',
                      'Yukon','Nunavut'],
    'Eastern Canada': ['New Brunswick', 'Newfoundland and Labrador', 'Nova Scotia',
                       'Ontario', 'Prince Edward Island', 'Quebec'],
   'Western Canada': ['Alberta', 'British Columbia', 'Manitoba', 'Saskatchewan'],
   'St. Lawrence River': ['Ontario', 'Quebec'],
   'Atlantic Canada': ['New Brunswick', 'Newfoundland and Labrador', 'Nova Scotia', 'Prince Edward Island']
}

# List of stop words which are not considered as keywords
STOP_WORDS = set(["", "a", "about", "above", "above", "across", "after",
                 "afterwards", "again", "against", "all", "almost",
                 "alone", "along", "already", "also","although","always",
                 "am","among", "amongst", "amoungst", "amount",  "an",
                 "and", "another", "any","anyhow","anyone","anything",
                 "anyway", "anywhere", "are", "around", "as",  "at",
                 "back","be","became", "because","become","becomes",
                 "becoming", "been", "before", "beforehand", "behind",
                 "being", "below", "beside", "besides", "between",
                 "beyond", "bill", "both", "bottom","but", "by", "call",
                 "can", "cannot", "cant", "co", "con", "could", "couldnt",
                 "cry", "de", "describe", "detail", "do", "done", "down",
                 "due", "during", "each", "eg", "eight", "either",
                 "eleven","else", "elsewhere", "empty", "enough", "etc",
                 "even", "ever", "every", "everyone", "everything",
                 "everywhere", "except", "few", "fifteen", "fify", "fill",
                 "find", "fire", "first", "five", "for", "former",
                 "formerly", "forty", "found", "four", "from", "front",
                 "full", "further", "get", "give", "go", "had", "has",
                 "hasnt", "have", "he", "hence", "her", "here", "hereafter",
                 "hereby", "herein", "hereupon", "hers", "herself", "him",
                 "himself", "his", "how", "however", "hundred", "ie",
                 "if", "in", "inc", "indeed", "interest", "into", "is",
                 "it", "its", "itself", "keep", "last", "latter", "latterly",
                 "least", "less", "ltd", "made", "many", "may", "me",
                 "meanwhile", "might", "mill", "mine", "more", "moreover",
                 "most", "mostly", "move", "much", "must", "my", "myself",
                 "name", "namely", "neither", "never", "nevertheless",
                 "next", "nine", "no", "nobody", "none", "noone", "nor",
                 "not", "nothing", "now", "nowhere", "of", "off", "often",
                 "on", "once", "one", "only", "onto", "or", "other",
                 "others", "otherwise", "our", "ours", "ourselves", "out",
                 "over", "own","part", "per", "perhaps", "please", "put",
                 "rather", "re", "same", "see", "seem", "seemed",
                 "seeming", "seems", "serious", "several", "she",
                 "should", "show", "side", "since", "sincere", "six",
                 "sixty", "so", "some", "somehow", "someone",
                 "something", "sometime", "sometimes", "somewhere",
                 "still", "such", "system", "take", "ten", "than",
                 "that", "the", "their", "them", "themselves", "then",
                 "thence", "there", "thereafter", "thereby", "therefore",
                 "therein", "thereupon", "these", "they", "thickv", "thin",
                 "third", "this", "those", "though", "three", "through",
                 "throughout", "thru", "thus", "to", "together", "too",
                 "top", "toward", "towards", "twelve", "twenty", "two",
                 "un", "under", "until", "up", "upon", "us", "very", "via",
                 "was", "we", "well", "were", "what", "whatever", "when",
                 "whence", "whenever", "where", "whereafter", "whereas",
                 "whereby", "wherein", "whereupon", "wherever", "whether",
                 "which", "while", "whither", "who", "whoever", "whole",
                 "whom", "whose", "why", "will", "with", "within",
                 "without", "would", "yet", "you", "your", "yours",
                 "yourself", "yourselves", "the"])

# prepositions in place description
PLACE_PREPOSITIONS = ("to", "of")

# missing values
MISSINGVALUE = None;

# Value substituted for unknown attribute
MISSINGDATE = 'unknown'

OUTPUT_DIR = os.path.join(os.getcwd(), 'data' ,'datamart')
INPUT_SOURCE_FILE = os.path.join(os.getcwd(), 'data', 'CanadianDisasterDatabase.csv')
population_file = os.path.join(os.getcwd(), 'data','population.csv')

DB_SCHEMA = [
    '''create schema disaster_DB;''',
    """
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
    );""",
    """
    create table disaster_DB.location(
        location_key int,
        city text not null,
        province text not null,
        country text not null,
        canada text not null,
        primary key(location_key)
    );""",
    """
        create table disaster_DB.disaster(
        disaster_key int,
        disaster_type text not null,
        disaster_subgroup text not null,
        disaster_group text not null,
        disaster_category text not null,
        magnitude numeric(2,1),
        utility_people_affected numeric,
        primary key(disaster_key)
    );""",
    """
    create table disaster_DB.summary(
        description_key int,
        summary text not null,
        keyword1 text not null,
        keyword2 text not null,
        keyword3 text not null,
        primary key(description_key)
    );""",
    """
    create table disaster_DB.costs(
        cost_key int,
        estimated_total_cost numeric,
        normalized_total_cost numeric,
        federal_payments numeric,
        provincial_payments numeric,
        provicial_dfaa_payments numeric,
        insurance_payments numeric,
        primary key(cost_key)
    );""",
    """
    create table disaster_DB.population(
        population_key int,
        city text,
        population numeric,
        primary key(population_key)
    );""",
    """
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
    );"""
]





















