# Web Scraping Python Requirements
Task is to fetch/scrape data from website (www.moneycontrol.com) and print according to below 
A python/node script will run and should get the Nifty top gainers and losers from the website. 

**Print all details like below for each table of gainers and losers :** 

| Company Name | High Low | Last Price | Prev Close | Change | % Gain | Gain/lost since last run |

**Setup:**
1. Need python 3.9 and pip installed
2. Have used virtualEnv
3. $ pip install -r requirements.txt

**Constants:**

1. FILE_PATH = os.curdir + '/stock_data.csv'
2. STOCK_GAIN_WEB_URL = 'https://www.moneycontrol.com/stocks/marketstats/nsegainer/index.php'
3. STOCK_LOSS_WEB_URL = 'https://www.moneycontrol.com/stocks/marketstats/nseloser/index.php'

**Run:**

$ python main.py

**Note:** Previous stock data will accessible in stock_data.csv file in root dir
