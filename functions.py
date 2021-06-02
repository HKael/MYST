
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: functions.py : python script with general functions                                         -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""
import pandas as pd
import numpy as np
import yfinance as yf
import time
import datetime

# Get Dates
def f_date(p_files):
    # Labels for dataframe and yfinance
    t_dates = [i.strftime("%d-%m-%Y") for i in sorted([pd.to_datetime(i[8:]).date() for i in p_files])]

    # For other calculations
    i_dates = [i.strftime("%Y-%m-%d") for i in sorted([pd.to_datetime(i[8:]).date() for i in p_files])]

    # Final data to return
    r_f_dates = {"i_dates": i_dates, "t_dates": t_dates}

    return r_f_dates

# Get Tickers
def f_tickers(p_archivos, p_data_archivos):
    tickers = []
    for i in p_archivos:
        l_tickers = list(p_data_archivos[i]["Ticker"])
        [tickers.append(i + ".MX") for i in l_tickers]
    global_tickers = np.unique(tickers).tolist()

    # Name adjustment
    global_tickers = [i.replace("GFREGIOO.MX", "RA.MX") for i in global_tickers]
    global_tickers = [i.replace("MEXCHEM.MX", "ORBIA.MX") for i in global_tickers]
    global_tickers = [i.replace("LIVEPOLC.1.MX", "LIVEPOLC-1.MX") for i in global_tickers]

    # Remove problematic tickers and cash entries
    [global_tickers.remove(i) for i in ["MXN.MX", "USD.MX", "KOFL.MX", "KOFUBL.MX,"
                                        "BSMXB.MX", "SITESB.1.MX", "NEMAKA.MX", "NMKA.MX"]]

    return global_tickers

# Get Prices
def f_get_prices(p_tickers, p_fechas):
    # Initial date, no changes
    f_ini = p_fechas[0]

    # Initial date plus 3 days
    f_fin = str(datetime.datetime.strptime(p_fechas[-1], "%Y-%m-%d") + datetime.timedelta(days=3))[:10]

    # Time counter
    inicio = time.time()

    # Yahoo finance data download
    data = yf.download(p_tickers, start=f_ini, end=f_fin, actions=False, group_by="close",
                       interval="1d", auto_adjust=False, prepost=False, threads=True)

    # Time length of process
    tiempo = "It took", round(time.time() - inicio, 2), "seconds."

    # Morph date column
    data_close = pd.DataFrame({i: data[i]["Close"] for i in p_tickers})

    # We assume NAFRTAC rebalance and Yahoo finance close price times align.

    # Only relevant dates
    ic_fechas = sorted(list(set(data_close.index.astype(str).tolist() & set(p_fechas))))

    # All prices
    precios = data_close.iloc[[int(np.where(data_close.index == i)[0]) for i in ic_fechas]]

    # Order columns
    precios = precios.reindex(sorted(precios.columns), axis = 1)

    return {"precios": precios, "tiempo": tiempo}
