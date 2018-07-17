# run_func_demo
from rqalpha.api import *

from rqalpha import run_func
import numpy as np
from datetime import datetime
import math
from config import *
import tushare as ts
import pandas as pd
import os
from xmlrpc.client import ServerProxy

_RPC = ServerProxy("http://node0:8898")

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
    """将股票的数字代码转化为米筐识别的代码——code_id，传入code，传出6位的code以及code_id
    """
    if len(code) <6:
        code = '000000'+code
        code = code[-6:]
    if int(code[:2]) >= 50:
        code_id = code +'.XSHG'
    else:
        code_id = code + '.XSHE'
    return code,code_id

def Hs300IndustryRate(start_date, context, bar_dict):  #bug may apear here for the lack of industry.csv of some stock
    """该函数计算hs300在各个行业的权重比例    
    """
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

    code_list = list(dfM[thedate])
    sto_basics = pd.read_csv(os.path.join(os.path.dirname(os.path.realpath(__file__)),'all.csv'))
    
    sto_basics = sto_basics[['code','outstanding']]
    
    sto_basics = sto_basics.set_index('code')
    sto_outstand = sto_basics.to_dict(orient='dict')['outstanding']
    # import pdb;pdb.set_trace()
    industry_rate ={}
    hs300AllMarkets = 0.0 
    for code in code_list:
        code,code_id = code_to_id(code)
        if sto_outstand.get(int(code)) and sto_outstand.get(int(code)) is not np.nan:
            outstand = sto_outstand.get(int(code))
        else:
            outstand = 1.0
        
        # import pdb; pdb.set_trace()
        try:
            price = bar_dict[code_id].close
        except Exception:
            price = 10.0     ####################

        if price is np.nan:
            price = 10.0 ############!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        market_value = outstand *1e8* price
        hs300AllMarkets += market_value
        if len(_INDUSTRY[_INDUSTRY.code == int(code)]['c_name'].values) <=0:
            ind = 'None'   #will repair later
        else:
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
    context.done=False
    context.futureLots = 0
    subscribe(context.future)
    context.lastStocks=0
    context.stocks=0
    scheduler.run_monthly(before_trade, tradingday=1)  
    pass

def before_trade(context, bar_dict):    
    # test_uncomplete(datetime.strftime(context.now,'%Y-%m-%d'), context)
    # exit()
    sto_m_total = context.portfolio.stock_account.total_value
    fut_m_total = context.portfolio.future_account.total_value
    print('stock account money: {0}, future account money: {1}, total {2}'.format(sto_m_total,fut_m_total,sto_m_total+ fut_m_total))
    context.dayDeal = False
    print('now is: ',datetime.strftime(context.now,'%Y-%m-%d'))
    stocks = _RPC.getTradeStocks(datetime.strftime(context.now,'%Y-%m-%d'),'m') 
    if stocks.count('sh000300'):
        stocks.remove('sh000300')    
    stocks.sort()  #assert that it is list!!!
    industry_rate = Hs300IndustryRate(datetime.strftime(context.now,'%Y-%m-%d'), context, bar_dict)
    context.sto_moneyall = context.portfolio.stock_account.total_value
    industry_count={}
    for sto in stocks:
        if len(_INDUSTRY[_INDUSTRY.code == int(sto)]['c_name'].values) <=0:
            ind = 'None'   #will repair later
        else:
            ind = _INDUSTRY[_INDUSTRY.code == int(sto)]['c_name'].values[0]

        if industry_count.get(ind):
            industry_count[ind] += 1
        else:
            industry_count[ind] = 1
        
    context.industry_count = industry_count #amount of certain industry
    context.industry_rate = industry_rate  #market value of industry among all
    context.lastStocks = context.stocks
    context.stocks = stocks  # the deal stock list or dict


def deal_stocks(context, bar_dict):  
    if context.portfolio.stock_account.market_value > 10:        
        for sto in context.portfolio.stock_account.positions:
            pased = False
            for stoo in context.stocks:
                code, code_id = code_to_id(stoo) 
                if code_id == sto:
                    pased = True
                    break
            if not pased:
                order_target_value(sto,0)

    if type(context.stocks) == type({}):
        money = 0 
        for sto in context.stocks:
            code, code_id = code_to_id(sto)
            ind = _INDUSTRY[_INDUSTRY.code == int(code)]['c_name'].values[0]
            money = context.industry_rate[ind] * context.sto_moneyall * context.stocks[sto]
            #"deal the stocks"
            order_target_value(code_id,money)
            print('deal ',code_id,' with money of ',money)
    else:        
        for sto in context.stocks:
            code, code_id = code_to_id(sto)
            # if len(_INDUSTRY[_INDUSTRY.code == int(sto)]['c_name'].values) <=0:
            #     ind = 'None'   #will repair later
            # else:
            #     ind = _INDUSTRY[_INDUSTRY.code == int(sto)]['c_name'].values[0]
            # if not context.industry_rate.get(ind) and context.industry_count.get(ind):
            #     money = context.sto_moneyall / len(context.stocks)
            # else:
            #     money = context.industry_rate[ind] * context.sto_moneyall / context.industry_count[ind]  

            # if context.sto_moneyall > context.portfolio.future_account.total_value:         
            #    context.sto_moneyall = context.portfolio.future_account.total_value
            
            context.money = context.sto_moneyall / len(context.stocks)
            # import pdb;pdb.set_trace()
            if context.portfolio.stock_account.cash < context.money:
                context.money = context.portfolio.stock_account.cash * 0.88
                pass
            order_target_value(code_id,context.money)
            # print('deal ',code_id,' with money of ',money)


def deal_future(context, bar_dict):
    sto_market_value = context.portfolio.stock_account.market_value
    if sto_market_value < 100:
        return

    price = bar_dict[context.future].close
    print("sto value: ", sto_market_value,' IF88 price: ', price)
    lots = int(sto_market_value/300/price)
    if lots - context.futureLots >= 1:    
        sell_open(context.future, lots - context.futureLots)  
    elif lots - context.futureLots <=-1:
        buy_close(context.future, context.futureLots - lots)
    # import pdb;pdb.set_trace()
    context.futureLots = lots
    print('deal future: ',lots)
    pass

def deal_complement(context, bar_dict):
    will_complete = []   
    for code in context.stocks:  #context.portfolio.stock_account.positions:
        code, code_id = code_to_id(code)  
        if not context.portfolio.stock_account.positions.get(code_id):
            will_complete.append(code_id)
    money = context.money
    for sto in will_complete:
        if context.portfolio.stock_account.cash < money*1.2:
            money = context.portfolio.stock_account.cash * 0.88
        order_target_value(sto, money)
        # print(datetime.strftime(context.now,'%Y-%m-%d'),'  Trying to deal complement on stock code: ',sto)
    # if len(will_complete)>1:
    #     deal_future(context,bar_dict)


def handle_bar(context, bar_dict):       
    if not context.stocks:
        return
    
    if context.stocks != context.lastStocks:
        deal_stocks(context, bar_dict)
        # deal_future(context, bar_dict)
        context.lastStocks = context.stocks

    deal_complement(context, bar_dict)    
    pass
    
run_func(init=init, handle_bar=handle_bar, config=config)