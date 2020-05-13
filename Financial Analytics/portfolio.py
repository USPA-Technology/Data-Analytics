# -*- coding: utf-8 -*-
"""
@author: Keval
"""
# Import all necessary libraries
import datetime
from finquant.portfolio import build_portfolio
from finquant.efficient_frontier import EfficientFrontier
from finquant.moving_average import compute_ma, ema
import matplotlib
import matplotlib.pylab as plt
matplotlib.rcParams['figure.figsize'] = (20.0, 10.0)

# Start with an empty list names
names = []

# Set new_name to something other than 'exit'.
new_name = ''

# Start a loop that will run until the user enters 'exit'.
while new_name != 'exit':
    # Ask the user for a stock ticker
    new_name = input("Please add stock ticker, or enter 'exit': ")

    # Add the new name to our list
    if new_name != 'exit':
        names.append(new_name)

year = int(input('Enter a year for start date: '))   #year for start date
month = int(input('Enter a month for start date: ')) #month for start date
day = int(input('Enter a day for start date: '))     #day for start date

# use datetime for start_date and end_date
start_date = datetime.datetime(year, month, day)
end_date = datetime.datetime.now()

# Use build_protfolio from finquant with yahoo finance as data api otherwise it will use quandl
pf = build_portfolio(names=names,start_date=start_date, end_date=end_date, data_api="yfinance")

pf.comp_cumulative_returns().plot().axhline(y = 0, color = "black", lw = 3)
plt.title('Cumlative Returns')
plt.show()

# get stock data
x = input("If you want to do moving average for particular data then say 'y' :" )
    
if x in ['y', 'Y', 'yes', 'Yes', 'YES']:
    dis = pf.get_stock(input('Get Stock data for moving average: ')).data.copy(deep=True)
    spans = [10, 50, 100, 150, 200]
    ma = compute_ma(dis, ema, spans, plot=True)
    plt.show()
else:
    print('OK, we will continue to further calculations.....')

print(' ')
print("let's see the result of Monte Carlo Stimulation.....")    
# performs and plots results of Monte Carlo run (5000 iterations)
opt_w, opt_res = pf.mc_optimisation(num_trials=5000)
# plots the results of the Monte Carlo optimisation
pf.mc_plot_results()
# plots the Efficient Frontier
pf.ef_plot_efrontier()
# plots optimal portfolios based on Efficient Frontier
pf.ef.plot_optimal_portfolios()
# plots individual plots of the portfolio
pf.plot_stocks()
plt.show()

print(' ')
print('optimised portfolio results')
# creating an instance of EfficientFrontier
ef = EfficientFrontier(pf.comp_mean_returns(freq=1), pf.comp_cov())
# optimisation for minimum volatility
print(ef.minimum_volatility())

# printing out relevant quantities of the optimised portfolio
(expected_return, volatility, sharpe) = ef.properties(verbose=True)

results = str(ef.minimum_volatility())

y = input("If you want to save results then say 'y' :" )

if y in  ['y', 'Y', 'yes', 'Yes', 'YES']:
    text_file = open('output.txt', 'w')
    text_file.write(results)
    text_file.close()
    print('saved in output.txt')
else:
    print("your current result is not saved")