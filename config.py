config = {
  "base": {
    "start_date": "2016-06-01",
    "end_date": "2016-12-01",
    "frequency": "1d",
    "margin_multiplier": 1,
    "benchmark": "000001.XSHG",
    "accounts": {
        "stock": 1000000,
        "future": 1000000,
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
