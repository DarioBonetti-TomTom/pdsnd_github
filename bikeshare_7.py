import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    print('Hello! Let\'s explore some US Bikeshare data')
    while True:
        choose_city = input("Would you like to see data for Chicago, New York or Washington?\n").lower()
        if choose_city in ('chicago', 'new york', 'washington'):
            print('the name of the city is matching the list!')
            break
        else:
            print("the name of the city is not in the list!")
    month_day_all = input("Would you like to filter the data by Month, Day, both, or not at all? Type \"all\" for no time filter:\n").lower()
    if month_day_all == 'month':
        print('We will make sure to filter by Month!')
        while True:
            month = input("Which Month? January, February, March, April, May or June? Please type out the full Month name:\n").lower()
            if month in ('january', 'february', 'march', 'april', 'may', 'june'):
                break
            else:
                print('That Month is not on the list!')
        day = 'all'
        city = choose_city.lower()
    if month_day_all == 'day':
        print('We will make sure to filter by Day!')
        while True:
            day = input("Which Day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday? Please type out the full day name:\n").lower()
            if day in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
                break
            else:
                print('That Day is not on the list!')
        month = 'all'
        city = choose_city.lower()
    if month_day_all == 'all':
        day =  'all'
        month = 'all'
        city = choose_city.lower()
    if month_day_all == 'both':
        print('We will make sure to filter by Month and Day!')
        while True:
            month = input("Which Month? January, February, March, April, May or June? Please type out the full month name:\n").lower()
            if month in ('january', 'february', 'march', 'april', 'may', 'june'):
                break
            else:
                print('That Month is not on the list!')
        while True:
            day = input("Which Day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday? Please type out the full day name:\n").lower()
            if day in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
                break
            else:
                print('That Day is not on the list!')
        city = choose_city.lower()
    print('Filters applied: {}, {}, {}'.format(city.title(), month.title(), day))
    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    df = pd.read_csv(CITY_DATA[city.lower()])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    return df

def time_stats(df):
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    popular_month =  df['month'].value_counts().idxmax()
    count_popular_month = df['month'].value_counts()[popular_month]
    popular_day =  df['day_of_week'].value_counts().idxmax()
    count_popular_day = df['day_of_week'].value_counts()[popular_day]
    df['hour'] = df['Start Time'].dt.hour
    popular_hour =  df['hour'].value_counts().idxmax()
    count_popular_hour = df['hour'].value_counts()[popular_hour]
    print('Most Frequent Start Month: {} Count: {}\n'.format(popular_month, count_popular_month))
    print('Most Frequent Start Day: {} Count: {}\n'.format(popular_day, count_popular_day))
    print('Most Frequent Start Hour: {} Count: {}'.format(popular_hour, count_popular_hour))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    popular_start_station =  df['Start Station'].value_counts().idxmax()
    count_popular_start_station = df['Start Station'].value_counts()[popular_start_station]
    popular_end_station =  df['End Station'].value_counts().idxmax()
    count_popular_end_station = df['End Station'].value_counts()[popular_end_station]
    df['Trip'] = df['Start Station'] + ' - ' + df['End Station']
    popular_trip =  df['Trip'].value_counts().idxmax()
    count_popular_trip = df['Trip'].value_counts()[popular_trip]
    print('Most Frequent Start Station: {} Count: {}\nMost Frequent End Station: {} Count: {}'.format(popular_start_station, count_popular_start_station, popular_end_station, count_popular_end_station))
    print('Most Frequent Trip from start to end: {} Count: {}'.format(popular_trip, count_popular_trip))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    total_travel_time = df['Trip Duration'].sum()
    total_travel_time_hours = round((total_travel_time/3600),3)
    average_travel_time = df['Trip Duration'].mean()
    total_travel_time_minutes = round((average_travel_time/60),3)
    print('Total Travel Time: {} hours\nAverage Travel Time: {} minutes'.format(total_travel_time_hours, total_travel_time_minutes))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    user_types =  df.groupby(['User Type'])['User Type'].count()
    print('The counts of each user type is: {}'.format(user_types))
    try:
        gender = df.groupby(['Gender'])['Gender'].count()
        oldest = df['Birth Year'].min()
        youngest = df['Birth Year'].max()
        popular_year_birth =  df['Birth Year'].value_counts().idxmax()
        count_popular_year_birth = df['Birth Year'].value_counts()[popular_year_birth]
        print('\nThe counts of each Gender is: {}'.format(gender))
        print('\nwhat is the oldest, youngest, and most popular year of birth, respectively? {}; {}; {} (count: {})'.format(oldest, youngest, popular_year_birth, count_popular_year_birth))
    except KeyError:
        print('\nNo birth year data to share')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    start_loc = 5
    while True:
        see_data = input("Would you like to see the first 5 rows of data? (Yes/No)\n").lower()
        if see_data == 'yes':
            print('\nCalculating Display Data...\n')
            start_time = time.time()
            five_rows_of_data = df.iloc[0:5]
            print('The first five rows of data are:\n')
            print(five_rows_of_data)
            while True:
                see_more_data = input("\nWould you like to see the next 5 rows of data? (Yes/No)\n").lower()
                if see_more_data == 'yes':
                    more_five_rows_of_data = df.iloc[start_loc:start_loc+5]
                    start_loc+=5
                    print('The next five rows of data are:\n')
                    print(more_five_rows_of_data)
                else:
                    print('\nOK! That was enough data!')
                    break
            print("\nThis took %s seconds." % (time.time() - start_time))
            print('-'*40)
        break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
if __name__ == "__main__":
	main()
