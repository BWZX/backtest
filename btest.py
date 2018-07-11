# run_func_demo
from rqalpha.api import *
from rqalpha.core.strategy_context import StrategyContext
from rqalpha import run_func
import numpy as np
import math
from config import *
import tushare as ts
import pandas as pd
import os

_INDUSTRY = pd.read_csv(os.path.join(os.path.dirname(os.path.realpath(__file__)),'industry.csv'))
_ALL_INDUSTRY = ['电子器件', '玻璃行业', '商业百货', '传媒娱乐', '造纸行业', '生物制药', '陶瓷行业', '印刷包装', '建筑建材', '石油行业', '纺织机械', '环保行业', '飞机制造', '其它行业', '船舶制造', '物资外贸', '摩托车', '机械行业', '医疗器械', '家具行业', '公路桥梁', '钢铁行业', '水泥行业', '交通运输', '食品行业', '发电设备', '化工行业', '塑料制品', '仪器仪表', '有色金属', '金融行业', '供水供气', '煤炭行业', '农林牧渔', '酿酒行业', '房地产', '电器行业', '综合行业', '次新股', '汽车制造', '农药化肥', '酒店旅游', '家电行业', '电子信息', '化纤行业', '开发区', '电力行业', '纺织行业', '服装鞋类']

def getTradeStocks(date='2010-10-10'):
    return {'000001', '000005'}

def getTradeIndustryStocks(ind_name, date='2010-10-10'):
    return {'000001':0.1, '000005':0.2}


all_industry = ['电子器件', '玻璃行业', '商业百货', '传媒娱乐', '造纸行业', '生物制药', '陶瓷行业', '印刷包装', '建筑建材', '石油行业', '纺织机械', '环保行业', '飞机制造', '其它行业', '船舶制造', '物资外贸', '摩托车', '机械行业', '医疗器械', '家具行业', '公路桥梁', '钢铁行业', '水泥行业', '交通运输', '食品行业', '发电设备', '化工行业', '塑料制品', '仪器仪表', '有色金属', '金融行业', '供水供气', '煤炭行业', '农林牧渔', '酿酒行业', '房地产', '电器行业', '综合行业', '次新股', '汽车制造', '农药化肥', '酒店旅游', '家电行业', '电子信息', '化纤行业', '开发区', '电力行业', '纺织行业', '服装鞋类']


def code_to_id(code):
    if len(code) <6:
        code = '000000'+code
        code = code[-6:]
    if int(code[:2]) >= 50:
        code_id = code +'.XSHG'
    else:
        code_id = code + '.XSHE'
    return code,code_id

def Hs300IndustryRate(start_date, context):
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
    hs300AllMarkets =0 
    for code in code_list:
        code,code_id = code_to_id(code)
        if sto_outstand.get(int(code)):
            outstand = sto_outstand.get(int(code))
        else:
            outstand = 1.0
        price = history_bars(code_id, 1,'1d', 'close')[0]
        market_value = outstand *1e8* price
        hs300AllMarkets += market_value
        ind = str(_INDUSTRY[_INDUSTRY.code == code]['c_name'])
        if industry_rate.get(ind):
            industry_rate[ind]+=market_value
        else:
            industry_rate[ind]=market_value
    return hs300AllMarkets, industry_rate



def init(context):
    context.future = 'IF88'
    # context.s2 = "000001.XSHE"
    context.done=False
    subscribe(context.future)
    print(dir(context))
    # import pdb;pdb.set_trace()   
    print(context.run_info.stock_starting_cash , ' ------------------------------')
     
    pass

def before_trading(context):
    stocks = getTradeStocks()
    industry_rate = Hs300IndustryRate('2010-06-10', context)
    context.sto_moneyall = context.run_info.stock_starting_cash
    industry_count={}
    # industry_
    for sto in stocks:
        ind = str(_INDUSTRY[_INDUSTRY.code == sto]['c_name'])
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
            money = context.industry_rate * context.moneyall * context.stocks[sto]
            #"deal the stocks"
            order_value(code_id,money)
    else:
        money = 0 
        for sto in context.stocks:
            code, code_id = code_to_id(sto)
            ind = str(_INDUSTRY[_INDUSTRY.code == code]['c_name'])
            money = context.industry_rate * context.sto_moneyall / context.industry_count[ind]
            #"deal the stocks"
            order_value(code_id,money)


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
        order_percent('000001.XSHE', 0.9)
        sell_open(context.future, 1)        
        context.done=True
    import pdb;pdb.set_trace()
    pass
    
run_func(init=init, handle_bar=handle_bar, config=config)