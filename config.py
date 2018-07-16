config = {
  "base": {
    "start_date": "2013-01-01",
    "end_date": "2017-12-01",
    "frequency": "1d",
    "margin_multiplier": 1,
    "benchmark": "000001.XSHG",
    "accounts": {
        "stock":  100000000,
        "future": 100000000,
    }
  },
  "extra": {
    "log_level": "verbose",
  },
  "mod": {
    "sys_analyser": {
      "enabled": True,
      "plot": True
    }
  }
}
