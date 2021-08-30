import replit
import json
import requests
import pandas as pd
import pygal
import pprint
import geopandas as gpd
import country_converter as coco
import csv
from dateutil import rrule
from datetime import date
from IPython.display import SVG

print('Starting to analyze Wikipedia...')

# Important: update pygal's map: https://github.com/Kozea/pygal_maps_world/pull/5

# Function used below to display maps
def display_svg(svg_code):
     return SVG(svg_code)

pp = pprint.PrettyPrinter(indent=4)

# As specified there: https://wikimedia.org/api/rest_v1/#/
# Without your contact details you'll get an error
contact_details = 'a455bcd9 on Wikipedia / @ADssx on Twitter'
headers = {
    'User-Agent': contact_details
}

# Get all projects from the Wikimedia Foundation
projects_list_url = 'https://commons.wikimedia.org/w/api.php?action=sitematrix&smtype=language&format=json'
projects_list_json = requests.get(projects_list_url, headers=headers).text

projects = json.loads(projects_list_json)

wiki_codes = []
id = 0

# Look the whole list
for i in projects['sitematrix']:
    # Only fetch dictionnaries
    if isinstance(projects['sitematrix'][i],dict):
        # Get the language code
        code = projects['sitematrix'][i]['code']
        
        # Avoid issue with classical orthography Belarusian Wikipedia
        if code == 'be-x-old':
            continue

        # For each language, look at all different projects
        for j in projects['sitematrix'][i]['site']:
            # If the project is a Wikipedia, add the language code to the list of Wikipedias
            if j['code'] == 'wiki':
                wiki_codes += [code]

# For testing purposes
test_mode = False
if test_mode:
    # Set to have unique languade codes in case there's a mistake in the list
    wiki_codes = set(['ary', 'en', 'ja', 'es', 'de', 'ru', 'fr', 'it', 'zh', 'pt', 'pl', 'tr', 'ko', 'ar', 'arz', 'nl', 'he', 'fa', 'id', 'hi'])
    # wiki_codes = ['fr', 'de']
    # Languages of India
    # wiki_codes = ['en', 'hi', 'ta', 'mr', 'ml', 'te', 'bn', 'kn', 'simple', 'gu']

print('Analysis of', len(wiki_codes), 'Wikipedias')

analyze_last_month = True
if analyze_last_month:
    # By default, use the last month
    today = date.today()

    year = today.year
    month = today.month - 1

    # Special case for January
    if today.month == 1:
        year = year - 1
        month = 12

    last_month = date(year, month, 1)
else:
    # Pick any other month
    last_month = date(2021, 1, 1)

# Convert to string to add to URL
point_in_time = last_month.strftime('%Y/%m')

print('Analyzed period:', point_in_time)

# For each Wikipedia, get the number of page views in the analyzed month, by country

# API example: https://wikimedia.org/api/rest_v1/metrics/pageviews/top-by-country/fr.wikipedia/all-access/2021/01
base_url = 'https://wikimedia.org/api/rest_v1/metrics/pageviews/top-by-country/'
complement = '/all-access/'

all_wikipedias = pd.DataFrame()
    
# Create empty DataFrame
all_languages_pageviews = pd.DataFrame()

# For each Wikipedia get the list of page views by country
for code in wiki_codes:
    project = code + '.wikipedia.org'
    
    # Fetch API
    countries_url = base_url + project + complement + point_in_time
    countries_json = requests.get(countries_url, headers=headers).text
    countries = json.loads(countries_json)
    
    # If there's no data for this language, continue to the next one
    if 'items' not in countries:
        continue

    # Transform to a dataframe
    df = pd.DataFrame.from_dict(countries['items'][0]['countries'])

    # Drop useless columns
    df = df.drop(columns=['views', 'rank'])

    # Rename one column
    df = df.rename(columns={'views_ceil': code})
    
    # Set the country code as index
    df = df.set_index('country')

    # Merging the dataframes on the country key with outer join
    all_wikipedias = pd.concat([all_wikipedias, df], axis=1)

    country_code = 'MA'
popular_wikipedias_in_country = all_wikipedias.loc[country_code].sort_values(ascending=False)
print('\nMost popular Wikipedias in', country_code, 'in', last_month, ':')
# Only print the top 10
print(popular_wikipedias_in_country[0:10])

# Same but in %
popular_wikipedias_in_country_pct = (100. * popular_wikipedias_in_country / popular_wikipedias_in_country.sum()).round(1)
print('\nMost popular Wikipedias in', country_code, ', %:')
# Only print the top 10
print(popular_wikipedias_in_country_pct[0:10])

# Get the most popular Wikipedia by country
most_popular_by_country = all_wikipedias.idxmax(axis=1)

# Add back the index
most_popular_by_country = most_popular_by_country.reset_index()
index = 'index'
most_popular_by_country = most_popular_by_country.rename(columns={"country": index}, errors="raise")

# Rename the column
most_popular_by_country = most_popular_by_country.rename(columns={0: 'most_popular'})

# Number of countries where each edition is top
popular_wikipedias = most_popular_by_country.groupby(['most_popular']).count()
# Sort by number of countries where language is first
popular_wikipedias = popular_wikipedias.sort_values(by=[index], ascending=False)

# Languages that are number one in at least one country
top_languages = set(most_popular_by_country['most_popular'])
print('\n', len(top_languages), 'languages are first in at least one country or territory:')
print(top_languages)

# Names of countries where each edition arrives first
# We concatenate country codes
# https://stackoverflow.com/a/22221675/5285608
countries_by_language = most_popular_by_country.groupby('most_popular')[index].apply(list).to_dict()