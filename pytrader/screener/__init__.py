# encoding: utf-8

from finviz.screener import Screener
import logging


log = logging.getLogger()

"""
Search class
uses preset filters to perform queries at FinViz.com to find stocks to watch
"""
class Search:
    presets = {
        'beta': {
            'filters': ['ta_beta_o1', 'sh_avgvol_o1000'],
        },
        'bouncy': {
            'filters': ['sh_curvol_o1000','ta_beta_o1','ta_highlow20d_b5h','ta_highlow52w_a70h','ta_sma20_sa50','ta_sma200_sb50','ta_sma50_pa'],
        },
        'breakout': {
            'filters': ['sh_price_u20','sh_relvol_o2','ta_change_u','ta_perf_dup','ta_perf2_d10o'],
        },
        'darkmoney': {
            'filters': ['sh_curvol_o5000','sh_relvol_o5','ta_beta_o1'],
        },
        'dip': {
            'filters': ['sh_price_u20','ta_averagetruerange_o0.25','ta_perf_ddown','ta_perf2_d5u','ta_rsi_os40'],
        },
        'party': {
            'filters': ['cap_small','ind_stocksonly','sh_avgvol_o100','ta_perf_dup'],
            'signal': 'ta_unusualvolume',
        },
        'short': {
            'filters': ['hsh_price_u20','sh_relvol_o1.5','ta_perf_dup','ta_rsi_ob80'],
        },
        's&p500': {
            'filters': ['exch_nyse','idx_sp500'],
            'rows': 500,
        },
        'swing': {
            'filters': ['fa_epsqoq_o5','fa_epsyoy1_o5','sh_instown_u10','sh_price_u20','sh_relvol_o0.5','ta_averagetruerange_o0.25','ta_sma20_pa','ta_sma200_pa','ta_sma50_pa'],
        },
    }

    """ init accepts a string to select filter preset """
    def __init__(self, strategy):
        log.debug("initialize search with {}".format(strategy))
        try:
            self.preset =  self.presets[strategy]
        except KeyError:
            logger.error('screener.Search was initialized using a strategy value which does not exist')

        self.stock_list = Screener(
            filters=self.preset.get('filters', []), 
            order=self.preset.get('order', '-volume'), 
            rows=self.preset.get('rows', 50), 
            signal=self.preset.get('signal', ''), 
            table=self.preset.get('table', 'Performance')
        )

    """ print the stock list table """
    def show(self):
        log.debug("Screener results")
        log.debug(self.stock_list)

    """ return the list of ticker symbols """
    def symbols(self):
        log.debug("Parsing ticker symbols from screener results")
        symbols=[] 
        for stock in self.stock_list:
            symbols.append(stock['Ticker'])
        return symbols
