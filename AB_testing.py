import pandas as pd
import csv

# reading the csv file 'ad_clicks.csv' and only displaying the first 10 rows 
# ad_clicks = pd.read_csv('/Users/hectorprado/Desktop/CodeCademy/Data_Analytics/Aggregates_in_Pandas/A:B Testing/ad_clicks.csv')
ad_clicks = pd.read_csv('ad_clicks.csv')

print('\nAd Clicks data frame only displaying first 10 rows:\n'+str(ad_clicks.head(10)))

# data frame created with the count of number of views coming from each plataform and renaming the columns 
utm_source_count = ad_clicks.groupby('utm_source').day.count().reset_index()
utm_source_count.rename(columns = {'day':'count'}, inplace = True)
print('\nNumber of views coming from each plataform: \n'+str(utm_source_count))


# adding a new column that displays 'True' if the row of the column ad_click_timestamp is not null, else false 
is_click = ~ad_clicks.ad_click_timestamp.isnull()
ad_clicks['is_click'] = is_click
print('\nColumn is_clicked added displays True if ad_click_timestamp is not null:\n'+(str(ad_clicks.head(10))))


clicks_by_source = ad_clicks.groupby(['utm_source', 'is_click']).user_id.count().reset_index()
print('\nPercent of people who click on ads from each source:\n'+str(clicks_by_source))

clicks_pivot = clicks_by_source.pivot(columns = 'is_click', index = 'utm_source' , values = 'user_id')
print('\nPivot data frame for better display:\n'+str(clicks_pivot))

# added column of percentaged of people who saw the add by clicking on the site and rounded to 2 decimal numbers 
clicks_pivot['percent_clicked'] = round((clicks_pivot[True]/(clicks_pivot[True].sum()+clicks_pivot[False].sum()))*100,2)

print('\nPivoted data frame with column percent_clicked added:\n'+str(clicks_pivot))

# Get the amount of poeple who were shown either ad A or ad B 
experimental_group = ad_clicks.groupby('experimental_group').day.count().reset_index()
experimental_group.rename(columns = {'day': 'count'}, inplace = True)
print('\nExperimental group ad A and B count:\n'+str(experimental_group))


# data frame of every source that countains the number of people who clicked on each ad or not 
clicks_by_source  = ad_clicks\
                    .groupby(['utm_source','is_click'])\
                    .user_id\
                    .count()\
                    .reset_index()\
                    .pivot( index = 'utm_source', columns = 'is_click', values = 'user_id')\
                    .reset_index()
print('\ndata frame of every source that countains the number of people who clicked on each ad or not:\n'+str(clicks_by_source))


a_or_b = ad_clicks\
        .groupby(['experimental_group','is_click'])\
        .user_id\
        .count()\
        .reset_index()\
        .pivot(columns = 'is_click', index = 'experimental_group', values = 'user_id')\
        .reset_index()

print('\nDisplaying only the experimental groups and the result:\n'+str(a_or_b))

# created 2 data frames and pivot them, one with A ads the other one with only B ads 
a_clicks = ad_clicks[ad_clicks.experimental_group == 'A']
b_clicks = ad_clicks[ad_clicks.experimental_group == 'B']

a_clicks_pivot=\
    a_clicks\
    .groupby(['is_click', 'day'])\
    .user_id.count()\
    .reset_index()\
    .pivot(
        index = 'day',\
        columns = 'is_click',\
        values = 'user_id'
    )\
    .reset_index()




b_clicks_pivot=\
    b_clicks\
    .groupby(['is_click', 'day'])\
    .user_id.count()\
    .reset_index()\
    .pivot(
        index = 'day',\
        columns = 'is_click',\
        values = 'user_id'
    )\
    .reset_index()

#  column added of percentage of useres who clicked on the ad per day 
a_clicks_pivot['percent_clicked'] = round(a_clicks_pivot[True]/ (a_clicks_pivot[True] + a_clicks_pivot[False]) * 100,2)
b_clicks_pivot['percent_clicked'] = round(b_clicks_pivot[True]/ (b_clicks_pivot[True] + b_clicks_pivot[False]) * 100,2)



print('\nData Frame displays the result of ad A and percentage of clicks per day:\n'+str(a_clicks_pivot))
print('\nData Frame displays the result of ad B and percentage of clicks per day:\n'+str(b_clicks_pivot))


