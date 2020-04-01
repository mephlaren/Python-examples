#coding=ISO-8859-2

#oanda trading API
import requests
from requests.auth import HTTPDigestAuth
import json
import datetime
import get_instument 


class OandaClient:


    def __init__(self, token,  instrument, session_id, session_name, Logger,  env = "Sandbox", version = "v3"   ):
        self.token = token
        self.instrument = instrument
        self.SESSION_ID = session_id
        self.SESSION_NAME = session_name
        self.session_trade_nr = 0

        self.last_errorcode = None
        if env =='Sandbox':
            self.URL = 'https://api-fxpractice.oanda.com'
        elif env == 'Trade':
            self.URL = "https://api-fxtrade.oanda.com"
        self.version = version
        self.state = "Alive"
        self.Logger = Logger

    def getEnv(self):
        return self.URL
    def getAccountIDs (self,  ) : 
        # http://developer.oanda.com/rest-live-v20/account-ep/
        r = requests.get("{0}/{1}/accounts".format(self.URL, self.version),
                     headers={"Authorization": 'Bearer {0}'.format(self.token)})

        self.Logger.log(str(r.status_code), "Client statuscode")
        self.last_errorcode = r.status_code
        if r.status_code != 200:
            self.Logger.log(r.text, "Client error")

        nr_of_accs = 10
        print('getAccountIDs raw')
        print(r.raw)
        try:
            try: 
                accountdata = json.loads(r.text) 
            except: pass
            accounts = []
            print("ACCDATA: ".format(accountdata)) 
            i = 0 

            for f,v  in accountdata.items():
                try:
                    for i in range  (0,nr_of_accs):
                            accounts.append(v[i ].get('id'))
                except: continue

                #növeljük a ciklusváltozónkat

            print("ACCOUNTS: {0}".format(accounts))
            self.account_nr = nr_of_accs
            return accounts
        except requests.HTTPError:
            print("HTTP Error:{0}".format(str(requests.HTTPError.response)))

    def __SET_ACCOUNT_TO_USE__(self, NR):
       return  self.getAccountIDs()[NR]

    def getAccountData(self) :
        try:
            r=requests.get("{0}/{1}/{2}/{3}".format(self.URL, self.version, "accounts", self.acct_id), headers={"Authorization":'Bearer {0}'.format(self.token), 'accountID': self.acct_id} )
            accountData = json.loads(r.text)

            self.Logger.log(str(r.status_code), "Client statuscode")
            self.last_errorcode = r.status_code
            if r.status_code != 200:

                self.Logger.log(r.text, "Client error")

            print('getAccountData raw')
            print(r.text)
            print("AccountData:\n{0}".format(accountData))
            self.Logger.log("Account Data", "Client event")
            self.fetch_errno = 0
            for key, value in accountData.items():
                if (key == 'account'):
                    try:
                        self.currency = value['currency']
                    except:
                        print('F001')
                        self.fetch_errno =  self.fetch_errno + 1
                        pass
                    try:
                        self.marginRate = value['marginRate']
                    except:
                        print('F002')
                        self.fetch_errno =  self.fetch_errno + 1
                        pass
                    try:
                        self.lastTransID = value['lastTransactionID']
                    except:
                        print('F003')
                        self.fetch_errno =  self.fetch_errno + 1
                        pass
                    try:
                        self.balance = value['balance']
                    except:
                        print('F004')
                        self.fetch_errno =  self.fetch_errno + 1
                        pass
                    try:
                        self.opentrcnt = value['openTradeCount']
                    except:
                        print('F005')
                        self.fetch_errno =  self.fetch_errno + 1
                        pass
                    try:
                        self.openposcnt = value['openPositionCount']
                    except:
                        print('F006')
                        self.fetch_errno =  self.fetch_errno + 1
                        pass
                    try:
                        self.pendingordcnt = value['pendingOrderCount']
                    except:
                        print('F007')
                        self.fetch_errno =  self.fetch_errno + 1
                        pass
                    try:
                        self.comission = value['comission']
                    except:
                       print('F008')
                       self.fetch_errno =  self.fetch_errno + 1
                       pass
                    try:
                        self.orders = value['orders']
                    except:
                        print('F009')
                        self.fetch_errno =  self.fetch_errno + 1
                        pass
                    try:
                        self.positions = value['positions']
                    except:
                        print('F010')
                        self.fetch_errno =  self.fetch_errno + 1
                        pass
                    try:
                        self.trades = value['trades']
                    except:
                        print('F011')
                        self.fetch_errno =  self.fetch_errno + 1
                        pass
                    try:
                        self.NetAssetValue = value['NAV']
                    except:
                        print('F012')
                        self.fetch_errno =  self.fetch_errno + 1
                        pass
                    try:
                        self.marginUsed = value['marginUsed']
                    except:
                        print('F013')
                        self.fetch_errno =  self.fetch_errno + 1
                        pass
                    try:
                        self.maringAvailable = value['marginAvailable']
                    except:
                        print('F014')
                        self.fetch_errno =  self.fetch_errno + 1
                        pass
                    try:
                        self.posValue = value['positionValue']
                        pass
                    finally:
                        print('Fetching is complete')
                        print("Number of fetching errors: {0}".format(self.fetch_errno))
                        self.Logger.log('Fetching is complete', "Client event")
                        self.Logger.log("Number of fetching errors: {0}".format(self.fetch_errno), "Client event")
                        if self.fetch_errno == 14 :
                            self.Logger.log('F015', "Client event")
                            print('F015')


        except:
            print("NV002")
            self.Logger.log("NV002", "Client event")
    def __AutoHandleAccountAuth__(self,  acct_base, acct_nr = 1):
        try:
            if acct_base == 'NR':
                self.acct_id = self.__SET_ACCOUNT_TO_USE__(int(acct_nr))
            if acct_base == 'ID':
                self.acct_id = acct_nr
            print("AU001 - {0}".format(self.acct_id))
            self.Logger.log("AU001", "Client event")
        except requests.ConnectionError:

            self.Logger.log("AU002", "Client event")
            print("AU002")
        except requests.ConnectTimeout:

            self.Logger.log("AU003", "Client event")
            print("AU003")
        try:
           self.getAccountData()
        except:

            self.Logger.log("NV001", "Client event")
            print("NV001")
        finally:
            self.Logger.log("________________________AU004______________________________", "Client event")
            print("\n\n")

    def getInstrumentHistory(self,
                             granularity,
                             price,
                             instrument,
                             is_date_range,
                             from_dt=0,
                             to_dt=0,
                             count = 500
                             ):
        self.inst_hist_start_date = from_dt
        self.inst_hist_end_date   = to_dt
        if is_date_range:

            req = requests.get("{0}/{1}/instruments/{2}/candles".format(self.URL, self.version, instrument),
                               headers={'Authorization': 'Bearer {0}'.format(self.token),
                                        'Accept-Datetime-Format':'{0}'.format('RFC3339')
                                        },
                               params={

                                        'price': '{0}'.format(price),
                                        'granularity': '{0}'.format(granularity),
                                        'from':  '{0}'.format(from_dt),
                                        'to':  '{0}'.format(to_dt),
                                        'smooth': 'False',  # .format(smooth),
                                        'includeFirst': 'True',  
                                        'dailyAlignment': '17',  ,
                                        'alignmentTimezone': 'America/New_York',   
                                        'weeklyAlignment': 'Friday'   
                })
        else:
            req = requests.get("{0}/{1}/instruments/{2}/candles".format(self.URL, self.version, instrument),
                               headers={'Authorization': 'Bearer {0}'.format(self.token),
                                        'Accept-Datetime-Format': '{0}'.format('RFC3339')
                                        },
                               params={

                                   'price': '{0}'.format(price),
                                   'granularity': '{0}'.format(granularity),
                                   'count': '{0}'.format(count),
                                   'smooth': 'False',  
                                   'dailyAlignment': '17',   
                                   'alignmentTimezone': 'America/New_York',  
                                   'weeklyAlignment': 'Friday'   
                               })

        print(str(req.status_code))
        self.Logger.log(str(req.status_code) , "Client statuscode")
        self.last_errorcode = req.status_code
        if req.status_code != 200:
            self.Logger.log(req.text, "Client error")

        pricing = json.loads(req.text) 
        return pricing


    def GetState(self):
        return self.state

    def GetAccountTrades(self):
        req = requests.get("{0}/{1}/accounts/{2}/trades".format(self.URL, self.version, self.acct_id),
                           headers={'Authorization': 'Bearer {0}'.format(self.token),
                                    'Accept-Datetime-Format': '{0}'.format('RFC3339')
                                    },
                           params={

                               'instrument': '{0}'.format(self.instrument)
                           })

        print(req)
        print(req.text)
        self.Logger.log(str(req.status_code) , "Client statuscode")
        self.last_errorcode = req.status_code
        if req.status_code != 200:
            self.Logger.log(req.text, "Client error")
        data = json.loads(req.text)
        for key, value in data.items():
            if key == "lastTransactionID":
               self.lastTransID = int(value)-1
        print("Last trade id: {0}".format(self.lastTransID))


    def openTrade(self, stoploss, units,  price = 0):  # BUY - SEL

        req = requests.post("{0}/{1}/accounts/{2}/orders".format(self.URL, self.version, self.acct_id, ),
                            headers={'Authorization': 'Bearer {0}'.format(self.token),
                                     'Accept-Datetime-Format': '{0}'.format('RFC3339')
                                     },
                            json={

                                "order": { 
                                    "stopLossOnFill": {
                                        "timeInForce": "GTC",
                                        "price":  "{0}".format(stoploss.__str__()),
                                        "tradeID" :   "{0}".format( (self.lastTransID-1).__str__())
                                    }, 
                                    "timeInForce": "FOK",
                                    "instrument": self.instrument,
                                    "units": "{0}".format(units.__str__()),
                                    "type": "MARKET",
                                    "positionFill": "OPEN_ONLY",
                                    "clientExtensions": {
                                        "comment": "{0}".format(self.SESSION_NAME),
                                        "tag": "{0}".format(self.SESSION_ID),
                                        "id": '{0}'.format((self.lastTransID+1).__str__())
                                    },

                                }

                            })

        print(req)
        print(req.text)

        self.Logger.log(str(req.status_code) , "Client statuscode")
        self.last_errorcode = req.status_code
        if req.status_code != 200:
            self.Logger.log(req.text, "Client error")
        self.session_trade_nr = self.session_trade_nr + 1
        print('trade nr in session: {0}'.format(self.session_trade_nr) )

    def createTrailingStopLoss(self, TSL, id=None):  # BUY - SEL
        if id == None:
            self.GetAccountTrades()
            id = self.lastTransID

        req = requests.put(
            "{0}/{1}/accounts/{2}/trades/{3}/orders".format(self.URL, self.version, self.acct_id, id),
            headers={'Authorization': 'Bearer {0}'.format(self.token),
                     'Accept-Datetime-Format': '{0}'.format('RFC3339')
                     },
            json={


                    "trailingStopLoss": {
                        "timeInForce": "GTC",
                        "distance": "{0}".format(TSL)
                    }


            })

        print(req)
        print(req.text)

        self.Logger.log(str(req.status_code), "Client statuscode")
        self.Logger.log(req.text, "Client error")
        self.last_errorcode = req.status_code
        if req.status_code != 200:
            self.Logger.log(req.text, "Client error")
        self.session_trade_nr = self.session_trade_nr + 1
        print('trailing stop set to: {0} @trade {1}'.format(TSL, id))

    def closeTrade(self):
        pass

    def getBalance(self):
        self.getAccountData()
        return self.balance





''' DEPRECATED --- UNUSED 
    def getLivePrices(self):
        #TODO : GET LIVE PRICES FROM STREAM
        pass
    def BuyPosition(self):
        #TODO: BUY A POSITION
        pass
    def SellPosition(self):
        #TODO: SELL A POSITION
        pass
    def CreateMarketOrder(self):
        #TODO : CREATE AN ORDER
        pass'''

