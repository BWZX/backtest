# run_func_demo
from rqalpha.api import *
from rqalpha import run_func
import numpy as np
import math
from config import *

"""



"""

def init(context):
    context.s1 = 'IF88'
    context.s2 = "000001.XSHE"
    context.done=False
    subscribe(context.s1)
    pass

def handle_bar(context, bar_dict):
    if not context.done:
        order_percent(context.s2, 0.9)
        sell_open(context.s1, 1)
        context.done=True
    pass
    
run_func(init=init, handle_bar=handle_bar, config=config)