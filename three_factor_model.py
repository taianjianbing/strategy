# !/usr/bin/env python
# -*- coding: utf-8 -*-
from gmsdk.api import StrategyBase
import datetime
import pandas as pd
import numpy as np



class Strategy(StrategyBase):
    '''
    three factor model;

    '''
    def __init__(self, *args, **kwargs):
        super(Strategy, self).__init__(*args, **kwargs)
        self.buy_dict = {}
        self.sell_dict = {}
        self.stocks_pool = []
        self.is_traded = False
        self.md.subscribe('SHSE.000016.bar.daily')
        self.count  = 0
        self.Number = 10
        self.TP = 15
        self.yb = 63
        self.NoF =3
        self.param = None
        self.rf = 0.04
    def initialize(self):
        pass

    def set_slip_fee(self):
        pass

    def decide_transfer_position(self):
        self.count += 1
        if self.count % self.TP == 0:
            self.is_traded = True
        else:
            self.is_traded = False

    def get_stock_pool(self):
        instruments1 = self.get_instruments('SHSE', '1', '1')
        instruments2 = self.get_instruments('SZSE', '1', '1')
        symbol_list1 = set(instrument.symbol for instrument in instruments1+instruments2)
        constituents = self.get_constituents('SHSE.000300')
        symbol_list2 = set(constituent.symbol for constituent in constituents)
        symbol_list =  list(symbol_list1 & symbol_list2)
        return symbol_list

    def on_bar(self, bar):
        self.decide_transfer_position()

        if self.is_traded:
            self.initialize()
            self.stocks_pool = self.get_stock_pool()

            start_time = self.getDay(bar.strtime[:6].replace('T', " "), self.TP)
            end_time = self.getDay(bar.strtime[:6].repalce("T", " "), -1)

            self.param = self.FF(self, start_time, end_time)

            self.everyStockMoney = self.get_cash()/self.Number
            self.order_order_buy(self)
            self.order_order_sell(self)

    #"2015-10-29 9:30:00", "2015-10-29 15:00:00"
    def get_stocks_pd(self):
        stocks_pool_pd = pd.DataFrame()
        stocks_dic = {}

        for stock in self.stocks_pool:

            stock_dailybars = self.get_last_n_dailybars(stock, self.yb)
            stock_marketindex = self.get_last_n_market_index(stock, self.yb)
            stock_financial  = self.get_last_n_financial_index(stock, self.yb)

            temp_dic[stock] = {'Data':[stock_dailybar.strendtime()]}
            stocks_dic[stock] = pd.DataFrame({stock:[]})
        stocks_pool_pd = pd.concat(stocks_dic)
        stocks_pool_pd.to_csv('stocks_pool_dic.csv')
        return stocks_pool_pd

    def getDay(self, present, dt):

        t = datetime.datetime.strptime(present, '%Y-%m-%d %H:%M:%S') + datetime.timedelta(days=dt)
        return datetime.datetime.strftime(t, '%Y-%m-%d %H:%M:%S')


    def order_stock_sell(self, stock_sort):

        pass
    def order_order_buy(self, stock_sort):
        pass
    def on_order_filled(self, order):
        pass

    def collect_last_yb_information(self):

    def linregression(self, X, Y, columns = 3):
        pass




if __name__ == '__main__':
    my_strategy = Strategy(
        username='18660821753',  # 请修改账号
        password='long199124',  # 请修改密码
        strategy_id='strategy_id',  # 请修改策略ID
        mode=2,
        td_addr='localhost:8001')

    ret = my_strategy.run()
    print('exit code: ', ret)