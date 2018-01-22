# crypto_analysis_1
Using quantitative methods to hedge against risk in the cryptocurrency market

Data scraping:
--------------
Create a comprehensive function to scrape crytocurrency data from various resources. Due to the presence of various indices which have different closing values for the cryptocurrencies, there is a need to scrape the trading value of a cryptocurrency from each index.

Calcuating Correlation:
-----------------------
Calculate the correlation of the cryptocurrencies with one another. Here we create a matrix to visualize the data. We use both normal correlation and spearman correlation. 

The correlation coefficient measures the extent to which the relationship between two variables is linear. Its value is always between -1 and 1. A positive coefficient indicates that the variables are directly related, i.e. when one increases the other one also increases. A negative coefficient indicates that the variables are inversely related, so that when one increases the other decreases. The closer to 0 the correlation coefficient is, the weaker the relationship between the variables.

Spearman correlation is used in order to reduce the impact of outliers.Regular correlation can be vulnerable to outliers in your data. Spearman rank correlation was developed in an attempt to be more robust to extreme values, which is especially important in the fat-tailed distributions of finance.

The Spearman Rank Correlation Coefficient allows us to determine whether or not two data series move together; that is, when one increases (decreases) the other also increases (decreases).This is useful when your data sets may be in different units, and therefore not linearly related

The data that we consider for the correlation are the daily returns of all cryptocurrencies as a time series. The reason we look for returns is because we are looking to identify deviations from the random walk theory. 

Risk Exposure:
----------------
In order to move on to beta hedging, we need to know what exactly it is and why we're doing it.

There are probably numerous factors that influence the price of a cryptocurrency or stock. In order to identify good trading strategies, one needs to find out the risk exposure of the cryptocurrency or stock to that particular factor. This is conveyed by something called a beta. 

A high beta means high risk. You're taking a volatile bet. So your trading model needs to have a low beta value. I am unsure of the standards set by companies for trading models but I have read that beta values in the range [-0.3,0.3] are considered good.

Consider:
Y = a + b1X1 + b2X2 + ... + bnXn

Where 
Y - Return of an asset
a - alpha
X1 - Price of oil (Random example)
X2 - Market returns (Random example)
b1,b2 - Beta of X1,X2
here X1 and X2 are the two factors which you've picked to base your model on. 

Now, if the above trading model suggests that all your factors have zero value. Then you have achieved a model with pure alpha. 
Since the value of alpha(a) is independant of the factors, you get alpha returns everyday. 

This is only an ideal scenario. In most scenarios, you need to identify the right factors and then ensure you hedge against the risk enumerated by the beta values.

How you do this leads to the next part.

Risk Management:
----------------
There are many ways of managing risk but here I will initially discuss 2 of them and then move on to the rest.

1. Diversification:

Using spearman correlation, we can identify which two assets/cryptocurrencies are correlated.

Correlation is a useful statistic because uncorrelated portfolios are quite useful to have. If the assets are uncorrelated, a drawdown in one will not correspond with a drawdown in another. This leads to a very stable return stream when many uncorrelated assets are combined.

While it may sound simple, identifying uncorrelated cryptocurrencies is hard. This is mainly due to the fact that there so many new cryptocurrencies and since the general public currently views its a viable investment option, the cryptomarket is largely impacted by the public emotion. Hence, there is high positive correlation between cryptocurrencies. 

It may be necessary to identify assets in other classes which have a negative correlation with cryptocurrencies in order to make a diversified portfolio.

2. Beta Hedging
