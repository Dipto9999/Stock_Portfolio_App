# Stock Market Exploration

## Contents
* [Overview](#Overview)
* [Market](#Market)
    * [RSI](#Relative-Strength-Index-(RSI))
    * [Stock Correlations](#Stock-Correlations)
* [Portfolio](#Portfolio)
    * [Example](#Example)
    * [Preview](#Preview)
* [Credit](#Credit)

## Overview

An exploration of historical records and investor activity for the stock market. The records are pulled from [(`yahoo-finance`)](https://ca.finance.yahoo.com/) API.


## Market

In this analysis, we are primarily considering the $adjusted$ $closing$ prices over the past $365$ days</i>.

<p align = "center"><img src = "figures/Market_Prices.png" width = "60%" height = "60%" title = "Market Prices"></p>

This graph above is produced to show the price fluctuations from this time period.

### Relative Strength Index (RSI)

We have visualized the stock prices for an individual ticket along with its $RSI$.


<p align = "center"><img src = "figures/RSI_equation.png" width = "60%" height = "60%" title = "RSI equation"></p>
<p align = "center"><img src = "figures/TSLA_RSI.png" width = "60%" height = "60%" title = "Tesla Stock RSI"></p>

### Stock Correlations

We have included a `seaborn` heatmap of the $Pearson$ $correlation$ between the stock prices. These are expressed as a $percentage$ here.


<p align = "center"><img src = "figures/Stock_Correlations.png" width = "60%" height = "60%" title = "Stock Price Correlation"></p>

## Portfolio

An exploration of investor activity is implemented through modification of the `portfolio dataframe` variable :

### Example

Here is an example of a stock portfolio I had for a period of time, as well as the effective balances on $2022-08-28$.

<p align = "left">
    <img src = "figures/portfolio_df.png" width = "30%" height = "15%" title = "Portfolio DataFrame">
    <img src = "figures/balances_dict.png" width = "20%" height = "20%" title = "Portfolio Balances">
</p>

### Preview

We are implementing functionality for a `matplotlib` pie chart to display a portfolio preview here.

<p align = "center"><img src = "figures/Stock_Portfolio.png" width = "60%" height = "60%" title = "Stock Portfolio Preview"></p>

## Credit

The following links were consulted as reference in this exploration.

* [NeuralNine Youtube Channel](https://www.youtube.com/playlist?list=PL7yh-TELLS1HJzPsb6Xjdse2zbyQ-ocDH)