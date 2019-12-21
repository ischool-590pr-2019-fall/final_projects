import pandas as pd
import numpy as np
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image
import seaborn as sns
from matplotlib.pyplot import MultipleLocator
import time



def replace_symbol(dataset, replace_col, target_symbol, final_symbol):
    """
        Use function to replace a symbol in target column to another symbol
        :param dataset: The dataset we want to replace the symbol
        :param replace_col: The specific column we want to replcace
        :param target_symbol: The initial symbol will be replcaed
        :param final_symbol: The final symbol replace the initial symbol
        :return: the dataset after replaced

        >>> d={'student':['%Amy','%Sophie','%Zoe','%Ben','%Kelley'],'number':['$1','2','$3','$4','5']}
        >>> dataset=pd.DataFrame(data=d)
        >>> replace_symbol(dataset, 'student', '%', '')
          student number
        0     Amy     $1
        1  Sophie      2
        2     Zoe     $3
        3     Ben     $4
        4  Kelley      5

        >>> replace_symbol(dataset, 'number', '$', '')
          student number
        0     Amy      1
        1  Sophie      2
        2     Zoe      3
        3     Ben      4
        4  Kelley      5
        """
    dataset[replace_col] = dataset[replace_col].str.replace(target_symbol, final_symbol)
    return dataset


def delete_duplicate (dataframe, dup_col):
    """
        Use function to delete the duplicate rows
        :param dataframe: The dataframe we want to delete duplicate rows
        :param dup_col: The specific colunmn we want to delete dupilicate items
        :return: The dataframe after dropping duplucate items

        >>> d={'fruit':['apple','banana','orange','orange','pear', 'orange'],'price':['$1','$3','$3','$4','$5','$6']}
        >>> dataframe=pd.DataFrame(data=d)
        >>> delete_duplicate(dataframe, 'fruit')
            fruit price
        0   apple    $1
        1  banana    $3
        2  orange    $3
        4    pear    $5

        >>> delete_duplicate(dataframe, 'price')
            fruit price
        0   apple    $1
        1  banana    $3
        4    pear    $5
        """
    dataframe.drop_duplicates(subset=dup_col, inplace=True)
    return dataframe


#Hypothesis 3: The rating will be higher if the application need be paid.
def Analyze_Free_rate(Google, Apple):
    """
    Categorize the Apps according to free or not free. Calculate the average review rating score relatively. Compare the score to get conclusion
    :param Google: The Google Play dataset
    :param Apple: The Apple Store dataset

    >>> google = {'App':['a','b','c','d','e','f'],'Price':['0','6','8','0','2','7'], 'Rating':['1','2','3','4','5','6']}
    >>> g = pd.DataFrame(data=google)
    >>> apple = {'track_name':['b','e','f','g','q','z'],'price':['1','2','6','0','3','9'], 'user_rating':['9','8','7','6','5','4']}
    >>> a = pd.DataFrame(data=apple)
    >>> Analyze_Free_rate(g, a)
    Hypothesis 3: The relationship between the free and review rating score:
    <BLANKLINE>
     The average score of free Apps:  3.6667
     The average score of not free Apps:  4.1667
    """
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

    print("Hypothesis 3: The relationship between the free and review rating score: ", "\n", "\n"
          " The average score of free Apps: ", Free_mean, "\n",
          "The average score of not free Apps: ", Not_Free_mean)

#Hypothesis 5:For those apps higher than normal price in the store($0.99), Game ranks the first in terms of category percentage.
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

