import yfinance as yf
import json
from pathlib import Path
import os
from tickerwrapper import TickerWrapper

class Model:
    def __init__(self):
        self.tickerlist = list()
        self.basepath = Path(__file__).resolve().parent
        self.watchlistfile = self.basepath.joinpath("watchlist.json")  # configfile containing watchlist
        self.methods = []
        self.movingaverage_symbol = "MA"
        self.initWatchlist()

    def initWatchlist(self) -> None:
        if not self.checkWatchlist():
            return

        # Load existing data from the JSON file
        with open(self.watchlistfile, 'r') as file:
            data = json.load(file)

        for each in data:
            tickerwrapper = self.findTicker(each[0])  # each[0] = symbol, each[1] = shortName
            if tickerwrapper.ticker:
                self.add_stock_to_tickerlist(tickerwrapper)

    #checks if 
    def checkWatchlist(self) -> bool:
        
        if not os.path.exists(self.watchlistfile):
            print("Watchlistfile not found!")
            Path(self.watchlistfile).touch()
            return False
        
        if not os.path.getsize(self.watchlistfile)>0:
            print("Watchlistfile is empty!")
            return False
        
        return True

    def getWatchlist(self,tickerwrapper: TickerWrapper) -> bool:

        # Load existing data from the JSON file
        with open(self.watchlistfile, 'r') as file:
            data = json.load(file)

        # extract each[0] (symbol) from each element in data, to check for duplicates
        tmpdata = [each[0] for each in data]
        if tickerwrapper.ticker.info["symbol"] in tmpdata:
            print("Stock already exists in Watchlist!")
            return False

    def findTicker(self,symbol: str) -> TickerWrapper:
        if not symbol:
            print("Symbol empty! Ticker couldnt be generated for this symbol!")
            return None
        tickerwrapper = TickerWrapper(yf.Ticker(symbol))
        try:
            check = tickerwrapper.ticker.info['symbol']
            check = tickerwrapper.ticker.info['shortName']
            #check = ticker.isin
        except:
            print("Tickerinfo about symbol, shortname and isin doesnt exist. Recheck entered symbol!")
            return None
        #self.symbol_info_label.config(text=f"Stock Symbol found: True\nShortname: {short_name}\nSymbol: {symbol}\nISIN: {isin}")
        return tickerwrapper
    
    def add_stock_to_tickerlist(self,tickerwrapper: TickerWrapper) -> None:
        self.tickerlist.append(tickerwrapper)

    def remove_stock_from_tickerlist(self,ticker_symbol: str) -> None:
        for tickerwrapper in self.tickerlist:
            if tickerwrapper.ticker.info["symbol"] == ticker_symbol:
                self.tickerlist.remove(tickerwrapper)

    def add_stockticker_to_watchlistfile(self,tickerwrapper: TickerWrapper) -> None:
        
        if not self.checkWatchlist():
            return

        # Load existing data from the JSON file
        with open(self.watchlistfile, 'r') as file:
            data = json.load(file)

        # Save the updated data back to the JSON file
        data.append([tickerwrapper.ticker.info["symbol"], tickerwrapper.ticker.info["shortName"]])
        with open(self.watchlistfile, 'w') as file:
            json.dump(data, file, indent=4)
    
    def check_duplicates_in_watchlistfile(self,tickerwrapper: TickerWrapper) -> bool:
        # Load existing data from the JSON file
        with open(self.watchlistfile, 'r') as file:
            data = json.load(file)
    
        # extract each[0] (symbol) from each element in data, to check for duplicates
        tmpdata = [each[0] for each in data]
        if tickerwrapper.ticker.info["symbol"] in tmpdata:
            print("Stock already exists in Watchlist!")
            return True
        else:
            return False

    def remove_stockticker_from_watchlistfile(self,symbol: str) -> None:
        check = self.checkWatchlist()
        if not check:
            return

        with open(self.watchlistfile, 'r') as file:
            data = json.load(file)

        # extract each[0] (symbol) from each element in data, to check for duplicates
        tmpdata = [each[0] for each in data]
        for index,each in enumerate(tmpdata):
            if each == symbol:
                data.pop(index)

        with open(self.watchlistfile, 'w') as file:
            json.dump(data, file, indent=4)


    def remove_method(self,index):
        #TODO: rework!
        pass
