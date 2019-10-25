# -*- coding: utf-8 -*-

import pylab
import re
import math

# cities in our weather data
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHILADELPHIA',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE',
    'SAN JUAN',
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]

TRAINING_INTERVAL = range(1961, 2010)
TESTING_INTERVAL = range(2010, 2016)

"""
Begin helper code
"""


class Climate(object):
    """
    The collection of temperature records loaded from given csv file
    """
    def __init__(self, filename):
        """
        Initialize a Climate instance, which stores the temperature records
        loaded from a given csv file specified by filename.

        Args:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',')
        for line in f:
            items = line.strip().split(',')

            date = re.match('(\d\d\d\d)(\d\d)(\d\d)', items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
            self.rawdata[city][year][month][day] = temperature
            
        f.close()

    def get_yearly_temp(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a 1-d pylab array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return pylab.array(temperatures)

    def get_daily_temp(self, city, month, day, year):
        """
        Get the daily temperature for the given city and time (year + date).

        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified time (year +
            date) and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]


def se_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.
    
    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by a linear
            regression model
        model: a pylab array storing the coefficients of a linear regression
            model

    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    var_x = ((x - x.mean())**2).sum()
    SE = pylab.sqrt(EE/(len(x)-2)/var_x)
    return SE/model[0]

"""
End helper code
"""


def generate_models(x, y, degs):
    """
    Generate regression models by fitting a polynomial for each degree in degs
    to points (x, y).

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        degs: a list of degrees of the fitting polynomial

    Returns:
        a list of pylab arrays, where each array is a 1-d array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    models = []
    for degree in degs:
        models.append(pylab.polyfit(x, y, degree))
    return models


def r_squared(y, estimated):
    """
    Calculate the R-squared error term.
    
    Args:
        y: 1-d pylab array with length N, representing the y-coordinates of the
            N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the R-squared error term
    """
    top_eq = ((y - estimated)**2).sum()
    bottom_eq = ((y - y.mean())**2).sum()
    r2 = 1 - top_eq / bottom_eq
    return r2


def evaluate_models_on_training(x, y, models):
    """
    For each regression model, compute the R-squared value for this model with the
    standard error over slope of a linear regression line (only if the model is
    linear), and plot the data along with the best fit curve.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        R-square of your model evaluated on the given data points,
        and SE/slope (if degree of this model is 1 -- see se_over_slope). 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    for model in models:
        p = pylab.poly1d(model)   # setting degree of polynomial
        r2 = r_squared(y, p(x))
        pylab.figure()
        pylab.plot(x, y, 'bo', label='Data Points')
        pylab.plot(x, p(x), 'r-', label='Model')
        pylab.legend(loc='best')
        if len(model) == 2:
            pylab.title(f'Degree of fit: {len(model) - 1} \n R2: {r2} \n Ratio of SE: {se_over_slope(x, y, p(x), model)}.')
        else:
            pylab.title(f'Degree of fit: {len(model) - 1} \n R2: {r2}')
        pylab.xlabel('Year')
        pylab.ylabel('Temperature in Celsius')
        pylab.show()


def gen_cities_avg(climate, multi_cities, years):
    """
    Compute the average annual temperature over multiple cities.

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to average over (list of str)
        years: the range of years of the yearly averaged temperature (list of
            int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the average annual temperature over the given
        cities for a given year.
    """
    multi_temperature_avg = []
    for year in years:
        yearly_temperature = []
        for city in multi_cities:
            yearly_temperature.append(climate.get_yearly_temp(city, year))
        yearly_temperature = pylab.array(yearly_temperature)   # converting list to an array.
        multi_temperature_avg.append(yearly_temperature.mean())
    multi_temperature_avg = pylab.array(multi_temperature_avg) # converting list to an array.
    return multi_temperature_avg


def moving_average(y, window_length):
    """
    Compute the moving average of y with specified window length.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        window_length: an integer indicating the window length for computing
            moving average

    Returns:
        an 1-d pylab array with the same length as y storing moving average of
        y-coordinates of the N sample points
    """
    moved_average = []
    y = pylab.array(y)   # converting list to an array.
    for i in range(len(y)):
        if i < window_length:
            arr_slice = y[:(i + 1)]
            slice_average = arr_slice.sum() / arr_slice.size
            moved_average.append(slice_average)
        else:
            arr_slice = y[(i - window_length + 1):(i + 1)]
            slice_average = arr_slice.sum() / window_length
            moved_average.append(slice_average)
    moved_average = pylab.array(moved_average)   # converting list to an array.
    return moved_average


def rmse(y, estimated):
    """
    Calculate the root mean square error term.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """
    top_eq = ((y - estimated)**2).sum()   # calculating top of equation.
    bottom_eq = len(y)    # calculating bottom of equation.
    rmse_value = math.sqrt((top_eq / bottom_eq))
    return rmse_value


def gen_std_devs(climate, multi_cities, years):
    """
    For each year in years, compute the standard deviation over the averaged yearly
    temperatures for each city in multi_cities. 

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to use in our std dev calculation (list of str)
        years: the range of years to calculate standard deviation for (list of int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the standard deviation of the average annual 
        city temperatures for the given cities in a given year.
    """
    annual_std_dev = []
    for year in years:
        all_cities_yearly_temp = []
        for city in multi_cities:
            yearly_temp = climate.get_yearly_temp(city, year)
            all_cities_yearly_temp.append(yearly_temp)
        all_cities_yearly_temp = pylab.array(all_cities_yearly_temp)   # converting list to an array.
        daily_mean = all_cities_yearly_temp.mean(axis=0)   # calculating mean for each day from all the city arrays.
        std_dev = pylab.std(daily_mean)   # calculating standard deviation across the year.
        annual_std_dev.append(std_dev)
    annual_std_dev = pylab.array(annual_std_dev)   # converting list to an array.
    return annual_std_dev


