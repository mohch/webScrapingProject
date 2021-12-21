import os

import requests
from bs4 import BeautifulSoup
import pandas as pd
from tabulate import tabulate
from termcolor import colored
from typing import Final

FILE_PATH: Final = os.curdir + '/stock_data.csv'
STOCK_GAIN_WEB_URL: Final = 'https://www.moneycontrol.com/stocks/marketstats/nsegainer/index.php'
STOCK_LOSS_WEB_URL: Final = 'https://www.moneycontrol.com/stocks/marketstats/nseloser/index.php'


def get_table_from_web_HTML(url: str, attr: dict = None) -> object:
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    return soup.find('div', attrs=attr)


def get_raw_table_headers(table: object, exclude_headers_start_with_list: tuple = None) -> []:
    res_headers = []
    for i in table.find_all('th'):
        title = i.text.strip()
        if not title.startswith(exclude_headers_start_with_list):
            res_headers.append(title)
    return res_headers


def populate_data_from_raw_html_table(table: object, data: pd.DataFrame, prev_data: pd.DataFrame) -> pd.DataFrame:
    for j in table.find_all('tr')[1:]:
        row_data = j.find_all('td')
        if len(row_data) > 0 and row_data[0].find('a') is not None:
            row = [row_data[0].find('a').text]
            row += [i.text for i in row_data[1:len(headers) - 1]]
            length = len(data)
            if prev_data is not None and len(row) >= 3:
                prev_price_pd = prev_data.query('`Company Name` == @row[0]')
                if prev_price_pd is not None and len(prev_price_pd["Last Price"].values.tolist()) > 0:
                    val, color = find_actual_gain_loss(prev_price_pd, row)
                    row += [colored(str(val) + "%", color)]
                else:
                    row += [colored("New Entrant", "blue")]
            else:
                row += [colored("New Entrant", "blue")]
            data.loc[length] = row
    return data


def find_actual_gain_loss(prev_price_pd: pd.DataFrame, row: []) -> tuple:
    prev_price = float(prev_price_pd["Last Price"].values.tolist()[0].replace(',', ''))
    curr_price = float(row[3].replace(',', ''))
    if curr_price > prev_price:
        val = (((prev_price - prev_price) / prev_price) * 100)
        color = "green"
    elif curr_price == prev_price:
        val = 0.0
        color = "blue"
    else:
        val = (((prev_price - curr_price) / prev_price) * 100)
        color = "red"
    return val, color


def preety_print(data: pd.DataFrame):
    print(tabulate(data, headers='keys', tablefmt='psql'))


if __name__ == '__main__':

    prev_stock_data = None
    if os.path.exists(FILE_PATH):
        prev_stock_data = pd.read_csv(FILE_PATH)

    gainTable = get_table_from_web_HTML(STOCK_GAIN_WEB_URL, {"class": "bsr_table hist_tbl_hm"})
    lossTable = get_table_from_web_HTML(STOCK_LOSS_WEB_URL, {"class": "bsr_table hist_tbl_hm"})

    exclude_headers_start_with = ("5 Day Performance", "% Loss")
    headers = get_raw_table_headers(gainTable, exclude_headers_start_with)
    headers.append("Gain/lost since last run")

    stockData = pd.DataFrame(columns=headers)
    populate_data_from_raw_html_table(gainTable, stockData, prev_stock_data)
    populate_data_from_raw_html_table(lossTable, stockData, prev_stock_data)

    preety_print(stockData)

    # Export to csv
    stockData.to_csv(FILE_PATH, index=False)
