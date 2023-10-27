### **Unofficial Python API for Box Office Mojo**

**update Note**
you can now get a panda Dataframe as output

This Python package allows you to retrieve box office information from Box Office Mojo. It provides data on daily, weekly, monthly, seasonal, quarterly, and yearly box office performance for movies. Additionally, it can fetch additional movie details like posters, descriptions, directors, and more from OMDb API when an API key is provided.

**Installation**

You can install this package using pip:

    pip install boxoffice_api

### Usage

Here's how you can use this package to retrieve box office information:
if You want to have more information from Movies, you can get free API key From "https://www.omdbapi.com/"
free account have 1000 daily requests we highly recommend if you want to use this package for collecting data and don't want to use thing like movie posters etc . don't use the API key

    from boxoffice_api import BoxOffice 

**if you have API Key**  

    box_office = BoxOffice(api_key="your_api_key") # Get daily box office information for a specific date 

**if you want to use the package without API Key**

    box_office = BoxOffice()

**if you want to use the package without API key and get panda Dataframe as output**


    box_office = BoxOffice(outputformat="DF")



#### **Getting Information**
    daily_data = box_office.get_daily("2023-09-21") # Get weekend box office information for a specific year and week 
    weekend_data = box_office.get_weekend(year=2023, week=39) # Get weekly box office information for a specific year and week 
    weekly_data = box_office.get_weekly(year=2023, week=39) # Get monthly box office information for a specific year and month 
    monthly_data = box_office.get_monthly(year=2023, month=9) # Get seasonal box office information for a specific year and season 
    seasonal_data = box_office.get_season(year=2023, season="fall") # Get quarterly box office information for a specific quarter and year 
    quarterly_data = box_office.get_quarterly(quarterly=3, year=2023) # Get yearly box office information for a specific year 
    yearly_data = box_office.get_yearly(year=2023) # Access the data as a list of dictionaries for movie in daily_data: print(movie)

Please replace "your_api_key" with your actual OMDb API key if you want to fetch additional movie details.

### Documentation

BoxOffice(api_key=None): Initializes the BoxOffice class with an optional OMDb API key.

get_daily(date): Retrieve daily box office information for a specific date.

get_weekend(year, week): Retrieves weekend box office information for a specific year and week.

get_weekly(year, week): Retrieve weekly box office information for a specific year and week.

get_monthly(year, month): Retrieve monthly box office information for a specific year and month.

get_season(year, season): Retrieve seasonal box office information for a specific year and season.

get_quarterly(quarterly, year): Retrieves quarterly box office information for a specific quarter and year.

get_yearly(year): Retrieves yearly box office information for a specific year.

**Output Example:**

    print(daily_records[0])
    >>>
    {
        'rank': '1',
        'yesterday rank': '1',
        'title': 'Thor: Love and Thunder',
        'daily gross': '$14,354,321',
        'gross change daily': '-22.4%',
        'gross change week': '-55.8%',
        'theaters': '4,375',
        'per theaters avg gross': '$3,280',
        'gross to date': '$233,903,308',
        'number of days release': '10',
        'Distributor': 'Walt Disney Studios Motion Pictures'
    }

### Dependencies

This package relies on the following Python libraries:

    BeautifulSoup
    requests



Please make sure to install these dependencies before using the package.

### Note

When using an OMDb API key, you can access additional movie details such as movie posters, descriptions, directors, actors, and more.

The package may make multiple requests to fetch movie details, so be mindful of your API limits, especially if you have a free API key.

Ensure you have a stable internet connection when making requests to Box Office Mojo and OMDb API.

Author

This Python package was created by Pourya Mohamadi. Feel free to contact fresh.pourya@gmail.com

    

