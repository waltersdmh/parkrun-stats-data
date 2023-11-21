import json


from bs4 import BeautifulSoup
import requests

#laura is more beautiful than the soup :)

# This script uses the JSON parkrun-data and scrapes event history. 
# Output to individual country files.

#parkrun events can be found on the following file.
#for now, manually copy th file content to use each refresh.
# https://images.parkrun.com/events.json


def main_function(results_url):
    print("running main function")
    headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1.1; SM-G928X Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.83 Mobile Safari/537.36'}
    run_url = results_url
    run_response = requests.get(run_url, headers=headers)
    run_soup = BeautifulSoup(run_response.text, 'html.parser')
    run_data = []

    for row in run_soup.find_all("tr", class_="Results-table-row"):
        #eventNumber = row.attrib.get("Results-table-row")
        eventNumber = row.attrs['data-parkrun']
        eventDate = row.attrs['data-date']
        finishers = row.attrs['data-finishers']
        volunteers = row.attrs['data-volunteers']

        run_data.append({"n":eventNumber,
                        "d":eventDate,
                        "f":finishers,
                        "v":volunteers}
                        )
    ##print("fetched:", run_data)
    return run_data





with open('parkrun-data.json', encoding="utf8") as user_file:
    file_contents = user_file.read()
    parsed_json = json.loads(file_contents)

    #list of countries
    countries_list = parsed_json['countries']
    #list of events
    event_list = parsed_json['events']['features']

    #for each country
    for country in countries_list:
        #if this is a country we want to do

        #23 dk
        if int(country) in [23]:
        #if True:

            #make a blank events list
            countries_list[country]['events'] = []

            # loop through all events in this country code
            for event in event_list:
                country_code = event['properties']['countrycode']
                if str(country_code) == str(country):

                    event_name = event['properties']['eventname']

                    resuls_url_start = countries_list.get(str(country_code))['url']
                    results_url = "https://"+resuls_url_start+"/"+event_name+"/results/eventhistory/"

                    event_history = []
                    try:
                        print("fetching:", event_name)
                        event_history = main_function(results_url)

                    except Exception as e:
                        print("exception", e)
                    event['eventhistory'] = event_history


                    countries_list[country]['events'].append(event)
        print("country", country)

    for country in countries_list:
        with open(str(country)+'.json', 'w') as fp:
            json.dump(countries_list[country], fp)