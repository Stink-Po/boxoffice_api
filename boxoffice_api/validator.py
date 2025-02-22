from datetime import datetime as dt


class Validator:
    def __init__(self):
        self.is_valued = False
        self.result = None

    def check_daily(self, day):

        try:
            wanted_date = dt.strptime(str(day), "%Y-%m-%d").date()
            today = dt.utcnow().date()

            if today < wanted_date:
                raise ValueError(f"Provided date is : {wanted_date} is in the Future")

            else:
                self.is_valued = True
                self.result = wanted_date
                return self.result, self.is_valued

        except ValueError as e:
            print(f"Error occurred: {e}")

    def check_weekly(self, year: int, week: int):
        try:
            int(week)
            int(year)
            current_year, current_week, _ = dt.utcnow().isocalendar()
            if year < 1982:
                raise ValueError("We Just Have Information after 1982 in the database")
            if week > 52:
                raise ValueError("week must be less than 52")
            if int(dt.utcnow().year) < year:
                raise ValueError("Inserted Year is Invalid")
            if int(current_year) == int(year) and int(current_week) < int(week):
                raise ValueError("Provided week is out of range")

            else:
                self.is_valued = True
                return self.is_valued

        except Validator as e:
            self.is_valued = False
            print(f"Input type Error : {e}")

    def check_monthly(self, year: int, month: int):
        try:
            int(year)
            int(month)
            if year < 1982:
                raise ValueError("We Just Have Information after 1982 in the database")
            if int(dt.utcnow().year) < year:
                raise ValueError("Selected Year is in future")
            if 0 < month < 13:
                self.is_valued = True
                return self.is_valued
            else:
                raise ValueError("month Must be between 1 and 12")

        except ValueError as e:
            print(f"Input type Error : {e}")
            self.is_valued = False

    def check_quarterly(self, q: int, year: int):
        try:
            int(q)
            int(year)
            if year < 1982:
                self.is_valued = False
                raise ValueError("We Just Have Information after 1982 in the database")
            if int(dt.utcnow().year) < year:
                self.is_valued = False
                raise ValueError("Selected Year is in future")
            if 0 < q < 5:
                self.is_valued = True
                return self.is_valued
            else:
                self.is_valued = False
                raise ValueError("Quarterly must be a positive number between 1 and 4")

        except ValueError as e:
            print(f"Input type Error : {e}")
            self.is_valued = False

    def validate_year(self, year):
        try:
            int(year)
            if year < 1982:
                self.is_valued = False
                raise ValueError("We Just Have Information after 1982 in the database")
            if int(dt.utcnow().year) < year:
                self.is_valued = False

            else:
                self.is_valued = True
                return self.is_valued

        except ValueError as e:
            print(f"Input type Error : {e}")
            self.is_valued = False

    def season_validate(self, year: int, season: str):
        if self.validate_year(year=year):
            seasons = ["spring", "summer", "fall", "winter"]
            if season.casefold() in seasons:
                self.is_valued = True
            else:
                self.is_valued = False
                raise ValueError("seasons are 'spring' 'summer' 'fall' 'winter'")

            return self.is_valued

    def check_integer(self, value: int):
        return isinstance(value, int)

    def check_year(self, year: int):
        if self.check_integer(value=year):
            return 1982 < year < int(dt.utcnow().year)
        else:
            print("Year Must be an Integer")

    def check_month(self, month: int):
        if self.check_integer(value=month):
            return 0 < month < 13
        else:
            print("Month Must be an Integer")

    def check_week(self, week: int):
        if self.check_integer(value=week):
            return 0 < week < 53

