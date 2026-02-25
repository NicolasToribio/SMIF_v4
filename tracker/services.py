# Portfolio Service Layer - fetching stock prices and calculating portfolio metrics
# Based on yfinanceprototypev2.py, adapted to SMIF v4 by Claude
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from django.core.cache import cache
from django.conf import settings
from .models import PortfolioHolding

class PortfolioService: # to fetch and calculate portfolio data
    CACHE_TIMEOUT = 900 # 900 seconds = 15 minutes

    def __init__(self):
        self.cache_key_portfolio = 'portfolio_data'

    def get_active_holdings(self): # get all active holdings from the database
        return PortfolioHolding.objects.filter(is_active = True)
    
    def get_portfolio_data(self, use_cache=True): # returns dict with tickers, shares, prices, values
        if use_cache: # check the cache first
            cached = cache.get(self.cache_key_portfolio)
            if cached:
                return cached
        
        try:
            holdings = self.get_active_holdings()

            if not holdings.exists():
                return {
                    'success': False,
                    'error': 'No active holdings in portfolio',
                    'data' : None
                }
            
            # Build the ticker list and shares dict
            tickers = [h.ticker for h in holdings]
            shares_dict = {h.ticker: float(h.shares) for h in holdings}

            # Fetch current prices from yfinance
            data = yf.download(
                tickers,
                period = "1d",
                interval = "1d",
                auto_adjust = False,
                progress = False
            )

            # Handling single vs multiple tickers
            if len(tickers) == 1: # because yfinance returns a series if you have a single ticker
                latest_prices = {tickers[0]: float(data['Close'].iloc[-1])}
            else:
                latest_close = data['Close'].iloc[-1]
                latest_prices = latest_close.to_dict()

            # calculate values
            portfolio_items = []
            total_value = 0

            for ticker in tickers:
                price = float(latest_prices.get(ticker, 0))
                shares = shares_dict[ticker]
                value = price * shares 
                total_value += value

                portfolio_items.append({
                    'ticker': ticker,
                    'shares': shares,
                    'price': round(price, 2),
                    'value': round(value, 2)
                })
            
            # Sort by value (descending)
            portfolio_items.sort(key=lambda x: x['value'], reverse=True)

            result = {
                'success': True,
                'data': {
                    'items': portfolio_items,
                    'total_value': round(total_value, 2),
                    'last_updated': datetime.now().isoformat(),
                    'holdings_count': len(portfolio_items)
                },
                'error': None
            }

            # caching the result
            cache.set(self.cache_key_portfolio, result, self.CACHE_TIMEOUT)

            return result
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'data': None
            }

    def clear_cache(self): # manually clearing the cache for admin actions
        cache.delete(self.cache_key_portfolio)