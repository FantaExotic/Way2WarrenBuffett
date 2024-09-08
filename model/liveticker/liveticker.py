import pandas as pd
from model.currency import CurrencyWrapper
from model.tickerwrapper import TickerWrapper

class Liveticker:
    
    def __init__(self):
        pass

    def append_liveticker_to_tickerwrapper(self, msg: dict, currencywrapper: CurrencyWrapper, tickerwrapper: TickerWrapper) -> None:
        """processes received data from liveticker and appends it to tickerhistory of corresponding ticker"""
        price = msg['price']
        timestamp_ms = msg['timestamp']
        timestamp_s = timestamp_ms / 1000  # Convert milliseconds to seconds
        dayVolume = msg['dayVolume']

        # convert currency if required
        if tickerwrapper.verify_currency_conversion_required():
            price = currencywrapper.convert_currency_scalar(price)

        new_value = {'Open': [price], 'High': [price], 'Low': [price], 'Close': [price], 'Volume': [dayVolume], 'Dividends': [222]}  # TODO: get dividends data from liveticker! 
        new_data = pd.DataFrame(new_value)
        new_data.index = pd.to_datetime([timestamp_s], unit="s")
        if new_data.index.tz is None:
            new_data.index = new_data.index.tz_localize("UTC")
        new_data.index = new_data.index.tz_convert(tickerwrapper.ticker._tz)
        new_data.index.name = tickerwrapper.tickerhistory['1m'].index.name
        # Update the existing tickerhistory['1m'] DataFrame with the new data
        new_dataframe = pd.concat([tickerwrapper.tickerhistory['1m'],new_data])
        tickerwrapper.tickerhistory['1m'] = new_dataframe