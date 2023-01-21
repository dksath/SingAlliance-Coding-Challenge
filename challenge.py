import requests
from datetime import datetime, timedelta
import time
import pandas as pd
import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt
from builtins import dict

# set the size for each request
size = 2000

# set the start and end date
start_date = datetime.fromisoformat("2022-11-01T00:00:00+00:00")
end_date = datetime.fromisoformat("2022-12-01T23:00:00+00:00")

# create a list of symbols
symbols = ["btcusdt", "ethusdt", "ltcusdt"]

# create an empty dictionary to store the dataframes
dataframes = {}

# loop over the symbols
for symbol in symbols:
    # initialize an empty list to store the data
    data = []
    # set the current date range to start from the start date
    current_start = start_date
    # loop until the current end date is less than the end date
    while current_start < end_date:
        # set the current end date as the current start date + 1 hour
        current_end = current_start + timedelta(hours=1)
        # make sure the current end date is not greater than the end date
        if current_end > end_date:
            current_end = end_date
        from_time = int(current_start.timestamp())*1000
        to_time = int(current_end.timestamp())*1000
        url = f"https://api.huobi.pro/market/history/kline?symbol={symbol}&period=60min&from={from_time}&to={to_time}&size={size}"

        # print loading message
        print(f"Loading data for {symbol} from {current_start} to {current_end}...")

        # make the API request
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.reason}")
        else:
            # add the data to the list
            data.extend(response.json()['data'])
            # update the current start date
            current_start = current_end

    # create the dataframe from the list of data
    dataf = pd.DataFrame(data)
    dataframes[symbol] = dataf

df = pd.DataFrame()
df['BTC'] = dataframes['btcusdt'][['close']]
df['ETH'] = dataframes['ethusdt'][['close']]
df['LTC'] = dataframes['ltcusdt'][['close']]

#create hourly returns for each token
df = df.pct_change().dropna()

#create expected return for each asset
expected_returns = df.mean()


# Calculate the covariance matrix of the tokens
cov_matrix = df.cov()


# Define the optimization function
def portfolio_optimization(x):
    return -np.dot(x, expected_returns) / np.sqrt(np.dot(np.dot(x, cov_matrix), x))

# Define the constraints of the optimization problem
constraints = [{'type': 'eq', 'fun': lambda x: np.sum(x) - 1}]

# Define the bounds of the optimization problem
bounds = [(0, 1) for i in range(len(expected_returns))]

# Run the optimization
initial_guess = np.ones(len(expected_returns)) / len(expected_returns)
result = minimize(portfolio_optimization, initial_guess, bounds=bounds, constraints=constraints)

#print a dictionary of the weights of each token
print(dict(zip(expected_returns.index, result.x)))


# Run the optimization for different target returns
target_returns = np.linspace(expected_returns.min(), expected_returns.max(), 100)
portfolios = []
for target_return in target_returns:
    constraints = [{'type': 'eq', 'fun': lambda x: np.sum(x) - 1},
                   {'type': 'eq', 'fun': lambda x: np.dot(x, expected_returns) - target_return}]
    result2 = minimize(portfolio_optimization, np.ones(len(expected_returns))/len(expected_returns), bounds=bounds, constraints=constraints)
    portfolios.append(result2.x)

# Plot the efficient frontier
portfolios = np.array(portfolios)
portfolio_std = []
portfolio_return = []
for i in range(portfolios.shape[0]):
    portfolio_std.append(np.sqrt(np.dot(portfolios[i], np.dot(cov_matrix, portfolios[i].T))))
    portfolio_return.append(np.dot(portfolios[i], expected_returns))

plt.scatter(portfolio_std, portfolio_return)
plt.xlabel('Standard Deviation')
plt.ylabel('Expected Return')


# find the index of the portfolio with minimum volatility
min_vol_index = portfolio_std.index(min(portfolio_std))
# find the index of the optimal portfolio
max_ret_index = portfolio_return.index(max(portfolio_return))

# add marker for the optimal portfolio
plt.annotate("Optimal portfolio", (portfolio_std[max_ret_index], portfolio_return[max_ret_index]),
             xytext=(10, 30), textcoords='offset points',
             arrowprops=dict(arrowstyle="->",
                             connectionstyle="arc3,rad=.2"))
# add marker for the minimum volatility portfolio
plt.annotate("Minimum volatility portfolio", (portfolio_std[min_vol_index], portfolio_return[min_vol_index]),
             xytext=(10, 30), textcoords='offset points',
             arrowprops=dict(arrowstyle="->",
                             connectionstyle="arc3,rad=.2"))

plt.savefig('efficient_frontier.png')
plt.show()