#Hypothesis 6:The proportion of free apps in each categroy is higher than paid apps.
def gen_cat_result(v:pd.core.frame.DataFrame)->pd.core.series.Series:
    """
    This function takes the original dataframe object and then find the number of free and non-free apps under each category
    Attention: to avoid the confusing output where the number of apps become floating number is there is NAN value,
    we apply the astype('Int64')-->New... Int64 with NaN support!
    :param v: the dataframe object to be parsed in find the catefory information
    :return: two Series object contains the number of free and non-free apps
    >>> d={'prime_genre':['red','red','red','yellow','green','yellow'],'price':['0','6','0','3','6','7']}
    >>> v=pd.DataFrame(data=d)
    >>> gen_cat_result(v)
    (prime_genre
    green     1
    red       1
    yellow    2
    dtype: Int64, prime_genre
    red    2
    dtype: Int64)
    """
    if 'Type' in list(v.columns):
        free_app = v[v['Type'] == 'Free']
        paid_app = v[v['Type'] == 'Paid']
        free_app_cat = free_app.groupby('Category').size().astype('Int64')
        paid_app_cat = paid_app.groupby('Category').size().astype('Int64')
        paid_app_cat = paid_app_cat.fillna(0)
    elif 'price' in list(v.columns):
        free_app = v[v['price'] == '0']
        paid_app = v[v['price'] != '0']
        free_app_cat = free_app.groupby('prime_genre').size().astype('Int64')
        paid_app_cat = paid_app.groupby('prime_genre').size().astype('Int64')
    else:
        raise ValueError('No payment information in input data,please check again...')
    return paid_app_cat,free_app_cat


def gen_df_result(free_app_cat:pd.core.series.Series,paid_app_cat:pd.core.series.Series)->pd.core.frame.DataFrame:
    """
    generate a dataframe object based on the payment information of apps, first column is the category name,
    then the next two columns contain the number of  free apps and paid apps, the last column contains the free percentage
    :param free_app_cat:a pandas series object which contains the number of free apps under each category
    :param paid_app_cat:a pandas series object which contains the number of non-free apps under each category
    :return:a dataframe object contains gateory and its corresponding
    >>> free_app_cat=pd.Series([2,3])
    >>> paid_app_cat=pd.Series([4,6])
    >>> gen_df_result(free_app_cat,paid_app_cat)
       free  paid  free_percentage
    0     2     4           0.3333
    1     3     6           0.3333
    """
    combine = pd.DataFrame()
    combine['free']=free_app_cat
    combine['paid']=paid_app_cat
    combine=combine.fillna(0)
    combine['free_percentage']=(combine['free']/(combine['free']+combine['paid']))
    combine['free_percentage'] = round(combine['free_percentage'], 4)
    combine=combine.sort_values(by='free_percentage',ascending=False)
    return combine



# Hypothesis 4: There is biased price in Applestore
def Analyze_same_App(Google, Apple):
    """
    Find the Apps avaliable on both paltforms. Calculate the number of Apps which has higher price and which has higher review rating scores
    :param Google: The Google Play dataset
    :param Apple: The Apple Store dataset

    >>> google = {'App':['a','b','c','d','e','f'],'Price':['$3','$6','$8','$3','$2','$7'], 'Rating':['1','2','3','4','5','6']}
    >>> g = pd.DataFrame(data=google)
    >>> apple = {'track_name':['b','e','f','g','q','z'],'price':['$1','$2','$6','$4','$3','$9'], 'user_rating':['9','8','7','6','5','4']}
    >>> a = pd.DataFrame(data=apple)
    >>> Analyze_same_App(g, a)
    <BLANKLINE>
    <BLANKLINE>
     Hypothesis 4: Compare same App on Google Play and Apple store:
    <BLANKLINE>
            Name                      Same                  Google Play is Higher          Apple Store is Higher
           Price                      1                             2                             0
    Review Rating Score               0                             0                             3
    """
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



