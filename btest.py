# run_func_demo
from rqalpha.api import *
from rqalpha.core.strategy_context import StrategyContext
from rqalpha import run_func
import numpy as np
from datetime import datetime
import math
from config import *
import tushare as ts
import pandas as pd
import os

_INDUSTRY = pd.read_csv(os.path.join(os.path.dirname(os.path.realpath(__file__)),'industry.csv'))
_ALL_INDUSTRY = ['电子器件', '玻璃行业', '商业百货', '传媒娱乐', '造纸行业', '生物制药', '陶瓷行业', '印刷包装', '建筑建材', '石油行业', '纺织机械', '环保行业', '飞机制造', '其它行业', '船舶制造', '物资外贸', '摩托车', '机械行业', '医疗器械', '家具行业', '公路桥梁', '钢铁行业', '水泥行业', '交通运输', '食品行业', '发电设备', '化工行业', '塑料制品', '仪器仪表', '有色金属', '金融行业', '供水供气', '煤炭行业', '农林牧渔', '酿酒行业', '房地产', '电器行业', '综合行业', '次新股', '汽车制造', '农药化肥', '酒店旅游', '家电行业', '电子信息', '化纤行业', '开发区', '电力行业', '纺织行业', '服装鞋类']

def getTradeStocks(date='2010-10-10'):
    return ['601788', '000002', '600583', '000709', '000898', '600089', '600418', '600675', '000959', '600011', '600837', '601186', '600027', '600269', '000631', '601390', '000685', '600999', '600320', '000932', '600688', '601607', '600660', '000001', '002142', '000778', '600748', '601169', '601003', '600718', '000951', '600597', '600611', '000423', '601618', '601668', '601918', '601166', '600028', '601333', '600109', '000900', '600048', '600820', '002304', '000031', '600808', '600663', '600104', '000876', '000625', '600881', '600018', '000686', '600009', '600635', '000063', '600022']

def getTradeIndustryStocks(ind_name, date='2010-10-10'):
    return {'000001':0.1, '000005':0.2}


all_industry = ['电子器件', '玻璃行业', '商业百货', '传媒娱乐', '造纸行业', '生物制药', '陶瓷行业', '印刷包装', '建筑建材', '石油行业', '纺织机械', '环保行业', '飞机制造', '其它行业', '船舶制造', '物资外贸', '摩托车', '机械行业', '医疗器械', '家具行业', '公路桥梁', '钢铁行业', '水泥行业', '交通运输', '食品行业', '发电设备', '化工行业', '塑料制品', '仪器仪表', '有色金属', '金融行业', '供水供气', '煤炭行业', '农林牧渔', '酿酒行业', '房地产', '电器行业', '综合行业', '次新股', '汽车制造', '农药化肥', '酒店旅游', '家电行业', '电子信息', '化纤行业', '开发区', '电力行业', '纺织行业', '服装鞋类']

def test_uncomplete(start_date,context):
    temdate = start_date.split('-')
    date = temdate[0]+temdate[1]
    dfM = pd.read_csv(os.path.join(os.path.dirname(os.path.realpath(__file__)),'hs300.csv'))
    dfM = dfM[1:]
    thedate=''    
    for d in dfM:
        thedate = str(d)
        if int(date) < int(d):
            break
    code_list = list(dfM[thedate])    
    for code in code_list:
        code,code_id = code_to_id(code) 
        if len(_INDUSTRY[_INDUSTRY.code == int(code)]['c_name'].values) <=0:
            print(code)

def code_to_id(code):
    if len(code) <6:
        code = '000000'+code
        code = code[-6:]
    if int(code[:2]) >= 50:
        code_id = code +'.XSHG'
    else:
        code_id = code + '.XSHE'
    return code,code_id

