from numba import jit
import pandas as pd
import numpy as n

def import_file():
    Google = pd.read_csv('/Users/sophie9w9/Desktop/googleplaystore.csv',
                    dtype={'Price': str,
                           'Rating': str},
                    sep=',')
    replace_symbol(Google, 'Price', '$', '')
    Google = delete_duplicate(Google, 'App')

    Apple = pd.read_csv('/Users/sophie9w9/Desktop/AppleStore.csv',
                     dtype={'price': str,
                            'user_rating': str},
                     sep=',')
    Apple = delete_duplicate(Apple, 'track_name')

    return Google, Apple

# Use function to replace a symbol in target column to another symbol
def replace_symbol(dataset, replace_col, target_symbol, final_symbol):
    dataset[replace_col] = dataset[replace_col].str.replace(target_symbol, final_symbol)
    return dataset

# Use function to delete the duplicate rows
def delete_duplicate (dataframe, dup_col):
    dataframe.drop_duplicates(subset=dup_col, inplace=True)
    return dataframe

#Hypothesis 1: The rating will be higher if the application need be paid.
# Categorize the Apps according to free or not free. Calculate the average review rating score relatively. Compare the score to get conclusion
def Analyze_Free_rate(Google, Apple):
    Google_PriceRate = Google[['App', 'Price', 'Rating']]
    Apple_PriceRate = Apple[['track_name', 'price', 'user_rating']]
    Apple_PriceRate.columns = ['App', 'Price', 'Rating']

    All_PriceRate = pd.concat([Google_PriceRate, Apple_PriceRate])
    delete_duplicate(All_PriceRate, 'App')

    Free = All_PriceRate[All_PriceRate['Price'] == '0']
    Free[['Price', 'Rating']] = Free[['Price', 'Rating']].astype('float')
    Free_mean = round(Free['Rating'].mean(), 4)

    Not_Free = All_PriceRate[All_PriceRate['Price'] != '0']
    Not_Free[['Rating']] = Not_Free[['Rating']].astype('float')
    Not_Free_mean = round(Not_Free['Rating'].mean(), 4)

    print("Hypothesis 1: The relationship between the free and review rating score: ", "\n", "\n"
          " The average score of free Apps: ", Free_mean, "\n",
          "The average score of not free Apps: ", Not_Free_mean)


# Hypothesis 4: There is biased price in Applestore
# Find the Apps avaliable on both paltforms. Calculate the number of Apps which has higher price and which has higher review rating scores
def Analyze_same_App(Google, Apple):
    google = Google[Google['App'].isin(Apple['track_name'])]
    final_google = google[['App', 'Rating', 'Price']]
    final_google.columns = ['App', 'Google_rating', 'Google_price']

    apple = Apple[Apple['track_name'].isin(Google['App'])]
    final_apple = apple[['track_name', 'user_rating', 'price']]
    final_apple.columns = ['App_Apple', 'Apple_rating', 'Apple_price']

    combine = combine_dataframe(final_google, final_apple, 'App', 'App_Apple')

    #Compare the price of same app on different platform
    same_price = combine[combine['Google_price'] == combine['Apple_price']].shape[0]
    Google_price_higher = combine[combine['Google_price'] > combine['Apple_price']].shape[0]
    Apple_price_higher = combine[combine['Google_price'] < combine['Apple_price']].shape[0]

    #Compre the review rating score of same app on different platform
    same_rate = combine[combine['Google_rating'] == combine['Apple_rating']].shape[0]
    Google_rate_higher = combine[combine['Google_rating'] > combine['Apple_rating']].shape[0]
    Apple_rate_higher = combine[combine['Google_rating'] < combine['Apple_rating']].shape[0]

    print("\n", "\n", "Hypothesis 4: Compare same App on Google Play and Apple store: ", "\n")
    print("Name".center(20), "Same".center(30), "Google Play is Higher".center(30), "Apple Store is Higher".center(30))
    print("{:^20}{:^30}{:^30}{:^30}".format("Price", same_price, Google_price_higher, Apple_price_higher))
    print("{:^20}{:^30}{:^30}{:^30}".format("Review Rating Score", same_rate, Google_rate_higher, Apple_rate_higher))

# Use function to combine two dataframes
def combine_dataframe (dataframe1, dataframe2, frame1_col, frame2_col):
    combine_dataframe = pd.merge(dataframe1, dataframe2, left_on = frame1_col, right_on=frame2_col, how='left')
    return combine_dataframe

if __name__ == "__main__":
    import_file()
    Google,Apple=import_file()
    Analyze_Free_rate(Google, Apple)
    Analyze_same_App(Google, Apple)

