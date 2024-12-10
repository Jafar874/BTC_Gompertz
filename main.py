from utils import *
from __init__ import b, c
from datetime import datetime, timedelta

if __name__ == "__main__":
    # User Input
    days_since_inception = float(input("Enter the number of days since Bitcoin's inception to estimate its price: "))

    # Estimate Price
    price = model(days_since_inception, b, c)

    # Output
    inception_date = datetime(2009, 1, 3)
    day = inception_date + timedelta(days=days_since_inception)
    print(f'The Bitcoin Price at {day.strftime('%B %d, %Y')} is estimated to be {int(price)} USD')






