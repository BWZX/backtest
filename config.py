from datetime import datetime as dt

config = {
  "base": {
    "start_date": "2013-01-01",
    "end_date": "2017-12-01",
    "frequency": "1d",
    "margin_multiplier": 1,
    "benchmark": "000001.XSHG",
    "accounts": {
        "stock":  120000000,
        "future": 100000000,
    }
  },
  "extra": {
    "log_level": "verbose",
  },
  "mod": {
    "sys_analyser": {
      "enabled": True,
      "output_file": "./results/out{}.pkl".format(dt.strftime(dt.now(),'%Y-%m-%d_%H_%S')),
      "plot": True
    }
  }
}
