import time
import datetime
import pandas as pd
import numpy as np

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }

city_list = ['Chicago', 'New York City', 'Washington']
months = ['January', 'February', 'March', 'April', 'May', 'June']
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "N" to apply no month filter
        (str) day - name of the day of week to filter by, or "N" to apply no day filter
    """
    print('\nHELLO LET\'S EXPLORE SOME US BIKE SHARE DATA!')
    print('\nWe have data from three selected major cities.')
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ''
    city = input('From which city would you like to see the data?\nType Chicago, New York City, or Washington: ').title()

    while city not in city_list:
        print('\nThat seems to be an invalid input.\nPlease choose your answer from the following list: ', city_list)
        city = input('From which city would you like to see the data?: ').title()
    
    print('\nThank you, we\'ll show you the data for {}.'.format(city))

    # give user the option to filter month
    month = 'any month'
    month_filter = input('Would you like to filter for month? Type Y or N: ').title()

    while month_filter not in ['Y','N']:
        print('\nThat seems to be an invalid input.\nPlease type Y for filter or N for no filter.')
        month_filter = input('Would you like to filter for month? Type Y or N: ').title()

    # get user input for month (all, january, february, ... , june)
    while month_filter == 'Y':
        month = input('\nFrom which month would you like to see the data?\nType January, February, March, April, May, or June: \n').title()
        
        while month not in months:
            print('\nThat seems to be an invalid input.\nPlease choose your answer from the following list: ', months)
            month = input('From which month would you like to see the data?: ').title()

        print('\nThank you, we\'ll show you the data for {} in {}'.format(city, month))
        break
    
    # give user the option to filter day
    day = 'anyday'
    day_filter = input('\nWhat about day of week? Would you like to filter that?\nType Y or N: ').title()
    
    while day_filter not in ['Y','N']:
        print('\nThat seems to be an invalid input.\nPlease type Y for filter or N for no filter.')
        day_filter = input('Would you like to filter for day? Type Y or N: ').title()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while day_filter == 'Y':
        day = input('\nWhich day would you like to filter by?\nType Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday: ').title()

        while day not in days:
            print('\nThat seems to be an invalid input\nPlease choose your answer from the following list: ', days)
            day = input('Which day would you like to filter by?: ').title()
            
        print('\nThank you, we\'ll show you the data for {} from {}s in {}.'.format(city, day, month))
        break

    print('-'*80)
    print('\nOk, here we go!')
    print('-'*80)
    print('SHOWING DATA FOR {} FROM {}S IN {}'.format(city.upper(), day.upper(), month.upper()))
    print('-'*80)
    
    return city, month, day    


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "N" to apply no month filter
        (str) day - name of the day of week to filter by, or "N" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a DataFrame
    df = pd.read_csv(CITY_DATA[city])

    # convert Start Time column to datetime format
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week to create new columns
    df['month'] = df['Start Time'].dt.strftime("%B")
    df['day of week'] = df['Start Time'].dt.strftime("%A")
    
    # filter by month if applicable
    if month in months:
        df = df[df['month'] == month]
  
    # filter by day of applicable
    if day in days:
        df = df[df['day of week'] == day]


    return df
    

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]

    # display the most common day of week
    popular_day = df['day of week'].mode()[0]

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)

    print('TIME OF TRAVEL')
    print('-'*80)
    print('Most popular month: {} \nMost popular day of week: {} \nMost popular hour: {} o\'clock'.format(popular_month, popular_day, popular_hour))
    print('-'*80)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]

    # calculate frequency of each combination of start station and end station  
    journey = df.groupby(['Start Station', 'End Station']).size().reset_index().rename(columns={0:'count'}).sort_values(by='count', ascending = False)
    # display the most frequent start station
    journey_from = journey.iloc[0,0]
    # display the most frequent end station
    destination = journey.iloc[0,1]

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)
    
    print('JOURNEY')
    print('-'*80)
    print('Most popular start station: {} \nMost popular destination station: {}'.format(popular_start_station, popular_end_station))
    print('Most popular journey is: from {} to {}'.format(journey_from, destination))
    print('-'*80)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()

    # display mean travel time
    avg_travel_time = df['Trip Duration'].mean()

    # display max travel time
    max_travel_time = df['Trip Duration'].max()
    
    # display min travel time
    min_travel_time = df['Trip Duration'].min()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)

    print('JOURNEY TIME')
    print('-'*80)
    print('Total usage: {} hours \nAverage journey time for each usage: {} minutes'.format(int((total_travel_time/60)/60), int(avg_travel_time/60)))
    print('Maximum journey time: {} minutes'.format(int(max_travel_time/60)))
    print('Minimum journey time: {} minutes'.format(int(min_travel_time/60)))
    print('-'*80)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # display counts of user types
    user_types = df['User Type'].value_counts()
    percentage_type = user_types/user_types.sum()*100
    percentage_type = percentage_type.round(decimals = 2)

    # display behaviour of each user types

    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)
    print('USER TYPE')
    print('-'*80)
    print('Breakdown of user types (users):\n', user_types)
    print('\nPercentage of each type (%):\n', percentage_type)
    print('-'*80)

def demographic(df):
    """Displays statistics on bikeshare users demographic."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # dealing with NaN in Gender column
    df['Gender'] = df['Gender'].fillna('not disclosed')
    # display counts of gender
    gender_count = df['Gender'].value_counts()
    percentage_gender = gender_count/gender_count.sum()*100
    percentage_gender = percentage_gender.round(decimals = 2)

    # dealing with NaN in Birth Year Column
    df['Birth Year'] = df['Birth Year'].dropna(axis = 0)
    # display user demographic
    now = datetime.datetime.now()
    current_year = int(now.year)
    youngest = current_year - int(df['Birth Year'].max())
    oldest = current_year - int(df['Birth Year'].min())
    majority_age = current_year - df['Birth Year'].mode()
    average_age = current_year - int(df['Birth Year'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)
    print('USER DEMOGRAPHIC')
    print('-'*80)
    print('User gender (users):\n', gender_count)
    print('\nPercentage of each gender (%):\n', percentage_gender)
    print('\nDemographic: \nMajority of users: {} years old\nAverage user age: {} years old\nThe youngest: {} years old\nThe oldest: {} years old'.format(int(majority_age[0]), average_age, youngest, oldest)) 
    print('-'*80)

def display_data(df):
    """
    Prompt the user if they wantto see five lines of raw data, 
    display that data if the answer is 'yes', and continue these prompts and displays until the user says 'no'
    """
    def is_valid(display):
        """Check if the input is valid"""
        if display in ['Y', 'N']:
            return True
        else:
            return False

    start = 0
    end = 5
    
    # give user the option to view raw data
    valid_input = False
    while valid_input == False:
        display = input('Would you also like to see some raw data? Type Y or N: ').title()
        valid_input = is_valid(display)
        if valid_input == True:
            break
        else:
            print('\nThat seems to be an invalid input.\nPlease type Y to display raw data or N to continue to the next section.')

    if display == 'Y':
        print(df.iloc[start:end])
        
        # give user the option to view more data
        more_data = ''
        while more_data != 'N':
            valid_input_2 = False
            while valid_input_2 == False:
                more_data = input('\nWould you like to see more? Type Y or N: ').title()
                valid_input_2 = is_valid(more_data)
                if valid_input_2 == True:
                    break
                else:
                    print('\nThat seems to be an invalid input.\nPlease type Y to display more data or N to continue to the next section.')
            if more_data == 'Y':
                start += 5
                end += 5
                print(df.iloc[start:end])
            elif more_data == 'N':
                break

                
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        if city in ['Chicago', 'New York City']:
            demographic(df)

        print('\nHope our data gives you some insights!')
        # give user an option to see the raw data based on their filter(s) 
        display_data(df)

        # give user an option to look at other data sets 
        restart = input('\nWould you like to look at other cities and/or with other filters as well? \nType Y or N: ').title()

        while restart not in ['Y','N']:
            print('\nThat seems to be an invalid input.\nPlease type Y to restart or N to end the query.')
            restart = input('\nWould you like to look at other cities and/or with other filters as well? \nType Y or N: ').title()        
        
        if restart != 'Y':
            print('\nOK, BYE! :)\n')
            break

#F currently running main
if __name__ == "__main__":
	main()
