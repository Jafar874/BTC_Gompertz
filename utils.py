import numpy as np
import pandas as pd

def load_data(path='./data/btc-usd-max.csv'):
    data = pd.read_csv(path)
    return data
    

def preprocess_data(data):
    # Make dates to datetime
    data['date'] = pd.to_datetime(data['snapped_at'])
    # Remove Timezones
    data['date'] = data['date'].dt.tz_localize(None)
    # Transform data to days since inception (Jan-03-2009)
    data['days_since_inception'] = (data['date'] - pd.Timestamp('2009-01-03')).dt.days
    # Transform price to log scale (base 10)
    data['price_log10'] = np.log10(data['price'].values)
    return data


def select_data(data):
    price_log10 = data['price_log10'].values
    days_since_inception = data['days_since_inception'].values
    price = data['price'].values
    return days_since_inception, price_log10, price
    

def get_data(path='./data/btc-usd-max.csv'):
    data = load_data(path)
    data = preprocess_data(data)
    days_since_inception, price_log10, price = select_data(data)
    return days_since_inception, price_log10, price


def model(t, b, c):
    """
    Gompertz function: a * np.exp(-b * np.exp(-c * t))
    a is an asymptote
    b sets the displacement along the x-axis 
    c sets the growth rate

    Exponential growth: np.exp(r * t)
    r sets the growth reate

    Bitcoin Gompertz Model: L * np.exp(r * t - b * np.exp(-c * t))
    Product of the Gompertz function with exponential growth
    a is the estimated world assets in 2009 in USD
    r is estimated as the daily world asset growth between 2009 and 2024

    """
    annual_growth = 0.058 # Estimated annual world asset growth between 2009 and 2024
    r = np.log(1+annual_growth)/365 # daily growth
    a = 1e7 # Estimated world assets in 2009 in USD
    return a * np.exp(r * t - b * np.exp(-c * t))


def log10_transform(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        try:
            return np.log10(result)
        except ValueError as e:
            raise ValueError(f"Error applying np.log10 to the output of {func.__name__}: {e}")
    return wrapper