def evaluate_models_on_testing(x, y, models):
    """
    For each regression model, compute the RMSE for this model and plot the
    test data along with the model’s estimation.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points. 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    for model in models:
        p = pylab.poly1d(model)   # setting degree of polynomial
        rmse_value = rmse(y, p(x))
        pylab.figure()
        pylab.plot(x, y, 'bo', label='Data Points')
        pylab.plot(x, p(x), 'r-', label='Model')
        pylab.legend(loc='best')
        pylab.title(f'Degree of fit: {len(model) - 1} \n RMSE: {rmse_value}')
        pylab.xlabel('Year')
        pylab.ylabel('Temperature in Celsius')
        pylab.show()


if __name__ == '__main__':
    pass
    # Part A.4
    # Problem 4.1 - January 10th, in order to run the code, please uncomment section below.

    # data_file = Climate('data.csv')
    # temperature_data = []
    # for year in TRAINING_INTERVAL:
    #     temperature = data_file.get_daily_temp('NEW YORK', 1, 10, year)
    #     temperature_data.append(temperature)
    # year_data = pylab.array(TRAINING_INTERVAL)
    # temperature_data = pylab.array(temperature_data)
    # temp_model = generate_models(year_data, temperature_data, [1])
    # evaluate_models_on_training(year_data, temperature_data, temp_model)

    # Problem 4.2 - Annual Temperature, in order to run the code, please uncomment section below.

    # data_file = Climate('data.csv')
    # avg_temperature_data = []
    # for year in TRAINING_INTERVAL:
    #     avg_temp = data_file.get_yearly_temp('NEW YORK', year).mean()
    #     avg_temperature_data.append(avg_temp)
    # year_data = pylab.array(TRAINING_INTERVAL)
    # avg_temperature_data = pylab.array(avg_temperature_data)
    # avg_temp_model = generate_models(year_data, avg_temperature_data, [1])
    # evaluate_models_on_training(year_data, avg_temperature_data, avg_temp_model)

    # Part B
    # in order to run the code, please uncomment section below.

    # data_file = Climate('data.csv')
    # all_cities_avg = gen_cities_avg(data_file, CITIES, TRAINING_INTERVAL)
    # year_data = pylab.array(TRAINING_INTERVAL)
    # all_cities_model = generate_models(year_data, all_cities_avg, [1])
    # evaluate_models_on_training(year_data, all_cities_avg, all_cities_model)

    # Part C
    # in order to run the code, please uncomment section below.

    # data_file = Climate('data.csv')
    # all_cities_avg = gen_cities_avg(data_file, CITIES, TRAINING_INTERVAL)
    # year_data = pylab.array(TRAINING_INTERVAL)
    # moved_average_cities = moving_average(all_cities_avg, 5)
    # all_cities_model = generate_models(year_data, moved_average_cities, [1])
    # evaluate_models_on_training(year_data, moved_average_cities, all_cities_model)

    # Part D2
    # in order to run the code, please uncomment section below.

    # data_file = Climate('data.csv')
    # all_cities_avg = gen_cities_avg(data_file, CITIES, TRAINING_INTERVAL)
    # year_data = pylab.array(TRAINING_INTERVAL)
    # all_cities_model = generate_models(year_data, all_cities_avg, [1])
    # year_data_testing = pylab.array(TESTING_INTERVAL)
    # all_cities_avg_testing = gen_cities_avg(data_file, CITIES, TESTING_INTERVAL)
    # evaluate_models_on_testing(year_data_testing, all_cities_avg_testing, all_cities_model)

    # Part D2.I
    # in order to run the code, please uncomment section below.

    # data_file = Climate('data.csv')
    # all_cities_avg = gen_cities_avg(data_file, CITIES, TRAINING_INTERVAL)
    # year_data = pylab.array(TRAINING_INTERVAL)
    # moved_average_cities = moving_average(all_cities_avg, 5)
    # all_cities_models = generate_models(year_data, moved_average_cities, [1, 2, 20])
    # evaluate_models_on_training(year_data, moved_average_cities, all_cities_models)

    # Part D2.II
    # in order to run the code, please uncomment section below and section above
    # keep (evaluate_models_in_training) commented.

    # year_data_testing = pylab.array(TESTING_INTERVAL)
    # all_cities_avg_testing = gen_cities_avg(data_file, CITIES, TESTING_INTERVAL)
    # moved_average_cities_testing = moving_average(all_cities_avg_testing, 5)
    # evaluate_models_on_testing(year_data_testing, moved_average_cities_testing, all_cities_models)

    # Part E
    # in order to run the code, please uncomment section below.

    # data_file = Climate('data.csv')
    # deviation = gen_std_devs(data_file, CITIES, TRAINING_INTERVAL)
    # year_data = pylab.array(TRAINING_INTERVAL)
    # deviation_moved = moving_average(deviation, 5)
    # deviation_models = generate_models(year_data, deviation_moved, [1])
    # evaluate_models_on_training(year_data, deviation_moved, deviation_models)