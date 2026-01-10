def newTradeLite():
    return {
    "e": "TRADE_LITE",
    "E": 1749013292798,
    "T": 1749013292798,
    "s": "SOLUSDT",
    "q": "0.09", 
    "p": "0.0000",
    "m": False,
    "c": "fOPYqvypuFM2LKJ3ihzKFZ", 
    "S": "BUY",
    "L": "156.5000",
    "l": "0.09",
    "t": 2369436085,
    "i": 121058809222
}
def newMarketOrder():
    return {
    "e": "ORDER_TRADE_UPDATE",
    "T": 1749013292798,
    "E": 1749013292798,
    "o": {
        "s": "SOLUSDT",
        "c": "fOPYqvypuFM2LKJ3ihzKFZ",
        "S": "BUY",
        "o": "MARKET",
        "f": "GTC",
        "q": "0.09",
        "p": "0",
        "ap": "0",
        "sp": "0",
        "x": "NEW",
        "X": "NEW",
        "i": 121058809222,
        "l": "0",
        "z": "0",
        "L": "0",
        "n": "0",
        "N": "USDT",
        "T": 1749013292798,
        "t": 0,
        "b": "0",
        "a": "0",
        "m": False,
        "R": False,
        "wt": "CONTRACT_PRICE",
        "ot": "MARKET",
        "ps": "BOTH",
        "cp": False,
        "rp": "0",
        "pP": False,
        "si": 0,
        "ss": 0,
        "V": "EXPIRE_MAKER",
        "pm": "NONE",
        "gtd": 0
    }
}

def newAccountUpdate():
    return {
    "e": "ACCOUNT_UPDATE",
    "T": 1749013292798,
    "E": 1749013292798,
    "a": { 
            "B": [
                {
                    "a": "USDT", 
                    "wb": "0.21843288", 
                    "cw": "0.21843288", 
                    "bc": "0" 
                }
            ],
            "P": [ 
                {"s": "SOLUSDT", 
                    "pa": "0.09",
                    "ep": "156.5",
                    "cr": "0.35020001",
                    "up": "-0.00824514",
                    "mt": "cross",
                    "iw": "0",
                    "ps": "BOTH",
                    "ma": "USDT",
                    "bep": "156.57825"
                }
            ],
            "m": "ORDER"
        }
    }

def newFilledMarketOrder():
    return {
    "e": "ORDER_TRADE_UPDATE",
    "T": 1749013292798,
    "E": 1749013292798,
    "o": {
        "s": "SOLUSDT",
        "c": "3",
        "S": "BUY",
        "o": "MARKET",
        "f": "GTC",
        "q": "0.09",
        "p": "0",
        "ap": "156.5",
        "sp": "0",
        "x": "TRADE",
        "X": "FILLED",
        "i": 121058809222,
        "l": "0.09",
        "z": "0.09",
        "L": "156.5",
        "n": "0.0070425",
        "N": "USDT",
        "T": 1749013292798,
        "t": 2369436085,
        "b": "0",
        "a": "0",
        "m": False,
        "R": False,
        "wt": "CONTRACT_PRICE",
        "ot": "MARKET",
        "ps": "BOTH",
        "cp": False,
        "rp": "0",
        "pP": False,
        "si": 0,
        "ss": 0,
        "V": "EXPIRE_MAKER",
        "pm": "NONE",
        "gtd": 0
    }
}

def newParsedMarketOrder():
    return {
    "order_id": 5,
    "status": "NEW",
    "symbol": "SOLUSDT",
    "side": "BUY",
    "type": "MARKET",
    "qty": "0.09",
    "direction": "LONG",
    "created_at": 1749013292798
}

def newParsedFilledMarketOrder():
    return {
    "order_id": 5,
    "status": "FILLED",
    "symbol": "SOLUSDT",
    "side": "SELL",
    "type": "MARKET",
    "qty": "3",
    "direction": "SHORT",
    "ask_price": "156.5",
    "filled_price": "156.5",
    "updated_at": 1749013292798
}

def newAlgoSLOrder():
    return {
    "e": "ALGO_UPDATE",
    "T": 1768015698681,
    "E": 1768015698682,
    "o": {
        "caid": "qtpsw3w8FLiEcues3KRbae",
        "aid": 1000000333505502,
        "at": "CONDITIONAL",
        "o": "STOP_MARKET",
        "s": "SOLUSDT",
        "S": "SELL",
        "ps": "BOTH",
        "f": "GTC",
        "q": "0.04",
        "X": "NEW",
        "ai": "",
        "tp": "136.12",
        "p": "0",
        "V": "EXPIRE_MAKER",
        "wt": "CONTRACT_PRICE",
        "pm": "NONE",
        "cp": False,
        "pP": False,
        "R": True,
        "tt": 0,
        "gtd": 0
    }
}

def newTriggeringAlgoSLOrder():
    return {
    "e": "ALGO_UPDATE",
    "T": 1768015729352,
    "E": 1768015729353,
    "o": {
        "caid": "qtpsw3w8FLiEcues3KRbae",
        "aid": 1000000333505502,
        "at": "CONDITIONAL",
        "o": "STOP_MARKET",
        "s": "SOLUSDT",
        "S": "SELL",
        "ps": "BOTH",
        "f": "GTC",
        "q": "0.04",
        "X": "TRIGGERING",
        "ai": "",
        "tp": "136.12",
        "p": "0",
        "V": "EXPIRE_MAKER",
        "wt": "CONTRACT_PRICE",
        "pm": "NONE",
        "cp": False,
        "pP": False,
        "R": True,
        "tt": 1768015729352,
        "gtd": 0
    }
}

