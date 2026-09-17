import yfinance as yf
import datetime as dt



def get_market_data(ticker_str: str, target_tau: float = None):
    ticker = yf.Ticker(ticker_str)
    exp_dts = ticker.options
    td = dt.datetime.now()
    i = 0

    if not exp_dts: 
        print(f"Error: No expiry dates found for Ticker {ticker_str}.")
        return False

    # Calculation of all rem_T
    taus = []
    for day in exp_dts:
        taus.append((dt.datetime.strptime(day, "%Y-%m-%d") - td).days / 365)

    if target_tau is None:
        i = next(index for index, tau in enumerate(taus))

    # Finding the rem_T closest to the targeted tau
    else: 
        candidates = [(idx, tau) for idx, tau in enumerate(taus) if tau > 0]
        i = min(candidates, key=lambda x: abs(x[1] - target_tau))[0]
    

    rem_T = taus[i]
    S = ticker.history(period = "1d")["Close"].iloc[-1]
    option_chain_unfiltered = ticker.option_chain(exp_dts[i]).calls
    option_chain_filtered = option_chain_unfiltered[(option_chain_unfiltered["volume"] > 0) & (option_chain_unfiltered["openInterest"] > 5) & (option_chain_unfiltered["bid"] > 0)]
    call_price_frame = (option_chain_filtered["bid"] + option_chain_filtered["ask"]) / 2


    return(exp_dts[i], rem_T, S, option_chain_filtered, call_price_frame)
