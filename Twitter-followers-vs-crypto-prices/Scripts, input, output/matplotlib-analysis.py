# --------------------------------------------------------------------------------------------------------------
# matplotlib-analysis.py:
# Analyzes data on Twitter followers and cryptocurrency prices from pickled pandas dataframe given by scraper.py, and
# saves plots and figures as images

# GitHub project link:
# https://github.com/antonshpak100/Data-Analysis-Portfolio/tree/main/Twitter-followers-vs-crypto-prices
# --------------------------------------------------------------------------------------------------------------

# importing libraries
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mpc


# reset: clears the figure, resets the axes and figure parameters
def reset():
    plt.clf()
    fig, ax = plt.subplots()
    fig.set_size_inches(12, 6.75)
    plt.tick_params(length=5)
    return fig, ax


# rescaleDF: rescales each column of a dataframe so that 1 represents the starting value and the following
# values become the ratio of the value to the starting value.
def rescaleDF(originalDF):
    rescaledDF = originalDF.copy()
    for i in range(len(originalDF.columns)):
        rescaledDF.iloc[:, i] = rescaledDF.iloc[:, i] / rescaledDF.iloc[0, i]
    return rescaledDF


# normalizeDF: rescales each column of a dataframe so that 1 represents the maximum value and 0 represents the
# minimum value.
def normalizeDF(originalDF):
    normalizedDF = originalDF.copy()
    for i in range(len(originalDF.columns)):
        normalizedDF.iloc[:, i] = \
            (normalizedDF.iloc[:, i] - normalizedDF.iloc[:, i].min()) / \
            (normalizedDF.iloc[:, i].max() - normalizedDF.iloc[:, i].min())
    return normalizedDF