def combine_dataframe (dataframe1, dataframe2, frame1_col, frame2_col):
    """
        Use function to combine two dataframes
        :param dataframe1: The first dataframe we want o combine
        :param dataframe2: The second dataframe we want to combine
        :param frame1_col: The column in first dataframe we want to combine with
        :param frame2_col: The column in second dataframe we want to combine with first dataframe
        :return: A dataframe after the combination

        >>> d1={'fruit':['apple','banana','orange','pear','tomato','blueberry'],'price':['$1','$2','$3','$4','$5','$6']}
        >>> dataframe1=pd.DataFrame(data=d1)
        >>> d2 = {'fruit':['apple','banana','orange','pear','tomato','blueberry'],'color':['red','yellow','orange','yelloe','red','blue']}
        >>> dataframe2=pd.DataFrame(data=d2)
        >>> combine_dataframe(dataframe1, dataframe2, 'fruit', 'fruit')
               fruit price   color
        0      apple    $1     red
        1     banana    $2  yellow
        2     orange    $3  orange
        3       pear    $4  yelloe
        4     tomato    $5     red
        5  blueberry    $6    blue
        """
    combine_dataframe = pd.merge(dataframe1, dataframe2, left_on = frame1_col, right_on=frame2_col, how='left')
    return combine_dataframe

# Hypothsis 1:People are not satisfied with the app will be more likely to publish the reviews
def addPropColumn(origin, numerator, deno, dirtyL):
    '''
    given a dataframe, add a new column whose value is the one column divided by the other column. Before division, we do data cleaning based on a list of strings which are the thing we want to strip
    :param origin: original dataframe with 2 columns
    :param numerator: the column name of the numerator
    :param deno: the column name of the denominator
    :param dirtyL: a list of strings which are the thing we want to strip
    :return: no return, modify the original dataframe
    >>> data = {'a':['1,000', '2,000'], 'b':['10+', '100+']}
    >>> df = pd.DataFrame(data)
    >>> addPropColumn(df, 'b', 'a', ['+', ','])
    >>> df['Proportion'][0]
    0.01
    >>> df['Proportion'][1]
    0.05
    '''
    # clean the dirty strings and change the data type of string to numberic
    if origin[numerator].dtype == 'O':
        for string in dirtyL:
            origin[numerator] = origin[numerator].str.replace(string, '')
        origin[numerator] = pd.to_numeric(origin[numerator])

    if origin[deno].dtype == 'O':
        for string in dirtyL:
            origin[deno] = origin[deno].str.replace(string, '')
        origin[deno] = pd.to_numeric(origin[deno])


    prop = origin[numerator] / origin[deno]
    origin['Proportion'] = prop



# Hypothesis 2 Part I:words frequency among all apps
def getFreq(df, colname):
    '''
    given a dataframe and a column name in it, get the word frequency of the column, regardless of upper and lower letter
    :param df: dataframe
    :param colname: colmun name
    :return: a dictionary of frequency, key is the word, value is the frequency it appears in the dataframe
    >>> data = {'sentence':['apple ! juice', 'Apple&:cider?','cider']}
    >>> df = pd.DataFrame(data)
    >>> dic = getFreq(df, 'sentence')
    >>> dic['apple']
    2
    >>> dic['cider']
    2
    '''
    s = r'[\s\,\;\(\)\.\&\!\:\?]+'
    mylist = list(df[colname])
    mydic = {}
    for i in mylist:
        #     print(type(i))

        sentence = re.split(s, str(i))
        for j in sentence:
            mydic[j.lower()] = mydic.get(j.lower(), 0) + 1

    return mydic

#Hypothesis 2 Part III:a closer look in terms of positive/negative/netural comments
def import_review():
    """
    Import the review data and split it to list and dictionaries
    :return: The Google review details dataset
    """
    with open('googleplaystore_user_reviews.csv', 'r') as f:
        Review = []  # final output

        for line in f:
            values_on_line = line.split(',')

            Review.append({})
            tempdic = Review[-1]  # temporary dictionary for all of the data
            tempdic["App"] = values_on_line[0]
            #Split the review to words
            word = values_on_line[1].split(' ')
            tempdic["Trans_Review"] = word
            tempdic["Sentiment"] = values_on_line[2]
            tempdic["Senti_Polarity"] = values_on_line[3]
            tempdic["Senti_Subjectibe"] = values_on_line[4]

    return Review



