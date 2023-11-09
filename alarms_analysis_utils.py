import datetime
import seaborn as sns
import pandas as pd

from matplotlib import pyplot as plt


# Round time to nearest 5 minutes
def round_time_5(time):
    time = datetime.datetime.strptime(time, '%H:%M:%S')
    minute = time.minute
    if minute < 3:
        minute = 0
    elif minute < 8:
        minute = 5
    elif minute < 13:
        minute = 10
    elif minute < 18:
        minute = 15
    elif minute < 23:
        minute = 20
    elif minute < 28:
        minute = 25
    elif minute < 33:
        minute = 30
    elif minute < 38:
        minute = 35
    elif minute < 43:
        minute = 40
    elif minute < 48:
        minute = 45
    elif minute < 53:
        minute = 50
    elif minute < 58:
        minute = 55
    else:
        minute = 0

    time = time.replace(minute=minute, second=0, microsecond=0)
    return time.strftime('%H:%M')


# Round time to nearest 10 minutes:
def round_time_10(time):
    time = datetime.datetime.strptime(time, '%H:%M:%S')
    minute = time.minute
    if minute < 5:
        minute = 0
    elif minute < 15:
        minute = 10
    elif minute < 25:
        minute = 20
    elif minute < 35:
        minute = 30
    elif minute < 45:
        minute = 40
    elif minute < 55:
        minute = 50
    else:
        minute = 0

    time = time.replace(minute=minute, second=0, microsecond=0)
    return time.strftime('%H:%M')


# Round time to nearest 15 minutes:
def round_time_15(time):
    time = datetime.datetime.strptime(time, '%H:%M:%S')
    minute = time.minute
    if minute < 8:
        minute = 0
    elif minute < 23:
        minute = 15
    elif minute < 38:
        minute = 30
    elif minute < 53:
        minute = 45
    else:
        minute = 0

    time = time.replace(minute=minute, second=0, microsecond=0)
    return time.strftime('%H:%M')


# Round time to nearest 30 minutes:
def round_time_30(time):
    time = datetime.datetime.strptime(time, '%H:%M:%S')
    minute = time.minute
    if minute < 15:
        minute = 0
    elif minute < 45:
        minute = 30
    else:
        minute = 0

    time = time.replace(minute=minute, second=0, microsecond=0)
    return time.strftime('%H:%M')


def plot_time_of_day(_df, round_minutes, title_postfix='', limit=20):
    _by_time_df = (_df.groupby('time_rounded')
                   .agg(count=('time_rounded', 'count'))
                   .sort_values(by='count', ascending=False))
    plt.figure(figsize=(10, 10))
    sns.barplot(x=_by_time_df['count'][:limit], y=_by_time_df.index[:limit], orient='h')
    plt.xticks(rotation=90)
    plt.ylabel(f'Time rounded to the nearest {round_minutes} minutes')
    plt.xlabel('Alarms count')
    plt.title(f'Top {limit} times of day with the most alarms {title_postfix}')
    plt.show()


# Plots all the alarms where X axis are bins of {round_minutes} minutes over 24 hours, and Y axis is the count of alarms in each bin:
def plot_time_of_day_24_hours(_df, round_minutes, title_postfix=''):
    # create a df of 24 hours with 10 minutes bins:
    _df_24_hours = pd.DataFrame({'time_rounded': [f'{i:02d}:{j:02d}' for i in range(24) for j in range(0, 60, 10)]})

    # for every bin, count the number of alarms in that bin:
    _df_24_hours['count'] = _df_24_hours['time_rounded'].apply(lambda x: _df[_df['time_rounded'] == x].shape[0])

    # plot the results:
    plt.figure(figsize=(25, 10))
    sns.set_palette('colorblind')
    sns.barplot(y=_df_24_hours['count'], x=_df_24_hours['time_rounded'])
    # Make bins with higher alarms count darker:
    for i, bar in enumerate(plt.gca().patches):
        bar.set_color(plt.cm.get_cmap('YlOrRd')(_df_24_hours['count'][i] / _df_24_hours['count'].max()))

    # Only show x ticks for every one hour:
    plt.xticks(range(0, 144, 6), [f'{i:02d}:00' for i in range(24)])
    plt.xlabel(f'Time rounded to the nearest {round_minutes} minutes')
    plt.ylabel('Alarms count')
    plt.title(f'Histogram of alarms over the day {title_postfix}')
    plt.show()
