import yfinance as yf
import datetime as dt



def get_market_data(ticker_str: str):
    ticker = yf.Ticker(ticker_str)
    exp_dts = ticker.options
    td = dt.datetime.now()
    i = 0
    if not exp_dts: 
        print(f"Error: No expiry dates found for Ticker {ticker_str}.")
        return False
    while (dt.datetime.strptime(exp_dts[i], "%Y-%m-%d") - td).days <= 0:
        i += 1
    next_date = dt.datetime.strptime(exp_dts[i], "%Y-%m-%d")
    rem_T = (next_date - td).days / 365
    S = ticker.history(period = "1d")["Close"].iloc[-1]
    option_chain_unfiltered = ticker.option_chain(exp_dts[i]).calls
    option_chain_filtered = option_chain_unfiltered[(option_chain_unfiltered["volume"] >= 10) & (option_chain_unfiltered["openInterest"] > 10)]
    call_price_frame = (option_chain_filtered["bid"] + option_chain_filtered["ask"]) / 2


    return(exp_dts[i], rem_T, S, option_chain_filtered, call_price_frame)
