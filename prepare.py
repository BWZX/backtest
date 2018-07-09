import tushare as ts
import pandas as pd
import os

all_industry = ['电子器件', '玻璃行业', '商业百货', '传媒娱乐', '造纸行业', '生物制药', '陶瓷行业', '印刷包装', '建筑建材', '石油行业', '纺织机械', '环保行业', '飞机制造', '其它行业', '船舶制造', '物资外贸', '摩托车', '机械行业', '医疗器械', '家具行业', '公路桥梁', '钢铁行业', '水泥行业', '交通运输', '食品行业', '发电设备', '化工行业', '塑料制品', '仪器仪表', '有色金属', '金融行业', '供水供气', '煤炭行业', '农林牧渔', '酿酒行业', '房地产', '电器行业', '综合行业', '次新股', '汽车制造', '农药化肥', '酒店旅游', '家电行业', '电子信息', '化纤行业', '开发区', '电力行业', '纺织行业', '服装鞋类']



def Hs300IndustryRate(start_date):
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
    
    for code in code_list:

