config = {
  "base": {
    "start_date": "2013-01-01",
    "end_date": "2017-12-01",
    "frequency": "1d",
    "margin_multiplier": 1,
    "benchmark": "000001.XSHG",
    "accounts": {
        "stock":  50000000,
        "future": 60000000,
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
