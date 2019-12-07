from numba import jit
import pandas as pd
import numpy as n

def import_data(file):
    v = pd.read_csv(file,
                    dtype={'Price': str,
                           'Rating': str},
                    sep=',')
    replace_symbol(v)
    delete_duplicate(v)
    return v

def replace_symbol(dataset):
    replace_col = input("The column you want to replace the symbol: ")
    target_symbol = input("The symbol you want to be replaced: ")
    final_symbol = input("The symbol you want to replace: ")
    dataset[replace_col] = dataset[replace_col].str.replace(target_symbol, final_symbol)
    return dataset

def delete_duplicate (dataframe):
    dup_col = input("The column you want to drop the duplicate: ")
    dataframe.drop_duplicates(subset=dup_col, inplace=True)
    return dataframe

def combine_dataframe (dataframe1, dataframe2,frame1_col, frame2_col):
    combine_dataframe = pd.merge(dataframe1, dataframe2, left_on = frame1_col, right_on=frame2_col, how='left')
    return combine_dataframe