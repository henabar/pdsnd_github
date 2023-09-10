import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    city = ""
    choice_month=""
    choice_day=""
    month=""
    day=""
    valid_input= False
    
# code will handle issues with capitalization, but otherwise requires precise inputs
# get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while valid_input ==False:
        city = input("Would you like to see data for chicago, new york or washington?\n")
        if city.lower() not in {'chicago', 'new york', 'washington'}:
            print("That is not a valid city! Try again")
        else :
            print("Let's see data for: ", city.lower())
            city = city.lower()
            valid_input = True

# get user input for month (all, january, february, ... , june)
    valid_input = False
    while valid_input == False:
        choice_month = input("Would you like to filter the data by month? Type \'yes\' or \'no\'\n")
        if choice_month.lower() not in {'yes','no'}:
            print("That is not a valid choice! Try again")
        elif choice_month.lower()=='yes':
            month=input("what month? options are january, february, march, april, may, june\n")
            if month.lower() not in {'january','february','march','april','may','june'}:
                print("That is not a valid choice! Try again")
            else:
                month=month.lower()
                valid_input=True
        else: 
            month='all'
            valid_input =True

# get user input for day of week (all, monday, tuesday, ... sunday)
    valid_input =False
    while valid_input == False: 
        choice_day = input("Would you like to filter the data by day of week? Type \'yes\' or \'no\'\n")
        if choice_day.lower() not in {'yes','no'}:
            print("That is not a valid choice! Try again")
        elif choice_day.lower()=='yes':
            day=input("what day? options are mon, tue, wed, thu, fri, sat, sun\n")
            if day.lower() not in {'mon','tue','wed','thu','fri','sat','sun'}:
                print("That is not a valid choice! Try again")
            else:
                day=day.lower()
                valid_input=True
        else: 
            day='all'
            valid_input =True

    print('-'*40)
    print("You selected::",city,month,day)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    if city=='new york':
        city='new york city'
        
    filename=CITY_DATA[city]
    # add path to city name
    df = pd.read_csv(filename)
    ## convert the Start Time and End Time columns to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()
    #Create a list of months
    if month!="all":
        df = df[df['month'] == month.title()]
    if day!="all":
        df = df[df['day_of_week'].str[:3] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print('Most common month:', common_month)

    # display the most common day of week
    common_day_of_week = df['day_of_week'].mode()[0]
    print('Most common day of the week:', common_day_of_week)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print('Most common start hour:', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('Most common start station:', common_start_station)

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('Most common end station:', common_end_station)

    # display most frequent combination of start station and end station trip
    combo_start=""
    combo_end=""
    grouped_stations = df.groupby(['Start Station','End Station'])['Trip Duration'].count()
    max_count_index = grouped_stations.idxmax()
    combo_start, combo_end = max_count_index
    max_count = grouped_stations[max_count_index]
    print("Most frequent combination of start station and end station is: \n Start: {}, End: {}, with a total of {} trips".format( combo_start, combo_end, max_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total travel time is {:.2f} minutes'.format(df['Trip Duration'].sum()/60))

    # display mean travel time
    print('Mean travel time is {:.2f} minutes'.format(df['Trip Duration'].mean()/60))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    not_available_user_types= df['User Type'].isnull().sum()
    print('Number of user types is\n',user_types.to_string())
    print ('Please note that {} user types are not available'.format(not_available_user_types))
    
    if city.lower()!='washington':
        # Display counts of gender
        gender_counts = df['Gender'].value_counts()
        not_available_user_genders= df['Gender'].isnull().sum()
        print('Gender count is\n',gender_counts.to_string())
        print ('Please note that {} user genders were not available'.format(not_available_user_genders))

        # Display earliest, most recent, and most common year of birth
        earliest_birth_year = df['Birth Year'].min()
        print('Earliest birth year is',int(earliest_birth_year))
        latest_birth_year = df['Birth Year'].max()
        print('Most recent birth year is',int(latest_birth_year))
        common_birth_year = df['Birth Year'].mode()
        print('Most common birth year is',int(common_birth_year))
        not_available_birth_year= df['Birth Year'].isnull().sum()
        print("Please note that {} birth years were not available".format(not_available_birth_year))
    else:
        print("Gender and age statistics are not available for this city")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def raw_data(df):
    """Displays raw data 5 lines at a time on bikeshare users."""
    valid_input = False
    i=0
    while valid_input == False and i<df['Start Time'].count():
        see_trip_data = input("Would you like to see individual trip data? Type \'yes\' or \'no\'\n")
        if see_trip_data.lower() not in {'yes','no'}:
            print("That is not a valid choice! Try again")
        elif see_trip_data.lower() =='yes':
            # show data 5 rows
            print(df.iloc[i:(i+5),:])
            i=i+5
        else:
            valid_input= True

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        raw_data(df)
        # If response from user (below) is anything other than "yes" then the assumed response is "no"
        restart = input('\nWould you like to restart? Enter yes to continue.\n')
        if restart.lower() != 'yes':
            print("Thank you for using the bikeshare data analysis tool! Goodbye!")
            break


if __name__ == "__main__":
	main()
