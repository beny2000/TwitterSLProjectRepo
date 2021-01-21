import os
import warnings
import pandas as pd
from pathlib import Path
warnings.simplefilter(action='ignore', category=Warning)

class Cleaner:
    def __init__(self, input_dir='input',
                 output_dir="output",
                 canadianLocationsFile = "list_of_municipalities_of_canada-1633j.csv"):
        self.canadianLocationsFile = os.path.abspath(Path(os.getcwd())) +"\scripts\\" + canadianLocationsFile  # "list_of_municipalities_of_canada-1633j.csv"
        self.output_path = os.path.abspath(Path(os.getcwd())) + '\\' + output_dir
        self.input_path = os.path.abspath(Path(os.getcwd())) + '\\' + input_dir
        self.__initCanadianLocations()
        self.print_console = False
        self.append_master = True

    def on_print(self):
        self.print_console = True

    def off_append(self):
        self.append_master = False

    def __initCanadianLocations(self):
        cities_reference = pd.read_csv(self.canadianLocationsFile)

        # # Convert the city names and provinces of Canada to lowercase in the reference data
        cities_reference.Provinces = cities_reference.Provinces.str.lower()
        cities_reference.Name = cities_reference.Name.str.lower()

        # To remove the single space at the beginning of strings in country column in reference data
        cities_reference['Provinces'] = cities_reference['Provinces'].str.lstrip()

        # Make a numpy array from the list of canadian cities/provinces
        Canadian_cities = cities_reference.Name.to_numpy()
        Canadian_provinces = cities_reference.Provinces.to_numpy()

        # Remove duplicates from the provinces list
        Canadian_provinces = list(dict.fromkeys(Canadian_provinces))

        # Remove single space from the provinces list
        # Canadian_provinces.remove(" ")

        # Remove nan from Canadian_provinces and Canadian_cities
        Canadian_provinces = list(filter(lambda x: str(x) != 'nan', Canadian_provinces))
        Canadian_cities = list(filter(lambda x: str(x) != 'nan', Canadian_cities))

        # add major Canadian cities to the list of provinces
        big_cities = ['toronto', 'calgary', 'ottawa', 'hamilton', 'edmonton', 'montreal', 'sherbrooke', 'newfoundland',
                      'north york',
                      'richmond hill', 'mississauga', 'vaughan', 'saskatoon', 'markham', 'kitchener', 'vancouver',
                      'guelph', 'waterloo']
        Canadian_provinces.extend(big_cities)

        # make a list of all Canadian cities and provinces
        all_reference = []
        all_reference.extend(Canadian_provinces)
        all_reference.extend(Canadian_cities)

        self.canadian_provinces = Canadian_provinces
        self.canadian_cities = Canadian_cities

        return all_reference

    def start_clean(self):
        iteration = 0
        for entry in os.listdir(self.input_path):
            print("Cleaning:", entry)
            self.clean(entry)
            iteration +=1
            print("Completed", entry, iteration, "of", len(os.listdir(self.input_path)))
            print()

    def clean(self, filename):

        def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd=" "):
            """
            Call in a loop to create terminal progress bar
            @params:
                iteration   - Required  : current iteration (Int)
                total       - Required  : total iterations (Int)
                prefix      - Optional  : prefix string (Str)
                suffix      - Optional  : suffix string (Str)
                decimals    - Optional  : positive number of decimals in percent complete (Int)
                length      - Optional  : character length of bar (Int)
                fill        - Optional  : bar fill character (Str)
                printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
            """
            percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
            filledLength = int(length * iteration // total)
            bar = fill * filledLength + '-' * (length - filledLength)
            print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
            # Print New Line on Complete
            if iteration == total:
                print()
                print()

        printProgressBar(0, 5)
        df = pd.read_csv(self.input_path + "/" + filename)
        printProgressBar(1, 5)
        # store the file name in the 'name' variable
        name = filename
        name = name.replace('.csv', '_')


        # drop unnecessary columns in data
        data = df.drop(['place', 'possibly_sensitive', 'user_created_at', 'user_default_profile_image',
                        'user_favourites_count', 'user_listed_count', 'user_name', 'user_time_zone', 'user_urls'],
                       axis='columns')

        # Remove verified Twitter accounts
        data_unverified = data.drop(data.loc[data['user_verified'] == True].index)

        # Remove non-English tweets
        data_unverified_en = data_unverified[data_unverified.lang == 'en']

        # Split city and country (province) in user_location column
        new = data_unverified_en.loc[:, 'user_location'].str.split(",", n=1, expand=True)
        # making separate city column from new data frame
        data_unverified_en.loc[:, 'city'] = new.loc[:, 0]

        # making separate country or province column from new data frame
        data_unverified_en.loc[:, 'country'] = new.loc[:, 1]

        # Convert cities and countries strings to lowercase
        data_unverified_en.loc[:, 'country'] = data_unverified_en.loc[:, 'country'].str.lower()
        data_unverified_en.loc[:, 'city'] = data_unverified_en.loc[:, 'city'].str.lower()

        printProgressBar(2, 5)
        # select the rows from 'data_unverified_en' dataset with country=='canada' or country âˆˆ 'Canadian_provinces' list,
        # or the rows with city=='canada' or city âˆˆ 'Canadian_provinces' list,
        data_unverified_en_1 = data_unverified_en[data_unverified_en['country'].isin(['canada'])
                                                  | (data_unverified_en.city == 'canada')
                                                  | data_unverified_en['city'].isin(self.canadian_provinces)
                                                  | data_unverified_en['country'].isin(self.canadian_provinces)]

        # select the rows from 'data_unverified_en' dataset with country=='ca'
        data_unverified_en_2 = data_unverified_en[data_unverified_en['country'].isin(['ca'])]

        # select the rows in 'data_unverified_en_2' dataset that their city column's values exist in
        # Canadian_cities list (we do this to make sure that 'ca' indicates 'Canada' not for example 'California' )

        data_unverified_en_ca = data_unverified_en_2[data_unverified_en_2['city'].isin(self.canadian_cities)]

        # Merge datasets to have a whole dataset of Canadian tweets
        data_unverified_en_canada = data_unverified_en_1.append(data_unverified_en_ca)

        # get a Series containing counts of cities in 'data_unverified_en_canada' dataframe
        value_counts = data_unverified_en_canada['city'].value_counts(dropna=True, sort=True)

        # Convert Pandas Series to a new dataframe
        city_val_counts = pd.DataFrame(value_counts)

        printProgressBar(3, 5)

        # change the index to the column of cities in 'city_val_counts' dataframe
        city_value_counts = city_val_counts.reset_index()
        city_value_counts.columns = ['location', 'counts']

        # Export the locations along with their tweet counts. the file has a unique name based on the input data name
        city_value_counts.to_csv(Path(self.output_path, name + 'location_counts' + '.csv'), index=False, header=True)

        ## detect retweets from the original tweets
        data_unverified_en_canada.loc[data_unverified_en_canada['text'].str.contains('RT @'), 'retweet'] = "true"
        data_unverified_en_canada['retweet'] = data_unverified_en_canada['retweet'].fillna("false")

        printProgressBar(4, 5)
        # Separate the retweets from the original tweets into two files
        data_unverified_en_canada_original = data_unverified_en_canada[data_unverified_en_canada['retweet'] == "false"]
        data_unverified_en_canada_retweet = data_unverified_en_canada[data_unverified_en_canada['retweet'] == "true"]
        data_unverified_en_canada_original = data_unverified_en_canada_original.drop(['retweet'], axis='columns')
        data_unverified_en_canada_retweet = data_unverified_en_canada_retweet.drop(['retweet'], axis='columns')


        # print the first rows of both output datasets as well as their size
        def p(name, data_unverified_en_canada_original, data_unverified_en_canada_retweet):
            print("name=", name)
            print("data_unverified_en_canada_original=\n", data_unverified_en_canada_original.head())
            print("data_unverified_en_canada_retweet=\n", data_unverified_en_canada_retweet.head())
            print("data_unverified_en_canada_original size=", data_unverified_en_canada_original.shape)
            print("data_unverified_en_canada_retweet size=", data_unverified_en_canada_retweet.shape)


        # Export final datasets (original and retweet) with unique names containing input data name (e.g. Oct1full_original.csv)
        # using p and name variables
        data_unverified_en_canada_original.to_csv(Path(self.output_path, name + 'tweets_cleaned' + '.csv'), index=False)
        data_unverified_en_canada_retweet.to_csv(Path(self.output_path, name + 'retweet_cleaned' + '.csv'), index=False)

        if self.append_master:
            data_unverified_en_canada_original.to_csv(Path(self.output_path,'all_tweets_cleaned' + '.csv'),
                                                      index=False, mode='a')
            data_unverified_en_canada_retweet.to_csv(Path(self.output_path, 'all_retweet_cleaned' + '.csv'),
                                                     index=False, mode='a')
        printProgressBar(5, 5)
        if self.print_console: p(name, data_unverified_en_canada_original, data_unverified_en_canada_retweet)