def newFilledAlgoSLOrder():
    return {
    "e": "ALGO_UPDATE",
    "T": 1768015729360,
    "E": 1768015729360,
    "o": {
        "caid": "qtpsw3w8FLiEcues3KRbae",
        "aid": 1000000333505502,
        "at": "CONDITIONAL",
        "o": "STOP_MARKET",
        "s": "SOLUSDT",
        "S": "SELL",
        "ps": "BOTH",
        "f": "GTC",
        "q": "0.04",
        "X": "FINISHED",
        "ai": "188463665892",
        "ap": "136.12",
        "aq": "0.04",
        "act": "MARKET",
        "tp": "136.12",
        "p": "0",
        "V": "EXPIRE_MAKER",
        "wt": "CONTRACT_PRICE",
        "pm": "NONE",
        "cp": False,
        "pP": False,
        "R": True,
        "tt": 1768015729352,
        "gtd": 0
    }
}

def newCanceledSLOrder():
    return {
    "e": "ALGO_UPDATE",
    "T": 1768014907127,
    "E": 1768014907127,
    "o": {
        "caid": "1P4xTv4U5Fr3KI2PFOejPn",
        "aid": 1000000332992900,
        "at": "CONDITIONAL",
        "o": "STOP_MARKET",
        "s": "SOLUSDT",
        "S": "SELL",
        "ps": "BOTH",
        "f": "GTC",
        "q": "0.05",
        "X": "CANCELED",
        "ai": "",
        "tp": "100.02",
        "p": "0",
        "V": "EXPIRE_MAKER",
        "wt": "CONTRACT_PRICE",
        "pm": "NONE",
        "cp": False,
        "pP": False,
        "R": False,
        "tt": 0,
        "gtd": 0
    }
}

def newSLOrder():
    return {
    "e": "ORDER_TRADE_UPDATE",
    "T": 1749037471697,
    "E": 1749037471697,
    "o": {
        "s": "SOLUSDT",
        "c": "3",
        "S": "SELL",
        "o": "STOP_MARKET",
        "f": "GTC",
        "q": "0",
        "p": "0",
        "ap": "0",
        "sp": "155.7",
        "x": "NEW",
        "X": "NEW",
        "i": 121112646034,
        "l": "0",
        "z": "0",
        "L": "0",
        "n": "0",
        "N": "USDT",
        "T": 1749037471697,
        "t": 0,
        "b": "0",
        "a": "0",
        "m": False,
        "R": True,
        "wt": "CONTRACT_PRICE",
        "ot": "STOP_MARKET",
        "ps": "BOTH",
        "cp": True,
        "rp": "0",
        "pP": False,
        "si": 0,
        "ss": 0,
        "V": "EXPIRE_MAKER",
        "pm": "NONE",
        "gtd": 0
    }
}

def newParsedSLOrder():
    return {
    "order_id": 6,
    "status": "NEW",
    "symbol": "SOLUSDT",
    "side": "BUY",
    "type": "STOP_MARKET",
    "qty": "3", 
    "direction": "SHORT",
    "created_at": 1749037471697,
    "ask_price": "155.7"
}



def newFilledSLOrder():
    return {
    "e": "ORDER_TRADE_UPDATE",
    "T": 1749038674248,
    "E": 1749038674248,
    "o": {
        "s": "SOLUSDT",
        "c": "3",
        "S": "SELL",
        "o": "MARKET",
        "f": "GTC",
        "q": "0.09",
        "p": "0",
        "ap": "156.02",
        "sp": "156.02",
        "x": "TRADE",
        "X": "FILLED",
        "i": 121115517313,
        "l": "0.09",
        "z": "0.09",
        "L": "156.02",
        "n": "0.0070209",
        "N": "USDT",
        "T": 1749038674248,
        "t": 2369877422,
        "b": "0",
        "a": "0",
        "m": False,
        "R": True,
        "wt": "CONTRACT_PRICE",
        "ot": "STOP_MARKET",
        "ps": "BOTH",
        "cp": True,
        "rp": "-0.00359999",
        "pP": False,
        "si": 0,
        "ss": 0,
        "V": "EXPIRE_MAKER",
        "pm": "NONE",
        "gtd": 0
    }
}

def newParsedFilledSLOrder():
    return {
    "order_id": 6,
    "status": "FILLED",
    "symbol": "SOLUSDT",
    "side": "BUY",
    "type": "STOP_MARKET",
    "qty": "3",
    "direction": "SHORT",
    "filled_price": "156.02",
    "updated_at": 1749038674248
}

def newCancelOrder():
    return {
    "e": "ORDER_TRADE_UPDATE",
    "T": 1749008243657,
    "E": 1749008243657,
    "o": {
        "s": "SOLUSDT",
        "c": "3",
        "S": "SELL",
        "o": "STOP_MARKET",
        "f": "GTC",
        "q": "0",
        "p": "0",
        "ap": "0",
        "sp": "4",
        "x": "CANCELED",
        "X": "CANCELED",
        "i": 121046588788,
        "l": "0",
        "z": "0",
        "L": "0",
        "n": "0",
        "N": "USDT",
        "T": 1749008243657,
        "t": 0,
        "b": "0",
        "a": "0",
        "m": False,
        "R": True,
        "wt": "CONTRACT_PRICE",
        "ot": "STOP_MARKET",
        "ps": "BOTH",
        "cp": True,
        "rp": "0",
        "pP": False,
        "si": 0,
        "ss": 0,
        "V": "EXPIRE_MAKER",
        "pm": "NONE",
        "gtd": 0
    }
}

def newParsedCancelOrder():
    return {
    "order_id": 3,
    "status": "CANCELED",
    "symbol": "SOLUSDT",
    "side": "SELL",
    "type": "STOP_MARKET",
    "qty": "0",
    "direction": "LONG",
    "updated_at": 1749008243657
}

