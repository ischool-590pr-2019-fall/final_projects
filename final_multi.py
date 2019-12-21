from final import *
from multiprocessing import Process

if __name__ == '__main__':
    start_time = time.time()
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
    p1 = Process(target=Analyze_Free_rate, args=(Google, Apple))
    p1.start()

    # hypothesis 5
    Google_price = find_price(Google, '0.99')
    print(
        'Hypothesis 5:For those apps higher than normal price in the store($0.99), they fall into the Game category.\n',
        'Google result\n', Google_price)
    # data visualizaiton
    Google_plot = Google_price.plot(title='Google Play Store\nApp category for Prices of apps higher than 0.99)',
                                    kind='pie')
    plt.show()
    Apple_price = find_price(Apple, '0.99')
    # data visualization
    Apple_plot = Apple_price.plot(title='Apple Store\n App category for prices of apps higher than 0.99', kind="pie")
    plt.show()
    print(
        'Hypothesis 5:For those apps higher than normal price in the store($0.99), they fall into the Game category.\n',
        'Apple Result\n', Apple_price)

    # hypothesis 6
    paid_app_cat, free_app_cat = gen_cat_result(Google)
    Google_combine = gen_df_result(free_app_cat, paid_app_cat)
    Google_combine_plot = Google_combine.plot(y=["free", "paid"], kind="bar", stacked=True)
    plt.show()
    # data visualization based on percentage
    Google_combine_pplot = Google_combine['free_percentage'].plot(kind='barh')
    x_major_locator = MultipleLocator(0.1)
    Google_combine_pplot.xaxis.set_major_locator(x_major_locator)
    plt.show()
    print('Hypothesis 6:The proportion of free apps in each categroy is higher than paid apps.\n', 'Google result\n',
          Google_combine)
    paid_app_cat, free_app_cat = gen_cat_result(Apple)
    Apple_combine = gen_df_result(free_app_cat, paid_app_cat)
    Apple_combine.plot(y=["free", "paid"], kind="bar", stacked=True)
    plt.show()
    # data visualization based on percentage
    Apple_combine_pplot = Apple_combine['free_percentage'].plot(kind='barh')
    x_major_locator = MultipleLocator(0.1)
    Apple_combine_pplot.xaxis.set_major_locator(x_major_locator)
    plt.show()
    print('Hypothesis 6:The proportion of free apps in each categroy is higher than paid apps.\n', 'Apple result\n',
          Apple_combine)

    # Hypothesis 4
    p = Process(target=Analyze_same_App, args=(Google, Apple))
    p.start()

    # Hypothesis 1
    myframe = Google[['Installs', 'Reviews', 'Rating']]
    addPropColumn(myframe, 'Reviews', 'Installs', ['+', ','])
    myframe[['Rating']] = pd.to_numeric(myframe['Rating'])
    sns.regplot(myframe['Proportion'], myframe['Rating'])  # code for plot
    plt.show()
    print(myframe.dtypes)

    # Hypothesis 2
    # part1:find all words frequency
    wordsFreq = getFreq(Google_review, 'Translated_Review')

    # part2:data visulization
    remove_list = ['nan', 'i', 'it', 'this', 'the', 'game', 'app']
    [wordsFreq.pop(key) for key in remove_list]
    print(wordsFreq)
    wc = WordCloud(background_color="white").generate_from_frequencies(wordsFreq)
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    plt.show()
    end_time = time.time()
    print("the program runs", end_time - start_time)

    # part 3: find words under different sentiment
    Review = import_review()
    Analyze_Review(Review)