def Count_words(Review, search_word, sentiment):
    """
    Count the number of an word under different sentiment
    :param Review: The Google review details which arrange in a list
    :param search_word: The word we want to count the frequency of apperance
    :param sentiment: The sentiment we want to check
    :return: The number of apperance for the word

    >>> Rev = [{"Trans_Review": ['1', '2', '3', '4'], "Sentiment": 'Positive'}, {"Trans_Review": ['1', '1', '3', '5'], "Sentiment": 'Positive'}, {"Trans_Review": ['0', '1', '3', '5'], "Sentiment": 'Negative'}]
    >>> Count_words(Rev, '1', 'Positive')
    2

    >>> Count_words(Rev, '1', 'Negative')
    1

    >>> Count_words(Rev, '5', 'Positive')
    1
    """
    count = 0
    for i in range(0, len(Review)):
        if search_word in Review[i]["Trans_Review"] and Review[i]["Sentiment"] == sentiment:
            count += 1

    return count


def Count_senti(Review):
    """
    Count the total number of comments under different sentiment
    :param Review: The review details dataset
    :return: The total number of comments under respectively different sentiment

    >>> Rev = [{"Trans_Review": ['1', '2', '3', '4'], "Sentiment": 'Positive'}, {"Trans_Review": ['1', '1', '3', '5'], "Sentiment": 'Positive'}, {"Trans_Review": ['0', '1', '3', '5'], "Sentiment": 'Negative'}]
    >>> Count_senti(Rev)
    (2, 1, 0)
    """
    count_P = 0
    count_N = 0
    count_Netr = 0
    for i in range(0, len(Review)):
        if Review[i]["Sentiment"] == "Positive":
            count_P += 1
        if Review[i]["Sentiment"] == "Negative":
            count_N += 1
        if Review[i]["Sentiment"] == "Neutral":
            count_Netr += 1
    return count_P, count_N, count_Netr


def Analyze_Review(Review):
    """
    Analyze the frequency of a specific word under different sentiment
    :param Review: The review details dataset

    >>> Rev = [{"Trans_Review": ['I', 'like', 'it'], "Sentiment": 'Positive'}, {"Trans_Review": ['I', 'love', 'it'], "Sentiment": 'Positive'}, {"Trans_Review": ['I', 'do','not', 'like', 'it'], "Sentiment": 'Negative'}, {"Trans_Review": ['I', 'may', 'like', 'it'], "Sentiment": 'Neutral'}]
    >>> Analyze_Review(Rev)
    The word 'like' appears  1  times in positive comments. The percentage is  0.5
    The word 'like' appears  1  times in negative comments. The percentage is  1.0
    The word 'like' appears  1  times in neutral comments. The percentage is  1.0
    """
    word_like_P = Count_words(Review, "like", "Positive")
    word_like_N = Count_words(Review, "like", "Negative")
    word_like_Netr = Count_words(Review, "like", "Neutral")

    count_P, count_N, count_Netr = Count_senti(Review)
    Percent_P = round(word_like_P / count_P, 4)
    Percent_N = round(word_like_N/ count_N, 4)
    Percent_Netr = round(word_like_Netr/count_Netr, 4)

    print("The word 'like' appears ", word_like_P, " times in positive comments. The percentage is ", Percent_P)
    print("The word 'like' appears ", word_like_N, " times in negative comments. The percentage is ", Percent_N)
    print("The word 'like' appears ", word_like_Netr, " times in neutral comments. The percentage is ", Percent_Netr)

    while True:
        result = input("Find the words? (y/n): ")
        print()
        if result.lower() == "y":
            word_input = input("Enter the word you want to count: ")
            count_input_P = Count_words(Review, word_input, "Positive")
            count_input_N = Count_words(Review, word_input, "Negative")
            count_input_Netr = Count_words(Review, word_input, "Neutral")
            input_percent_P = round(count_input_P / count_P, 4)
            input_percent_N = round(count_input_N / count_N, 4)
            input_percent_Netr = round(count_input_Netr / count_Netr, 4)
            print("The word", word_input, "appears ", count_input_P, " times in positive comments. The percentage is ", input_percent_P)
            print("The word", word_input, "appears ", count_input_N, " times in negative comments. The percentage is ", input_percent_N)
            print("The word", word_input, "appears ", count_input_Netr, " times in neutral comments. The percentage is ", input_percent_Netr)
        else:
            break

