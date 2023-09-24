import time
from bs4 import BeautifulSoup
import requests
import calendar
from .validator import Validator


class BoxOffice:
    """
    A package For getting Box office Information
    """

    def __init__(self, api_key=None):
        """
        initial class
        :param api_key: an api key from https://www.omdbapi.com/ if you provide an api key, you will also get
        movie poster url and movie description director and artists
        a free type of api provides 1000 calls per day so use it carefully
        """
        self._api_key = api_key
        self._output = []

    def get_daily(self, date):

        """
        getting information about daily box office information
        :param date: a date object with format like this: 2023-09-21 must not be in future
        :return: a list of dictionary's contains movie information
        """
        validator = Validator()
        validator.check_daily(date)
        if validator.is_valued:
            wanted_date = validator.result
            daily_url = f"https://www.boxofficemojo.com/date/{str(wanted_date)}/?ref_=bo_di_table_1"
            result = self._collect_daily(url=daily_url)
            return result

    def get_weekend(self, year: int, week: int):
        """
        get information about weekend box office
        :param year: year you want to get the information from must be a positive integer between 1982 and current year
        :param week: week you want to get information from must be a positive integer number between 1 and 52
        :return: a list of dictionary's contains movie information
        """
        validator = Validator()
        if validator.check_weekly(year=year, week=week):
            weekend_url = f"https://www.boxofficemojo.com/weekend/{year}W{week}/?ref_=bo_wey_table_5"
            result = self._collect_weekend(url=weekend_url)
            return result

    def get_weekly(self, year: int, week: int):
        """
        get weekly information about box office
        :param year: year you want to get the information from must be a positive integer between 1982, and current year
        :param week: week you want to get information from must be a positive integer number btween 1 and 52
        :return: a list of dictionary's contains movie information
        """
        validator = Validator()
        if validator.check_weekly(year=year, week=week):
            weekly_url = f"https://www.boxofficemojo.com/weekly/{year}W{week}/?ref_=bo_wly_table_1"
            weekly_url = "https://www.boxofficemojo.com/weekly/2023W37/?ref_=bo_wly_table_1"
            result = self._collect_weekly(url=weekly_url)
            return result

    def get_monthly(self, year: int, month: int):
        """
        get monthly information about box office
        :param year: year you want to get the information from must be a positive integer between 1982, and current year
        :param month: month you want to get information from must be a positive integer btween 1 and 12
        :return: a list of dictionary's contains movie information
        """
        validator = Validator()
        if validator.check_monthly(year=year, month=month):
            str_month = calendar.month_name[month].lower()
            monthly_url = f"https://www.boxofficemojo.com/month/{str_month}/{year}/?ref_=bo_ml_table_1"
            result = self._collect_month_year_(url=monthly_url)
            return result

    def get_season(self, year: int, season: str):
        """
        get season information box office
        :param year: year you want to get the information from must be a positive integer between 1982, and current year
        :param season: season you want to get information from must be a string of season name etc.: spring, fall, ...
        :return: a list of dictionary's contains movie information
        """
        validator = Validator()
        if validator.season_validate(year=year, season=season):
            season_url = f"https://www.boxofficemojo.com/season/{season.lower()}/{year}/?ref_=bo_sl_table_1"
            result = self._collect_month_year_(url=season_url)
            return result

    def get_quarterly(self, quarterly: int, year: int):
        """
        get quarterly information
        :param quarterly: quarterly you want to get information from must be a positive integer btween 1 and four
        :param year: year: year you want to get the information from must be a positive integer between 1982,
         and current year
        :return: a list of dictionary's contains movie information
        """
        validator = Validator()
        validator.check_quarterly(q=quarterly, year=year)
        if validator.is_valued:
            quarterly_url = f"https://www.boxofficemojo.com/quarter/q{quarterly}/{year}/?ref_=bo_ql_table_1"
            result = self._collect_month_year_(url=quarterly_url)
            return result

    def get_yearly(self, year: int):
        """
        get yearly box office information
        :param year: year you want to get the information from must be a positive integer between 1982,
        :return: a list of dictionary's contains movie information
        """
        validator = Validator()
        validator.validate_year(year=year)
        if validator.is_valued:
            yearly_url = f"https://www.boxofficemojo.com/year/{year}/?ref_=bo_yl_table_1"
            result = self._collect_month_year_(url=yearly_url)
            return result

    def _collect_daily(self, url):
        self._output = []
        try:
            response = requests.get(url).text
            daily_soap = BeautifulSoup(response, "html.parser")
            table = daily_soap.find("table", "mojo-body-table")
            table_rows = table.find_all("tr")

            for index, row in enumerate(table_rows):
                if index != 0:
                    td_element = row.find_all("td")
                    local_list = []
                    for td in td_element:

                        if "hidden" not in str(td):
                            td_text = td.get_text()
                            local_list.append(td_text)

                    if self._api_key is not None:
                        title = local_list[2]
                        api_url = f"https://www.omdbapi.com/?t={title}&apikey={self._api_key}"
                        time.sleep(1)
                        api_response = requests.get(api_url).json()

                        local_dict = {

                            "rank": local_list[0],
                            "previous day rank": local_list[1],
                            "title": title,
                            "daily gross": local_list[3],
                            "gross change daily": local_list[4],
                            "gross change week": local_list[5],
                            "theaters": local_list[6],
                            "per theaters avg gross": local_list[7],
                            "gross to date": local_list[8],
                            "number of days release": local_list[9],
                            "Distributor": local_list[10].replace("\n\n", ""),
                            "BoxOffice": api_response['BoxOffice'],
                            "Released": api_response['Released'],
                            "Runtime": api_response['Runtime'],
                            "Genre": api_response['Genre'],
                            "Director": api_response['Director'],
                            "Writer": api_response['Writer'],
                            "Actors": api_response['Actors'],
                            "description": api_response['Plot'],
                            "Country": api_response['Country'],
                            "Awards": api_response['Awards'],
                            "Poster": api_response['Poster'],
                            "imdbRating": api_response['imdbRating'],
                            "imdbID": api_response['imdbID'],

                        }
                        print(local_dict)
                        self._output.append(local_dict)
                    else:
                        local_dict = {

                            "rank": local_list[0],
                            "previous day rank": local_list[1],
                            "title": local_list[2],
                            "daily gross": local_list[3],
                            "gross change daily": local_list[4],
                            "gross change week": local_list[5],
                            "theaters": local_list[6],
                            "per theaters avg gross": local_list[7],
                            "gross to date": local_list[8],
                            "number of days release": local_list[9],
                            "Distributor": local_list[10].replace("\n\n", ""),

                        }
                        self._output.append(local_dict)

            return self._output
        except Exception as e:
            print(f"Error occurred: {e} Check Your Connection or wait  afew Second")

    def _collect_weekend(self, url):
        self._output = []
        try:
            response = requests.get(url).text
            daily_soap = BeautifulSoup(response, "html.parser")
            table = daily_soap.find("table", "mojo-body-table")
            table_rows = table.find_all("tr")

            for index, row in enumerate(table_rows):
                if index != 0:
                    td_element = row.find_all("td")
                    local_list = []
                    for td in td_element:

                        if "hidden" not in str(td):
                            td_text = td.get_text()
                            local_list.append(td_text)

                    if self._api_key is not None:
                        title = local_list[2]
                        api_url = f"https://www.omdbapi.com/?t={title}&apikey={self._api_key}"
                        time.sleep(1)
                        api_response = requests.get(api_url).json()

                        local_dict = {

                            "rank": local_list[0],
                            "previous week rank": local_list[1],
                            "title": title,
                            "weekend gross": local_list[3],
                            "gross change/week": local_list[4],
                            "theaters": local_list[5],
                            "number of theaters change": local_list[6],
                            "per theatre avg gross": local_list[7],
                            "total gross": local_list[8],
                            "weeks": local_list[9],
                            "Distributor": local_list[10].replace("\n\n", ""),
                            "BoxOffice": api_response['BoxOffice'],
                            "Released": api_response['Released'],
                            "Runtime": api_response['Runtime'],
                            "Genre": api_response['Genre'],
                            "Director": api_response['Director'],
                            "Writer": api_response['Writer'],
                            "Actors": api_response['Actors'],
                            "description": api_response['Plot'],
                            "Country": api_response['Country'],
                            "Awards": api_response['Awards'],
                            "Poster": api_response['Poster'],
                            "imdbRating": api_response['imdbRating'],
                            "imdbID": api_response['imdbID'],

                        }
                        print(local_dict)
                        self._output.append(local_dict)
                    else:
                        local_dict = {

                            "rank": local_list[0],
                            "previous week rank": local_list[1],
                            "title": local_list[2],
                            "weekend gross": local_list[3],
                            "gross change/week": local_list[4],
                            "theaters": local_list[5],
                            "number of theaters change": local_list[6],
                            "per theatre avg gross": local_list[7],
                            "total gross": local_list[8],
                            "weeks": local_list[9],
                            "Distributor": local_list[10].replace("\n\n", ""),

                        }
                        self._output.append(local_dict)

            return self._output
        except Exception as e:
            print(f"Error occurred: {e} Check Your Connection or wait  afew Second")

    def _collect_weekly(self, url):
        self._output = []
        try:
            response = requests.get(url).text
            daily_soap = BeautifulSoup(response, "html.parser")
            table = daily_soap.find("table", "mojo-body-table")
            table_rows = table.find_all("tr")

            for index, row in enumerate(table_rows):
                if index != 0:
                    td_element = row.find_all("td")
                    local_list = []
                    for td in td_element:

                        if "hidden" not in str(td):
                            td_text = td.get_text()
                            local_list.append(td_text)

                    if self._api_key is not None:
                        title = local_list[2]
                        api_url = f"https://www.omdbapi.com/?t={title}&apikey={self._api_key}"
                        time.sleep(1)
                        api_response = requests.get(api_url).json()

                        local_dict = {

                            "rank": local_list[0],
                            "previous week rank": local_list[1],
                            "title": title,
                            "weekly gross": local_list[3],
                            "gross change/week": local_list[4],
                            "theaters": local_list[5],
                            "number of theaters change": local_list[6],
                            "per theatre avg gross": local_list[7],
                            "total gross": local_list[8],
                            "weeks": local_list[9],
                            "Distributor": local_list[10].replace("\n\n", ""),
                            "BoxOffice": api_response['BoxOffice'],
                            "Released": api_response['Released'],
                            "Runtime": api_response['Runtime'],
                            "Genre": api_response['Genre'],
                            "Director": api_response['Director'],
                            "Writer": api_response['Writer'],
                            "Actors": api_response['Actors'],
                            "description": api_response['Plot'],
                            "Country": api_response['Country'],
                            "Awards": api_response['Awards'],
                            "Poster": api_response['Poster'],
                            "imdbRating": api_response['imdbRating'],
                            "imdbID": api_response['imdbID'],

                        }
                        print(local_dict)
                        self._output.append(local_dict)
                    else:
                        local_dict = {

                            "rank": local_list[0],
                            "previous week rank": local_list[1],
                            "title": local_list[2],
                            "weekly gross": local_list[3],
                            "gross change/week": local_list[4],
                            "theaters": local_list[5],
                            "number of theaters change": local_list[6],
                            "per theatre avg gross": local_list[7],
                            "total gross": local_list[8],
                            "weeks": local_list[9],
                            "Distributor": local_list[10].replace("\n\n", ""),

                        }
                        self._output.append(local_dict)

            return self._output
        except Exception as e:
            print(f"Error occurred: {e} Check Your Connection or wait  afew Second")

    def _collect_month_year_(self, url):
        self._output = []
        try:
            response = requests.get(url).text
            daily_soap = BeautifulSoup(response, "html.parser")
            table = daily_soap.find("table", "mojo-body-table")
            table_rows = table.find_all("tr")

            for index, row in enumerate(table_rows):
                if index != 0:
                    td_element = row.find_all("td")
                    local_list = []
                    for td in td_element:

                        if "hidden" not in str(td):
                            td_text = td.get_text()
                            local_list.append(td_text)

                    if self._api_key is not None:
                        title = local_list[1]
                        api_url = f"https://www.omdbapi.com/?t={title}&apikey={self._api_key}"
                        time.sleep(1)
                        api_response = requests.get(api_url).json()

                        local_dict = {

                            "rank": local_list[0],
                            "title": local_list[1],
                            "gross": local_list[2],
                            "theaters": local_list[3],
                            "total_gross": local_list[4],
                            "release date": local_list[5],
                            "Distributor": local_list[6].replace("\n\n", ""),
                            "BoxOffice": api_response['BoxOffice'],
                            "Released": api_response['Released'],
                            "Runtime": api_response['Runtime'],
                            "Genre": api_response['Genre'],
                            "Director": api_response['Director'],
                            "Writer": api_response['Writer'],
                            "Actors": api_response['Actors'],
                            "description": api_response['Plot'],
                            "Country": api_response['Country'],
                            "Awards": api_response['Awards'],
                            "Poster": api_response['Poster'],
                            "imdbRating": api_response['imdbRating'],
                            "imdbID": api_response['imdbID'],

                        }
                        print(local_dict)
                        self._output.append(local_dict)
                    else:
                        local_dict = {

                            "rank": local_list[0],
                            "title": local_list[1],
                            "gross": local_list[2],
                            "theaters": local_list[3],
                            "total_gross": local_list[4],
                            "release date": local_list[5],
                            "Distributor": local_list[6].replace("\n\n", ""),

                        }
                        self._output.append(local_dict)

            return self._output
        except Exception as e:
            print(f"Error occurred: {e} Check Your Connection or wait  afew Second")