def Hs300IndustryRate(start_date, context):  #bug may apear here for the lack of industry.csv of some stock
    temdate = start_date.split('-')
    date = temdate[0]+temdate[1]
    dfM = pd.read_csv(os.path.join(os.path.dirname(os.path.realpath(__file__)),'hs300.csv'))
    dfM = dfM[1:]
    thedate=''
    nextdate=''
    end_date=''
    for d in dfM:
        thedate = str(d)
        if int(date) < int(d):
            break

    # cursor = financetable.find({'code':'000001'}).sort('date')
    # struct = equitystructure.find({'code': '000001'}).sort('report_date')
    # print(list(cursor))
    # print(list(struct))
    code_list = list(dfM[thedate])
    sto_basics = pd.read_csv(os.path.join(os.path.dirname(os.path.realpath(__file__)),'all.csv'))
    
    sto_basics = sto_basics[['code','outstanding']]
    
    sto_basics = sto_basics.set_index('code')
    sto_outstand = sto_basics.to_dict(orient='dict')['outstanding']
    # import pdb;pdb.set_trace()
    # print(code_list)
    industry_rate ={}
    hs300AllMarkets = 0.0 
    for code in code_list:
        code,code_id = code_to_id(code)
        # print(code)
        if sto_outstand.get(int(code)):
            outstand = sto_outstand.get(int(code))
        else:
            outstand = 1.0
        price = history_bars(code_id, 1,'1d', 'close')[0]
        # print(7777777777,' ',code_id,' ',price,)
        market_value = outstand *1e8* price
        hs300AllMarkets += market_value
        # print(888887888)
        # import pdb;pdb.set_trace()  
        ind = _INDUSTRY[_INDUSTRY.code == int(code)]['c_name'].values[0]
        # print(ind,'----',market_value)
        if industry_rate.get(ind):
            # print('inside add ',industry_rate[ind])
            industry_rate[ind]+=market_value
            # print('add to ',industry_rate[ind])
        else:
            # print('inside creat.')
            industry_rate[ind]=market_value
    # print('loop all')
    for inds in industry_rate:
        industry_rate[inds] = industry_rate[inds]/ hs300AllMarkets
    return industry_rate



def init(context):
    context.future = 'IF88'
    # context.s2 = "000001.XSHE"
    context.done=False
    subscribe(context.future)
    # print(dir(context))
    # import pdb;pdb.set_trace()   
    # print(context.run_info.stock_starting_cash , ' ------------------------------')
     
    pass

def before_trade(context):
    # test_uncomplete(datetime.strftime(context.now,'%Y-%m-%d'), context)
    # exit()
    stocks = getTradeStocks() 
    # print('ssssssss',datetime.strftime(context.now,'%Y-%m-%d'))   
    industry_rate = Hs300IndustryRate(datetime.strftime(context.now,'%Y-%m-%d'), context)
    context.sto_moneyall = context.run_info.stock_starting_cash
    industry_count={}
    # industry_
    for sto in stocks:
        ind = _INDUSTRY[_INDUSTRY.code == int(sto)]['c_name'].values[0]
        if industry_count.get(ind):
            industry_count[ind] += 1
        else:
            industry_count[ind] = 1
        
    context.industry_count = industry_count #amount of certain industry
    context.industry_rate = industry_rate  #market value of industry among all
    context.stocks = stocks  # the deal stock list or dict

def deal_stocks(context, bar_dict):    
    if type(context.stocks) == type({}):
        money = 0 
        for sto in context.stocks:
            code, code_id = code_to_id(sto)
            ind = _INDUSTRY[_INDUSTRY.code == int(code)]['c_name'].values[0]
            money = context.industry_rate[ind] * context.sto_moneyall * context.stocks[sto]
            #"deal the stocks"
            order_value(code_id,money)
            print('deal ',code_id,' with money of ',money)
    else:
        money = 0 
        for sto in context.stocks:
            code, code_id = code_to_id(sto)
            ind = _INDUSTRY[_INDUSTRY.code == int(code)]['c_name'].values[0]
            # print('iam here,')
            # import pdb;pdb.set_trace()  
            print('the count is： ',context.industry_count[ind],' the code ',code, ' rate: ',context.industry_rate.get(ind))
            money = context.industry_rate[ind] * context.sto_moneyall / context.industry_count[ind]
            print('before deal ', money)
            #"deal the stocks"
            order_value(code_id,money)
            print('deal ',code_id,' with money of ',money)


def deal_future(context, bar_dict):
    sto_market_value = context.portfolio.stock_account.market_value
    if sto_market_value <100:
        return
    price = bar_dict[context.future].close
    lots = int(sto_market_value/price)
    sell_open(context.future, lots)  
    pass

def handle_bar(context, bar_dict):    
    if not context.done:
        before_trade(context)
        deal_stocks(context, bar_dict)
        # deal_future(context, bar_dict)
        # order_percent('000001.XSHE', 0.9)
        # sell_open(context.future, 1)        
        context.done=True
    # import pdb;pdb.set_trace()
    pass
    
run_func(init=init, handle_bar=handle_bar, config=config)