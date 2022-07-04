# binance-assignment-python
# Assignment
- Use public market data from the Spot API at https://api.binance.com
- Binance API Spot documentation is at https://github.com/binance-exchange/binance-official-api-docs/
- All answers should be provided as source code written in either Go, Python, Java, Rust, or Bash.
- All technical or financial terminologies refer to their common, well known interpretations.

# Questions
1. Print the top 5 symbols with quote asset BTC and the highest volume over the last 24 hours in descending order.
2. Print the top 5 symbols with quote asset USDT and the highest number of trades over the last 24 hours in descending order.
3. Using the symbols from Q1, what is the total notional value of the top 200 bids-and-asks currently on each order book?
4. What is the price spread for each of the symbols from Q2?
5. Every 10 seconds print the result of Q4 and the absolute delta from the previous value for each symbol.
6. Make the output of Q5 accessible by querying http://localhost:8080/metrics using the Prometheus Metrics format.

## Pre-requisite
This has been tested using Ubuntu20 LTS OS. The following should be installed in the system:

1. Python3
2. Pip3
3. requests lib
4. panda lib
5. prometheus-client

```
brew install python3 
python3 -m pip install –upgrade pip
python -m pip install requests
pip3 install pandas
pip3 install prometheus-client
```

## How to run
```
python3 binance_spot_APIs_impl.py
```
