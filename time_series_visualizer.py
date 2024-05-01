import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv", parse_dates=True, index_col='date')

# Clean data
#filter out top & bottom 2.5% page views
df = df[(df['value']>=df['value'].quantile(0.025)) & (df['value']<=df['value'].quantile(0.975))]

def draw_line_plot():
    # Draw line plot
    fig = plt.figure(figsize=(16, 6))
    plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    plt.plot(df['value'], color='red')
    plt.xlabel('Date'), 
    plt.ylabel('Page Views')

    plt.close()


    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar.reset_index(inplace=True)

    #extract month, day, year from date(already a datetime obj) 
    df_bar['month'] = [d.strftime('%B') for d in df_bar.date] 
    df_bar['year'] = df_bar['date'].dt.year

    #set month order
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    df_bar['month'] = pd.Categorical(df_bar['month'], categories=month_order, ordered=True)

    #average daily page views for each month grouped by year
    df_bar = df_bar[['year', 'month','value']].groupby(['year', 'month'], observed=False).mean()

    #pivot modified df for plotting
    dfbar_pivot = pd.pivot_table(df_bar, index="year", columns="month", values='value', observed=False)

    # Draw bar plot
    plt.rcParams["figure.figsize"] = (9,7)

    fig = dfbar_pivot.plot(kind='bar').figure
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.legend(title='Months')

    plt.close()    


    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    #set (abrev) month order
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    df_box['month'] = pd.Categorical(df_box['month'], categories=month_order, ordered=True)

    # Draw box plots (using Seaborn)
    fig = plt.figure(figsize=(20, 6))

    #1st box plot---years
    fig.add_subplot(1,2,1)
    sns.boxplot(data=df_box, x='year', y='value', hue='year', palette='tab10', legend=None)
    plt.xlabel('Year')
    plt.ylabel('Page Views')
    plt.title('Year-wise Box Plot (Trend)')
    plt.yticks(list(range(0,220000,20000))) 


    #2nd boxplot---months
    fig.add_subplot(1,2,2)
    sns.boxplot(data=df_box, x='month', y='value', hue='month', palette='husl', legend=None)
    plt.xlabel('Month')
    plt.ylabel('Page Views')
    plt.title('Month-wise Box Plot (Seasonality)')
    plt.yticks(list(range(0,220000,20000))) 

    plt.close()


    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
