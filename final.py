from numba import jit
import pandas as pd
import numpy as np

def import_file():
    """
    This function explores the csv file by pd.readcsv() and did some basic data cleaning for further analysis
    :return:
    """
    Google = pd.read_csv('/Users/ss/Desktop/GA/course/IS590/final_projects/googleplaystore.csv',
                    dtype={'Price': str,
                           'Rating': str},
                    sep=',')
    replace_symbol(Google, 'Price', '$', '')
    Google = delete_duplicate(Google, 'App')

    Apple = pd.read_csv('/Users/ss/Desktop/GA/course/IS590/final_projects/AppleStore.csv',
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

#hypo 2:For those apps higher than normal price in the store($0.99), they fall into a specific genre.
def find_price(v:pd.core.frame.DataFrame,price_num:str)->pd.core.series.Series:
    """
    This function asks the user to decide the minimum price for each app to count, then parse the dataframe object,
    return a series object result, which contains information of category name and its app number
    :param v: dataframe object which needs to be parsed to find the numbers of apps under each category
    with price bigger than the price_num value
    :param price_num: the specific value where user applies to filter the minimum price to count
    :return:the number of apps under each category whith its price bigger than price_num value
    >>> d={'prime_genre':['yellow','green','red','yellow','green','yellow'],'price':['3','6','8','3','2','7']}
    >>> v=pd.DataFrame(data=d)
    >>> price_num='4'
    >>> find_price(v,price_num)
    prime_genre
    green     1
    red       1
    yellow    1
    dtype: int64
    >>> d={'prime_genre':['yellow','green','red','yellow','green','yellow'],'number':['3','6','8','3','2','7']}
    >>> v=pd.DataFrame(data=d)
    >>> price_num='4'
    >>> find_price(v,price_num)
    Traceback (most recent call last):
    ValueError: No price information in input data,please check again..
    """
    if 'price' in list(v.columns):
        v_price=v[v['price'] > price_num]
        v_price=v_price.groupby('prime_genre').size().sort_values(ascending=False)
    elif'Price' in list(v.columns):
        v_price=v[v['Price'] > price_num]
        v_price=v_price.groupby('Category').size().sort_values(ascending=False)
    else:
        raise ValueError('No price information in input data,please check again..')
    return v_price

#hypo3:The proportion of free apps in each categroy is higher than paid apps.
def gen_cat_result(v):
    if 'Type' in list(v.columns):
        free_app = v[v['Type'] == 'Free']
        paid_app = v[v['Type'] == 'Paid']
        free_app_cat = free_app.groupby('Category').size()
        paid_app_cat = paid_app.groupby('Category').size()
        paid_app_cat = paid_app_cat.fillna(0)
    elif 'price' in list(v.columns):
        free_app = v[v['price'] == '0']
        paid_app = v[v['price'] != '0']
        free_app_cat = free_app.groupby('prime_genre').size()
        paid_app_cat = paid_app.groupby('prime_genre').size()
    else:
        raise ValueError('No payment information in input data,please check again...')
    return paid_app_cat,free_app_cat


def gen_df_result(free_app_cat,paid_app_cat):
    combine = pd.DataFrame()
    combine['free']=free_app_cat
    combine['paid']=paid_app_cat
    combine['free_percentage']=(combine['free']/(combine['free']+combine['paid']))
    combine['free_percentage'] = round(combine['free_percentage'], 4)
    combine=combine.sort_values(by='free_percentage',ascending=False)
    return combine



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

    # Hypothesis 1
    Analyze_Free_rate(Google, Apple)

    #hypothesis 2:
    Google_price=find_price(Google,'0.99')
    print('Hypothesis 2:For those apps higher than normal price in the store($0.99), they fall into a specific genre.\n','Google result\n',Google_price)
    Apple_price=find_price(Apple,'0.99')
    print('Hypothesis 2:For those apps higher than normal price in the store($0.99), they fall into a specific genre.\n','Apple Result\n',Apple_price)

    #hypothesis 3:
    paid_app_cat,free_app_cat=gen_cat_result(Google)
    Google_combine=gen_df_result(free_app_cat,paid_app_cat)
    print('Hypothesis 3:The proportion of free apps in each categroy is higher than paid apps.\n','Google result\n',Google_combine)
    paid_app_cat,free_app_cat=gen_cat_result(Apple)
    Apple_combine=gen_df_result(free_app_cat,paid_app_cat)
    print('Hypothesis 3:The proportion of free apps in each categroy is higher than paid apps.\n','Apple result\n',Apple_combine)

    #Hypothesis 4
    Analyze_same_App(Google, Apple)


