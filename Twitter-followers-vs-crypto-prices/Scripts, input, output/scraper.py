# --------------------------------------------------------------------------------------------------------------
# scraper.py:
# Scrapes data on Twitter followers and cryptocurrency prices and exports to csv, pickled pandas dataframe,
# or to SQL database for further analysis

# GitHub project link:
# https://github.com/antonshpak100/Data-Analysis-Portfolio/tree/main/Twitter-followers-vs-crypto-prices
# --------------------------------------------------------------------------------------------------------------

# importing libraries
from selenium import webdriver
from bs4 import BeautifulSoup
import datetime as dt
import re
import pandas as pd
from sqlalchemy import create_engine


# parseWebpage: parses the specified webpage using BeautifulSoup through selenium browser automation
def parseWebpage(URL):
    print("\rReading webpage: "+URL, end="")
    driver = webdriver.Chrome()
    driver.get(URL)
    html = driver.page_source
    driver.close()
    soup = BeautifulSoup(html, features="html.parser")
    print("\rComplete.", end="")
    return soup


# scrapeDates: retrieves the dates listed on a specified SocialBlade page
def scrapeDates(URL):
    dates = []
    soup = parseWebpage(URL)
    for item in soup.find_all("div", {"style": "width: 80px; float: left;"}):
        dates.append(dt.datetime.strptime(item.contents.pop(), '%Y-%m-%d').date())
    dates.pop(0) # removing first day since there are no new followers recorded for this date
    dates.pop()  # removing value for current date as this corresponds to the "live" follower count which we don't want
    return dates


# scrapeFollowers: retrieves total and new follower counts for each day on a specified SocialBlade page
def scrapeFollowers(twitter):
    URL = "https://socialblade.com/twitter/user/" + twitter + "/monthly"
    soup = parseWebpage(URL)
    n = 1
    totalFollowers = []
    for item in soup.find_all("div", {"style": "width: 120px; float: left;"}):
        if n % 2 == 0 and 2 < n < 60:
            totalFollowers.append(
                re.findall("\d+", str(item.contents).replace("[", "").replace("]", "").replace(",", "")).pop())
        n += 1
    n = 1
    newFollowers = []
    for item in soup.find_all("div", {"style": "width: 100px; float: left;"}):
        if 1 < n < 30:
            newFollowers.append(re.findall("((?:(?<=\+)\d+|-)\d*)", str(item.contents).replace(",", "")).pop())
        n += 1
    return totalFollowers, newFollowers


# scrapePrices: retrieves crypto prices from specified investing.com page
def scrapePrices(crypto):
    URL = "https://www.investing.com/crypto/" + crypto + "/historical-data"
    soup = parseWebpage(URL)
    n = 1
    prices = []
    for item in soup.find_all("td"):
        if n % 7 == 2 and 15 < n < 206:
            prices = [float(item.contents.pop().replace(",", ""))] + prices
            # (since prices are listed from newest to oldest, I grow the list in reverse)
        n += 1
    return prices


# main: executes program
def main():

    # Specifying what kind of outputs I want
    exportPickledDataframe = True
    exportCSVs = True
    exportToSQL = False  # Set up SQL database first and link the database on line 139 if setting this to True

    # Retrieving list of dates
    dates = scrapeDates("https://socialblade.com/twitter/user/elonmusk/monthly")

    # Creating pandas dataframe for crypto prices
    cryptoListFile = open("./Inputs/crypto-list.txt", "r")
    cryptos = cryptoListFile.readlines()
    cryptoListFile.close()
    cryptos = [x.strip() for x in cryptos]
    cryptoPricesDF = pd.DataFrame.from_dict({})
    cryptoPricesDF["Date"] = dates
    cryptoPricesDF = cryptoPricesDF.set_index("Date")
    for crypto in cryptos:
        cryptoPricesDF[crypto] = scrapePrices(crypto)

    # Creating pandas dataframes for total twitter followers and new twitter followers
    # reading list of twitters from txt file
    twitterListFile = open("./Inputs/twitter-list.txt", "r")
    twitters = twitterListFile.readlines()
    twitterListFile.close()
    twitters = [x.strip() for x in twitters]

    totalFollowersDF = pd.DataFrame.from_dict({})
    totalFollowersDF["Date"] = dates
    totalFollowersDF = totalFollowersDF.set_index("Date")
    newFollowersDF = pd.DataFrame.from_dict({})
    newFollowersDF["Date"] = dates
    newFollowersDF = newFollowersDF.set_index("Date")

    n = 0
    for twitter in twitters:
        totalFollowers, newFollowers = scrapeFollowers(twitter)
        totalFollowersDF[twitter] = totalFollowers
        newFollowersDF[twitter] = newFollowers
        n+=1
    newFollowersDF = newFollowersDF.replace("-", 0)
    newFollowersDF = newFollowersDF.astype("int")
    totalFollowersDF = totalFollowersDF.astype("int")

    # Exporting pandas dataframes to byte stream via pickling
    if exportPickledDataframe == True:
        cryptoPricesDF.to_pickle("./Data/pickled-data/cryptoPricesDF.pkl")
        totalFollowersDF.to_pickle("./Data/pickled-data/totalFollowersDF.pkl")
        newFollowersDF.to_pickle("./Data/pickled-data/newFollowersDF.pkl")

    # Exporting dataframes as CSV
    if exportCSVs == True:
        cryptoPricesDF.to_csv("./Data/csv-data/cryptoPrices.csv")
        totalFollowersDF.to_csv("./Data/csv-data/totalFollowers.csv")
        newFollowersDF.to_csv("./Data/csv-data/newFollowers.csv")

    # Exporting dataframes to SQL:
    if exportToSQL == True:
        # Note: the specified SQL database must be set up first
        # Note: PASSWORD, HOSTNAME, and DATABASE are placeholders, specify the intended database if exporting to SQL
        # Create SQLAlchemy engine to connect to MySQL Database
        engine = create_engine("mysql+pymysql://root:PASSWORD@HOSTNAME/DATABASE")
        # Convert dataframe to sql table
        # Note: make sure that no tables with these names already exist in the database
        cryptoPricesDF.to_sql('cryptoPrices', engine)
        totalFollowersDF.to_sql('totalFollowers', engine)
        newFollowersDF.to_sql('newFollowers', engine)

# executing program
if __name__ == "__main__":
    main()