if __name__ == "__main__":
    start_time=time.time()
    Google = pd.read_csv('googleplaystore.csv',
                         dtype={'Price': str,
                                'Rating': str},
                         sep=',')
    replace_symbol(Google, 'Price', '$', '')
    Google = delete_duplicate(Google, 'App')

    Apple = pd.read_csv('AppleStore.csv',
                        dtype={'price': str,
                               'user_rating': str},
                        sep=',')
    Apple = delete_duplicate(Apple, 'track_name')

    Google_review = pd.read_csv('googleplaystore_user_reviews.csv',
                                )

    # Hypothesis 3
    Analyze_Free_rate(Google, Apple)

    #hypothesis 5
    Google_price=find_price(Google,'0.99')
    print('Hypothesis 5:For those apps higher than normal price in the store($0.99), they fall into the Game category.\n','Google result\n',Google_price)
    # data visualizaiton
    Google_plot = Google_price.plot(title='Google Play Store\nApp category for Prices of apps higher than 0.99)',
                                    kind='pie')
    plt.show()
    Apple_price=find_price(Apple,'0.99')
    # data visualization
    Apple_plot = Apple_price.plot(title='Apple Store\n App category for prices of apps higher than 0.99', kind="pie")
    plt.show()
    print('Hypothesis 5:For those apps higher than normal price in the store($0.99), they fall into the Game category.\n','Apple Result\n',Apple_price)

    #hypothesis 6
    paid_app_cat,free_app_cat=gen_cat_result(Google)
    Google_combine=gen_df_result(free_app_cat,paid_app_cat)
    Google_combine_plot = Google_combine.plot(y=["free", "paid"], kind="bar", stacked=True)
    plt.show()
    # data visualization based on percentage
    Google_combine_pplot=Google_combine['free_percentage'].plot(kind='barh')
    x_major_locator = MultipleLocator(0.1)
    Google_combine_pplot.xaxis.set_major_locator(x_major_locator)
    plt.show()
    print('Hypothesis 6:The proportion of free apps in each categroy is higher than paid apps.\n','Google result\n',Google_combine)
    paid_app_cat,free_app_cat=gen_cat_result(Apple)
    Apple_combine=gen_df_result(free_app_cat,paid_app_cat)
    Apple_combine.plot(y=["free", "paid"], kind="bar", stacked=True)
    plt.show()
    # data visualization based on percentage
    Apple_combine_pplot = Apple_combine['free_percentage'].plot(kind='barh')
    x_major_locator = MultipleLocator(0.1)
    Apple_combine_pplot.xaxis.set_major_locator(x_major_locator)
    plt.show()
    print('Hypothesis 6:The proportion of free apps in each categroy is higher than paid apps.\n','Apple result\n',Apple_combine)

    #Hypothesis 4
    Analyze_same_App(Google,Apple)


    #Hypothesis 1
    myframe = Google[['Installs', 'Reviews', 'Rating']]
    addPropColumn(myframe, 'Reviews', 'Installs', ['+', ','])
    myframe[['Rating']] = pd.to_numeric(myframe['Rating'])
    sns.regplot(myframe['Proportion'], myframe['Rating'])# code for plot
    plt.show()
    print(myframe.dtypes)

    #Hypothesis 2
    #part1:find all words frequency
    wordsFreq = getFreq(Google_review, 'Translated_Review')

    #part2:data visulization
    remove_list=['nan','i','it','this','the','game','app']
    [wordsFreq.pop(key) for key in remove_list]
    print(wordsFreq)
    # reference:https://www.datacamp.com/community/tutorials/wordcloud-python
    wc = WordCloud(background_color="white").generate_from_frequencies(wordsFreq)
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    plt.show()
    end_time = time.time()
    print("the program runs", end_time - start_time)

    # part 3: find words under different sentiment
    Review = import_review()
    Analyze_Review(Review)
