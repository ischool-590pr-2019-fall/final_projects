from numba import jit
import pandas as pd
import numpy as n

def import_data(file):
    with open (file, 'r') as f:
        print("Hello world!")


def replace_symbol(dataset, col_name, symbol):
    dataset[col_name] = dataset[col_name].str.replace(symbol, '')


