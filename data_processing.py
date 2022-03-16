'''
George Zhang
CSE 163 AD
Imports datasets needed to analyze and predict COVID cases.
'''
import geopandas as gpd
import pandas as pd


def full_name(abb):
    '''
    Given the abbreviation for a state, return its full name.
    Returns None if the abbreviation is not in the dictionary.
    '''
    states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
    }
    if abb in states:
        return states[abb]
    return None


def import_country(path):
    '''
    Returns the states geometry dataset given the filepath.
    Columns avaiable are "NAME", "CENSUSAREA", and "geometry".
    Contains only the states in the U.S. mainland.
    '''
    country = gpd.read_file(path)
    country = country[['NAME', 'CENSUSAREA', 'geometry']]
    country = country[(country['NAME'] != 'Alaska') &
                      (country['NAME'] != 'Hawaii') &
                      (country['NAME'] != 'Puerto Rico')]
    return country


def import_population(path):
    '''
    Returns the states population dataset given the filepath.
    Columns available are "NAME" and "POPESTIMATE2019".
    '''
    population = pd.read_csv(path)
    population = population[['NAME', 'POPESTIMATE2019']]
    return population


def import_vaccinations(path, state_data):
    '''
    Returns the states COVID vaccination dataset given the filepath
    and population/geometry data regarding each state.
    '''
    vaccinations = pd.read_csv(path)
    vaccinations['State'] = vaccinations['Location'].apply(full_name)
    vaccinations['Date'] = pd.to_datetime(vaccinations['Date'])
    vaccinations = state_data.merge(vaccinations, left_on='NAME',
                                    right_on='State', how='left')
    return vaccinations


def import_cases(path, state_data):
    '''
    Returns the states COVID cases dataset given the filepath
    and population/geometry data regarding each state.
    '''
    cases = pd.read_csv(path)
    cases['state'] = cases['state'].apply(full_name)
    cases['Date'] = pd.to_datetime(cases['submission_date'])
    cases = state_data.merge(cases, left_on='NAME',
                             right_on='state', how='left')
    return cases
