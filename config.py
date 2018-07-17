from datetime import datetime as dt

config = {
  "base": {
    "start_date": "2013-01-01",
    "end_date": "2017-12-01",
    "frequency": "1d",
    "margin_multiplier": 1,
    "benchmark": "000001.XSHG",
    "accounts": {
        "stock":  80000000,
        "future": 1,
    }
  },
  "extra": {
    "log_level": "verbose",
  },
  "mod": {
    "sys_analyser": {
      "enabled": True,
      "output_file": "./results/out{}.pkl".format(dt.strftime(dt.now(),'%Y-%m-%d_%H_%S')),      
      "plot_save_file": "./pics/out{}.jpg".format(dt.strftime(dt.now(),'%Y-%m-%d_%H_%S')),
      "plot": False,
    }
  }
}