# main: executes program
def main():

    # Importing raw data tables from pickle
    cryptoPricesDF = pd.read_pickle("./Data/pickled-data/cryptoPricesDF.pkl")
    totalFollowersDF = pd.read_pickle("./Data/pickled-data/totalFollowersDF.pkl")
    newFollowersDF = pd.read_pickle("./Data/pickled-data/newFollowersDF.pkl")

    # Each of the blocks below generates a plot which is saved as an image in the 'Figures' folder.
    # The blocks are intended to function by themselves if necessary.
    # i.e, if only one plot is needed, all others can be commented out without issues.

    #  Plotting total followers
    # --------------------------------------------------------------------------------------------------------------
    fig, ax = reset()
    # sorting each column: this is done so that the legend shows the 5 largest-valued columns
    sortedTotalFollowersDF = totalFollowersDF.sort_values(by=[totalFollowersDF.index[-1]], axis=1, ascending=False)
    ax.plot(sortedTotalFollowersDF)
    ax.legend(sortedTotalFollowersDF.columns[:5])
    ax.set_title("Total Twitter followers by username")
    ax.set_xlabel("Date (from Aug. 15 to Sep. 11)")
    ax.set_xticks(range(19219, 19221 + len(totalFollowersDF) - 2, 7))
    ax.set_xticks(totalFollowersDF.index, minor=True)
    ax.set_ylabel("Total followers")
    fig.savefig('./Figures/' + ax.get_title() + '.png', dpi=200)
    # --------------------------------------------------------------------------------------------------------------

    # Plotting new followers
    # --------------------------------------------------------------------------------------------------------------
    fig, ax = reset()
    # sorting each column: this is done so that the legend shows the 5 largest-valued columns
    sortedNewFollowersDF = newFollowersDF.sort_values(by=[newFollowersDF.index[-1]], axis=1, ascending=False)
    ax.plot(sortedNewFollowersDF)
    ax.legend(sortedNewFollowersDF.columns[:5])
    ax.set_title("Daily new Twitter followers by username")
    ax.set_xlabel("Date (from Aug. 15 to Sep. 11)")
    ax.set_xticks(range(19219, 19221 + len(newFollowersDF) - 2, 7))
    ax.set_xticks(newFollowersDF.index, minor=True)
    ax.set_ylabel("New followers")
    fig.savefig('./Figures/' + ax.get_title() + '.png', dpi=200)
    # --------------------------------------------------------------------------------------------------------------

    # Plotting total followers relative to followers on 2022-08-15
    # --------------------------------------------------------------------------------------------------------------
    fig, ax = reset()
    # sorting each column: this is done so that the legend shows the 5 largest-valued columns
    sortedRescaledTotalFollowersDF = rescaleDF(totalFollowersDF).\
        sort_values(by=[totalFollowersDF.index[-1]], axis=1, ascending=False)
    ax.plot(sortedRescaledTotalFollowersDF)
    ax.legend(sortedRescaledTotalFollowersDF.columns[:5])
    ax.set_title("Total followers relative to followers on 2022-08-15")
    ax.set_xlabel("Date (from Aug. 15 to Sep. 11)")
    ax.set_xticks(range(19219, 19221 + len(totalFollowersDF) - 2, 7))
    ax.set_xticks(totalFollowersDF.index, minor=True)
    ax.set_ylabel("Ratio of total followers to total followers on 2022-08-15")
    fig.savefig('./Figures/' + ax.get_title() + '.png', dpi=200)
    # --------------------------------------------------------------------------------------------------------------

    # Plotting daily new followers relative to new followers on 2022-08-15
    # --------------------------------------------------------------------------------------------------------------
    fig, ax = reset()
    # sorting each column: this is done so that the legend shows the 5 largest-valued columns
    sortedRescaledNewFollowersDF = rescaleDF(newFollowersDF). \
        sort_values(by=[newFollowersDF.index[-1]], axis=1, ascending=False)
    ax.plot(sortedRescaledNewFollowersDF)
    ax.legend(sortedRescaledNewFollowersDF.columns[:5])
    ax.set_title("Daily new followers relative to new followers on 2022-08-15")
    ax.set_xlabel("Date (from Aug. 15 to Sep. 11)")
    ax.set_xticks(range(19219, 19221 + len(newFollowersDF) - 2, 7))
    ax.set_xticks(newFollowersDF.index, minor=True)
    ax.set_ylabel("Ratio of new followers to new followers on 2022-08-15")
    fig.savefig('./Figures/' + ax.get_title() + '.png', dpi=200)
    # --------------------------------------------------------------------------------------------------------------

    # Plotting cryptocurrency prices relative to price on 2022-08-15
    # --------------------------------------------------------------------------------------------------------------
    fig, ax = reset()
    ax.plot(rescaleDF(cryptoPricesDF))
    ax.legend(cryptoPricesDF.columns)
    ax.set_title("Cryptocurrency prices relative to price on 2022-08-15")
    ax.set_xlabel("Date (from Aug. 15 to Sep. 11)")
    ax.set_xticks(range(19219, 19221 + len(cryptoPricesDF) - 2, 7))
    ax.set_xticks(cryptoPricesDF.index, minor=True)
    ax.set_ylabel("Ratio of price to price on 2022-08-15")
    fig.savefig('./Figures/' + ax.get_title() + '.png', dpi=200)
    # --------------------------------------------------------------------------------------------------------------

    # Plotting relative total followers and relative crypto prices on same graph
    # --------------------------------------------------------------------------------------------------------------
    fig, ax = reset()
    # plotting relative total followers
    ax.plot(rescaleDF(totalFollowersDF), c="r", alpha=0.5)
    ax.set_title("Change in total followers vs change in crypto prices")
    ax.set_xlabel("Date (from Aug. 15 to Sep. 11)")
    ax.set_ylabel("Ratio of total followers to total followers on 2022-08-15")
    ax.set_ylim(1-0.006*max(ax.get_ylim()), 1+0.06*max(ax.get_ylim()))
    ax.legend(["Total followers"], loc=2)
    # plotting relative crypto prices
    ax2 = ax.twinx()
    ax2.plot(rescaleDF(cryptoPricesDF), c="b", alpha=0.75)
    ax2.set_xticks(range(19219, 19221 + len(cryptoPricesDF) - 2, 7))
    ax2.set_xticks(cryptoPricesDF.index, minor=True)
    ax2.set_ylabel("Ratio of price to price on 2022-08-15")
    ax2.set_ylim(1-0.1*max(ax2.get_ylim()), 1+max(ax2.get_ylim()))
    ax2.legend(["Cryptocurrency prices"], loc=1)
    # saving figure
    fig.savefig('./Figures/' + ax.get_title() + '.png', dpi=200)
    # --------------------------------------------------------------------------------------------------------------

    # Plotting normalized graph of total followers
    # --------------------------------------------------------------------------------------------------------------
    fig, ax = reset()
    ax.plot(normalizeDF(totalFollowersDF))
    ax.set_title("Normalized graph of total followers for each user")
    ax.set_xlabel("Date (from Aug. 15 to Sep. 11)")
    ax.set_xticks(range(19219, 19221 + len(totalFollowersDF) - 2, 7))
    ax.set_xticks(totalFollowersDF.index, minor=True)
    ax.set_ylabel("0 represents minimum and 1 represents maximum")
    fig.savefig('./Figures/' + ax.get_title() + '.png', dpi=200)
    # --------------------------------------------------------------------------------------------------------------

    # Plotting normalized graph of new followers
    # --------------------------------------------------------------------------------------------------------------
    fig, ax = reset()
    ax.plot(normalizeDF(newFollowersDF))
    ax.set_title("Normalized graph of daily new followers for each user")
    ax.set_xlabel("Date (from Aug. 15 to Sep. 11)")
    ax.set_xticks(range(19219, 19221 + len(newFollowersDF) - 2, 7))
    ax.set_xticks(newFollowersDF.index, minor=True)
    ax.set_ylabel("0 represents minimum and 1 represents maximum")
    fig.savefig('./Figures/' + ax.get_title() + '.png', dpi=200)
    # --------------------------------------------------------------------------------------------------------------

    # Plotting normalized graph of crypto prices
    # --------------------------------------------------------------------------------------------------------------
    fig, ax = reset()
    ax.plot(normalizeDF(cryptoPricesDF))
    ax.legend(cryptoPricesDF.columns)
    ax.set_title("Normalized graph of cryptocurrency prices")
    ax.set_xlabel("Date (from Aug. 15 to Sep. 11)")
    ax.set_xticks(range(19219, 19221 + len(cryptoPricesDF) - 2, 7))
    ax.set_xticks(cryptoPricesDF.index, minor=True)
    ax.set_ylabel("0 represents minimum and 1 represents maximum")
    fig.savefig('./Figures/' + ax.get_title() + '.png', dpi=200)
    # --------------------------------------------------------------------------------------------------------------

    # Plotting correlation matrix of total followers and crypto prices
    # --------------------------------------------------------------------------------------------------------------
    fig, ax = reset()
    # creating and plotting the correlation matrix
    matrix = (cryptoPricesDF.corrwith(totalFollowersDF.iloc[:, 0]).to_frame())
    matrix.columns = totalFollowersDF.columns[:1]
    for n in totalFollowersDF.columns:
        matrix[n] = (cryptoPricesDF.corrwith(totalFollowersDF[n]))
    cax = ax.matshow(matrix, vmin=-1, vmax=1)
    ax.set_xticks(range(len(totalFollowersDF.columns)))
    ax.set_xticklabels(totalFollowersDF.columns)
    ax.set_title("Correlation matrix - total followers vs crypto prices")
    plt.xticks(rotation=90)
    ax.set_yticks(range(len(cryptoPricesDF.columns)))
    ax.set_yticklabels(cryptoPricesDF.columns)
    ax.tick_params(axis='both', which='major', labelsize=5)
    # creating colorbar
    cb = fig.colorbar(cax, ax=ax, ticks=[-1, -0.5, 0, 0.5, 1], orientation="horizontal")
    # saving figure and removing the colorbar so that it doesn't interfere with the next plot
    fig.savefig('./Figures/' + ax.get_title() + '.png', dpi=200)
    cb.remove()
    # --------------------------------------------------------------------------------------------------------------

    # Stratified correlation matrix of relative total followers and relative crypto prices
    # --------------------------------------------------------------------------------------------------------------
    fig, ax = reset()
    # creating the correlation matrix
    matrix = (cryptoPricesDF.corrwith(totalFollowersDF.iloc[:, 0]).to_frame())
    matrix.columns = totalFollowersDF.columns[:1]
    # creating a custom colormap for the correlation matrix plot that divides the correlations more sharply
    for n in totalFollowersDF.columns:
        matrix[n] = (cryptoPricesDF.corrwith(totalFollowersDF[n]))
    cdict = {'red': [(0, 0, 64 / 255),
                     (0.125, 64 / 255, 70 / 255),
                     (0.875, 70 / 255, 249 / 255),
                     (1, 249 / 255, 0)],
             'green': [(0, 0, 17 / 255),
                       (0.125, 17 / 255, 142 / 255),
                       (0.875, 142 / 255, 232 / 255),
                       (1, 232 / 255, 0)],
             'blue': [(0, 0, 81 / 255),
                      (0.125, 81 / 255, 140 / 255),
                      (0.875, 140 / 255, 85 / 255),
                      (1, 85 / 255, 0)]}
    stratifiedCmap = mpc.LinearSegmentedColormap("", cdict)
    # plotting the correlation matrix
    cax = ax.matshow(matrix, vmin=-1, vmax=1, cmap=stratifiedCmap)
    ax.set_xticks(range(len(totalFollowersDF.columns)))
    ax.set_xticklabels(totalFollowersDF.columns)
    ax.set_title("Correlation matrix - total followers vs crypto prices (stratified)")
    plt.xticks(rotation=90)
    ax.set_yticks(range(len(cryptoPricesDF.columns)))
    ax.set_yticklabels(cryptoPricesDF.columns)
    ax.tick_params(axis='both', which='major', labelsize=5)
    # creating colorbar
    cb = fig.colorbar(cax, ax=ax, ticks=[-1, -0.75, 0, 0.75, 1], orientation="horizontal")
    # saving figure and removing the colorbar so that it doesn't interfere with the next plot
    fig.savefig('./Figures/' + ax.get_title() + '.png', dpi=200)
    cb.remove()
    # --------------------------------------------------------------------------------------------------------------

    # Correlation matrix of new followers and crypto price
    # --------------------------------------------------------------------------------------------------------------
    fig, ax = reset()
    # creating and plotting the correlation matrix
    matrix = (cryptoPricesDF.corrwith(newFollowersDF.iloc[:, 0]).to_frame())
    matrix.columns = newFollowersDF.columns[:1]
    for n in newFollowersDF.columns:
        matrix[n] = (cryptoPricesDF.corrwith(newFollowersDF[n]))
    cax = ax.matshow(matrix, vmin=-1, vmax=1)
    ax.set_xticks(range(len(newFollowersDF.columns)))
    ax.set_xticklabels(newFollowersDF.columns)
    ax.set_title("Correlation matrix - daily new followers vs crypto prices")
    plt.xticks(rotation=90)
    ax.set_yticks(range(len(cryptoPricesDF.columns)))
    ax.set_yticklabels(cryptoPricesDF.columns)
    ax.tick_params(axis='both', which='major', labelsize=5)
    # creating colorbar
    cb = fig.colorbar(cax, ax=ax, ticks=[-1, -0.5, 0, 0.5, 1], orientation="horizontal")
    # saving figure and removing the colorbar so that it doesn't interfere with the next plot
    fig.savefig('./Figures/' + ax.get_title() + '.png', dpi=200)
    cb.remove()
    # --------------------------------------------------------------------------------------------------------------

    # Bar graph of time-shifted average correlations for crypto prices and total followers
    # --------------------------------------------------------------------------------------------------------------
    fig, ax = reset()
    # creating bars from average correlations
    barHeights = []
    for i in range(-7, 8):
        # creating correlation matrix
        matrix = (cryptoPricesDF.shift(i).corrwith(totalFollowersDF.iloc[:, 0]).to_frame())
        matrix.columns = newFollowersDF.columns[:1]
        for n in totalFollowersDF.columns:
            matrix[n] = (cryptoPricesDF.shift(i).corrwith(totalFollowersDF[n]))
        # calculating and appending mean value of correlation matrix as bar heigh
        barHeights.append(matrix.mean().mean())
    # plotting bars
    plt.bar(range(-7, 8), barHeights)
    ax.set_title("Correlation between crypto prices and total followers shifted by date")
    ax.set_xlabel("Days crypto prices behind total followers")
    ax.set_xticks(range(-7, 8))
    ax.set_ylabel("Average correlation")
    ax.set_yticks([x/4 for x in range(-4, 5)])
    fig.savefig('./Figures/' + ax.get_title() + '.png', dpi=200)
    # --------------------------------------------------------------------------------------------------------------

    # Bar graph of time-shifted average correlations for crypto prices and new followers
    # --------------------------------------------------------------------------------------------------------------
    fig, ax = reset()
    # creating bars from average correlations
    barHeights = []
    for i in range(-7, 8):
        # creating correlation matrix
        matrix = (cryptoPricesDF.shift(i).corrwith(newFollowersDF.iloc[:, 0]).to_frame())
        matrix.columns = newFollowersDF.columns[:1]
        for n in newFollowersDF.columns:
            matrix[n] = (cryptoPricesDF.shift(i).corrwith(newFollowersDF[n]))
        # calculating and appending mean value of correlation matrix as bar heigh
        barHeights.append(matrix.mean().mean())
    # plotting bars
    plt.bar(range(-7, 8), barHeights)
    ax.set_title("Correlation between crypto prices and daily new followers shifted by date")
    ax.set_xlabel("Days crypto prices behind new followers")
    ax.set_xticks(range(-7, 8))
    ax.set_ylabel("Average correlation")
    ax.set_yticks([x/4 for x in range(-4, 5)])
    fig.savefig('./Figures/' + ax.get_title() + '.png', dpi=200)
    # --------------------------------------------------------------------------------------------------------------

    # Plotting total followers relative to followers on 2022-08-15 - comparing small and large accounts
    # --------------------------------------------------------------------------------------------------------------
    fig, ax = reset()
    # selecting accounts with less than 100,000 starting followers and plotting them
    lessThan100kList = totalFollowersDF[totalFollowersDF.iloc[:1] < 10 ** 6].dropna(axis=1, how='all').columns
    lessThan100k = ax.plot(rescaleDF(totalFollowersDF[lessThan100kList]), "r", alpha=0.5,
                           label="Accounts with < 100,000 followers")
    # selecting accounts with more than 100,000 starting followers and plotting them
    moreThan100kList = totalFollowersDF[totalFollowersDF.iloc[:1] > 10 ** 6].dropna(axis=1, how='all').columns
    moreThan100k = ax.plot(rescaleDF(totalFollowersDF[moreThan100kList]), "b", alpha=0.75,
                           label="Accounts with > 100,000 followers")
    ax.legend(handles=[lessThan100k[0], moreThan100k[0]], loc=9, framealpha=0.9)
    ax.set_title("Total followers relative to followers on 2022-08-15 - small accounts vs large accounts")
    ax.set_xlabel("Date (from Aug. 15 to Sep. 11)")
    ax.set_xticks(range(19219, 19221 + len(totalFollowersDF) - 2, 7))
    ax.set_xticks(totalFollowersDF.index, minor=True)
    ax.set_ylabel("Ratio of total followers to total followers on 2022-08-15")
    fig.savefig('./Figures/' + ax.get_title() + '.png', dpi=200)
    # --------------------------------------------------------------------------------------------------------------

    # Plotting new followers relative to followers on 2022-08-15 - comparing small and large accounts
    # --------------------------------------------------------------------------------------------------------------
    fig, ax = reset()
    # selecting accounts with less than 100,000 starting followers and plotting them
    lessThan100kList = newFollowersDF[totalFollowersDF.iloc[:1] < 10 ** 6].dropna(axis=1, how='all').columns
    lessThan100k = ax.plot(rescaleDF(newFollowersDF[lessThan100kList]), "r", alpha=0.5,
                           label="Accounts with < 100,000 followers")
    # selecting accounts with more than 100,000 starting followers and plotting them
    moreThan100kList = newFollowersDF[totalFollowersDF.iloc[:1] > 10 ** 6].dropna(axis=1, how='all').columns
    moreThan100k = ax.plot(rescaleDF(newFollowersDF[moreThan100kList]), "b", alpha=0.75,
                           label="Accounts with > 100,000 followers")
    ax.legend(handles=[lessThan100k[0], moreThan100k[0]], loc=9, framealpha=0.9)
    ax.set_title("Daily new followers relative to new followers on 2022-08-15 - small accounts vs large accounts")
    ax.set_xlabel("Date (from Aug. 15 to Sep. 11)")
    ax.set_xticks(range(19219, 19221 + len(newFollowersDF) - 2, 7))
    ax.set_xticks(totalFollowersDF.index, minor=True)
    ax.set_ylabel("Ratio of new followers to new followers on 2022-08-15")
    fig.savefig('./Figures/' + ax.get_title() + '.png', dpi=200)
    # --------------------------------------------------------------------------------------------------------------

    # Plotting normalized graph of total followers - comparing small and large accounts
    # --------------------------------------------------------------------------------------------------------------
    fig, ax = reset()
    # selecting accounts with less than 100,000 starting followers and plotting them
    lessThan100kList = totalFollowersDF[totalFollowersDF.iloc[:1] < 10 ** 6].dropna(axis=1, how='all').columns
    lessThan100k = ax.plot(normalizeDF(totalFollowersDF[lessThan100kList]), "r", alpha=0.5,
                           label="Accounts with < 100,000 followers")
    # selecting accounts with more than 100,000 starting followers and plotting them
    moreThan100kList = totalFollowersDF[totalFollowersDF.iloc[:1] > 10 ** 6].dropna(axis=1, how='all').columns
    moreThan100k = ax.plot(normalizeDF(totalFollowersDF[moreThan100kList]), "b", alpha=0.75,
                           label="Accounts with > 100,000 followers")
    ax.set_title("Normalized graph of total followers - small accounts vs large accounts")
    ax.legend(handles=[lessThan100k[0], moreThan100k[0]], loc=9, framealpha=0.9)
    ax.set_xlabel("Date (from Aug. 15 to Sep. 11)")
    ax.set_xticks(range(19219, 19221 + len(totalFollowersDF) - 2, 7))
    ax.set_xticks(totalFollowersDF.index, minor=True)
    ax.set_ylabel("0 represents minimum and 1 represents maximum")
    fig.savefig('./Figures/' + ax.get_title() + '.png', dpi=200)
    # --------------------------------------------------------------------------------------------------------------

    # Plotting normalized graph of daily new followers - comparing small and large accounts
    # --------------------------------------------------------------------------------------------------------------
    fig, ax = reset()
    # selecting accounts with less than 100,000 starting followers and plotting them
    lessThan100kList = newFollowersDF[totalFollowersDF.iloc[:1] < 10 ** 6].dropna(axis=1, how='all').columns
    lessThan100k = ax.plot(normalizeDF(newFollowersDF[lessThan100kList]), "r", alpha=0.5,
                           label="Accounts with < 100,000 followers")
    # selecting accounts with more than 100,000 starting followers and plotting them
    moreThan100kList = newFollowersDF[totalFollowersDF.iloc[:1] > 10 ** 6].dropna(axis=1, how='all').columns
    moreThan100k = ax.plot(normalizeDF(newFollowersDF[moreThan100kList]), "b", alpha=0.75,
                           label="Accounts with > 100,000 followers")
    ax.set_title("Normalized graph of daily new followers - small accounts vs large accounts")
    ax.legend(handles=[lessThan100k[0], moreThan100k[0]], loc=9, framealpha=0.9)
    ax.set_xlabel("Date (from Aug. 15 to Sep. 11)")
    ax.set_xticks(range(19219, 19221 + len(newFollowersDF) - 2, 7))
    ax.set_xticks(newFollowersDF.index, minor=True)
    ax.set_ylabel("0 represents minimum and 1 represents maximum")
    fig.savefig('./Figures/' + ax.get_title() + '.png', dpi=200)
    # --------------------------------------------------------------------------------------------------------------

    # Calculating selected correlations between users' new followers and cryptocurrencies
    # --------------------------------------------------------------------------------------------------------------
    pairs = [("stablekwon", "terra-luna-v2"), ("VitalikButerin", "ethereum"), ("cz_binance", "bnb"),
             ("AriannaSimpson", "terra-luna-v2")]
    for pair in pairs:
        print("Correlation between @"+pair[0]+"'s new follower count and "+pair[1]+" prices: " +
              '{:.3f}'.format(newFollowersDF[pair[0]].corr(cryptoPricesDF[pair[1]])))
    # --------------------------------------------------------------------------------------------------------------

    # Calculating average correlation between total followers and crypto price:
    # --------------------------------------------------------------------------------------------------------------
    matrix = (cryptoPricesDF.corrwith(totalFollowersDF.iloc[:, 0]).to_frame())
    matrix.columns = totalFollowersDF.columns[:1]
    for n in totalFollowersDF.columns:
        matrix[n] = (cryptoPricesDF.corrwith(totalFollowersDF[n]))
    print("Average correlation of total followers and crypto price: " + '{:.3f}'.format(matrix.mean().mean()))
    # --------------------------------------------------------------------------------------------------------------

    # Calculating average correlation between new followers and crypto price:
    # --------------------------------------------------------------------------------------------------------------
    matrix = (cryptoPricesDF.corrwith(newFollowersDF.iloc[:, 0]).to_frame())
    matrix.columns = newFollowersDF.columns[:1]
    for n in newFollowersDF.columns:
        matrix[n] = (cryptoPricesDF.corrwith(newFollowersDF[n]))
    print("Average correlation of new followers and crypto price: " + str(round(matrix.mean().mean(), 3)))
    # --------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    main()
