from numba import jit
import pandas as pd
import numpy as np

def import_data(file):
    with open (file, 'r') as f:
        print("Hello world!")


def replace_symbol(dataset, col_name, symbol):
    dataset[col_name] = dataset[col_name].str.replace(symbol, '')


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
        v_price=v_price.groupby('prime_genre').size()
    elif'Price' in list(v.columns):
        v['Price']=v['Price'].str.replace('$','')
        v_price=v[v['Price'] > price_num]
        v_price=v_price.groupby('Category').size()
    else:
        raise ValueError('No price information in input data,please check again..')
    return v_price

def gen_df_result(free_app_cat,paid_app_cat):
    combine = pd.DataFrame()
    combine['free']=free_app_cat
    combine['paid']=paid_app_cat
    combine['free_percentage']=(combine['free']/(combine['free']+combine['paid']))
    return combine

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

#hypothesis 2:

"""v_price=find_price(v,'0.99')
v_price
v2_price=find_price(v2,'1.99')
v2_price


#hypothesis 3:
paid_app_cat,free_app_cat=gen_cat_result(v)
v_combine=gen_df_result(free_app_cat,paid_app_cat)
paid_app_cat,free_app_cat=gen_cat_result(v2)
v2_combine=gen_df_result(free_app_cat,paid_app_cat)"""


