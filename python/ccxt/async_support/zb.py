# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange
import hashlib
import math
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import OrderNotFound
from ccxt.base.errors import DDoSProtection
from ccxt.base.errors import ExchangeNotAvailable


class zb (Exchange):

    def describe(self):
        return self.deep_extend(super(zb, self).describe(), {
            'id': 'zb',
            'name': 'ZB',
            'countries': ['CN'],
            'rateLimit': 1000,
            'version': 'v1',
            'has': {
                'CORS': False,
                'createMarketOrder': False,
                'fetchDepositAddress': True,
                'fetchOrder': True,
                'fetchOrders': True,
                'fetchOpenOrders': True,
                'fetchOHLCV': True,
                'fetchTickers': True,
                'withdraw': True,
            },
            'timeframes': {
                '1m': '1min',
                '3m': '3min',
                '5m': '5min',
                '15m': '15min',
                '30m': '30min',
                '1h': '1hour',
                '2h': '2hour',
                '4h': '4hour',
                '6h': '6hour',
                '12h': '12hour',
                '1d': '1day',
                '3d': '3day',
                '1w': '1week',
            },
            'exceptions': {
                # '1000': 'Successful operation',
                '1001': ExchangeError,  # 'General error message',
                '1002': ExchangeError,  # 'Internal error',
                '1003': AuthenticationError,  # 'Verification does not pass',
                '1004': AuthenticationError,  # 'Funding security password lock',
                '1005': AuthenticationError,  # 'Funds security password is incorrect, please confirm and re-enter.',
                '1006': AuthenticationError,  # 'Real-name certification pending approval or audit does not pass',
                '1009': ExchangeNotAvailable,  # 'This interface is under maintenance',
                '2001': InsufficientFunds,  # 'Insufficient CNY Balance',
                '2002': InsufficientFunds,  # 'Insufficient BTC Balance',
                '2003': InsufficientFunds,  # 'Insufficient LTC Balance',
                '2005': InsufficientFunds,  # 'Insufficient ETH Balance',
                '2006': InsufficientFunds,  # 'Insufficient ETC Balance',
                '2007': InsufficientFunds,  # 'Insufficient BTS Balance',
                '2009': InsufficientFunds,  # 'Account balance is not enough',
                '3001': OrderNotFound,  # 'Pending orders not found',
                '3002': InvalidOrder,  # 'Invalid price',
                '3003': InvalidOrder,  # 'Invalid amount',
                '3004': AuthenticationError,  # 'User does not exist',
                '3005': ExchangeError,  # 'Invalid parameter',
                '3006': AuthenticationError,  # 'Invalid IP or inconsistent with the bound IP',
                '3007': AuthenticationError,  # 'The request time has expired',
                '3008': OrderNotFound,  # 'Transaction records not found',
                '4001': ExchangeNotAvailable,  # 'API interface is locked or not enabled',
                '4002': DDoSProtection,  # 'Request too often',
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/32859187-cd5214f0-ca5e-11e7-967d-96568e2e2bd1.jpg',
                'api': {
                    'public': 'http://api.zb.cn/data',  # no https for public API
                    'private': 'https://trade.zb.cn/api',
                },
                'www': 'https://www.zb.com',
                'doc': 'https://www.zb.com/i/developer',
                'fees': 'https://www.zb.com/i/rate',
                'referral': 'https://vip.zb.com/user/register?recommendCode=bn070u',
            },
            'api': {
                'public': {
                    'get': [
                        'markets',
                        'ticker',
                        'allTicker',
                        'depth',
                        'trades',
                        'kline',
                    ],
                },
                'private': {
                    'get': [
                        # spot API
                        'order',
                        'cancelOrder',
                        'getOrder',
                        'getOrders',
                        'getOrdersNew',
                        'getOrdersIgnoreTradeType',
                        'getUnfinishedOrdersIgnoreTradeType',
                        'getAccountInfo',
                        'getUserAddress',
                        'getWithdrawAddress',
                        'getWithdrawRecord',
                        'getChargeRecord',
                        'getCnyWithdrawRecord',
                        'getCnyChargeRecord',
                        'withdraw',
                        # leverage API
                        'getLeverAssetsInfo',
                        'getLeverBills',
                        'transferInLever',
                        'transferOutLever',
                        'loan',
                        'cancelLoan',
                        'getLoans',
                        'getLoanRecords',
                        'borrow',
                        'repay',
                        'getRepayments',
                    ],
                },
            },
            'fees': {
                'funding': {
                    'withdraw': {
                        'BTC': 0.0001,
                        'BCH': 0.0006,
                        'LTC': 0.005,
                        'ETH': 0.01,
                        'ETC': 0.01,
                        'BTS': 3,
                        'EOS': 1,
                        'QTUM': 0.01,
                        'HSR': 0.001,
                        'XRP': 0.1,
                        'USDT': '0.1%',
                        'QCASH': 5,
                        'DASH': 0.002,
                        'BCD': 0,
                        'UBTC': 0,
                        'SBTC': 0,
                        'INK': 20,
                        'TV': 0.1,
                        'BTH': 0,
                        'BCX': 0,
                        'LBTC': 0,
                        'CHAT': 20,
                        'bitCNY': 20,
                        'HLC': 20,
                        'BTP': 0,
                        'BCW': 0,
                    },
                },
                'trading': {
                    'maker': 0.2 / 100,
                    'taker': 0.2 / 100,
                },
            },
            'commonCurrencies': {
                'ENT': 'ENTCash',
            },
        })

    async def fetch_markets(self, params={}):
        markets = await self.publicGetMarkets()
        keys = list(markets.keys())
        result = []
        for i in range(0, len(keys)):
            id = keys[i]
            market = markets[id]
            baseId, quoteId = id.split('_')
            base = self.common_currency_code(baseId.upper())
            quote = self.common_currency_code(quoteId.upper())
            symbol = base + '/' + quote
            precision = {
                'amount': market['amountScale'],
                'price': market['priceScale'],
            }
            result.append({
                'id': id,
                'symbol': symbol,
                'baseId': baseId,
                'quoteId': quoteId,
                'base': base,
                'quote': quote,
                'active': True,
                'precision': precision,
                'limits': {
                    'amount': {
                        'min': math.pow(10, -precision['amount']),
                        'max': None,
                    },
                    'price': {
                        'min': math.pow(10, -precision['price']),
                        'max': None,
                    },
                    'cost': {
                        'min': 0,
                        'max': None,
                    },
                },
                'info': market,
            })
        return result

    async def fetch_balance(self, params={}):
        await self.load_markets()
        response = await self.privateGetGetAccountInfo(params)
        # todo: use self somehow
        # permissions = response['result']['base']
        balances = response['result']['coins']
        result = {'info': response}
        for i in range(0, len(balances)):
            balance = balances[i]
            #     {       enName: "BTC",
            #               freez: "0.00000000",
            #         unitDecimal:  8,  # always 8
            #              cnName: "BTC",
            #       isCanRecharge:  True,  # TODO: should use self
            #             unitTag: "฿",
            #       isCanWithdraw:  True,  # TODO: should use self
            #           available: "0.00000000",
            #                 key: "btc"         }
            account = self.account()
            currency = balance['key']
            if currency in self.currencies_by_id:
                currency = self.currencies_by_id[currency]['code']
            else:
                currency = self.common_currency_code(balance['enName'])
            account['free'] = float(balance['available'])
            account['used'] = float(balance['freez'])
            account['total'] = self.sum(account['free'], account['used'])
            result[currency] = account
        return self.parse_balance(result)

    def get_market_field_name(self):
        return 'market'

    async def fetch_deposit_address(self, code, params={}):
        await self.load_markets()
        currency = self.currency(code)
        response = await self.privateGetGetUserAddress({
            'currency': currency['id'],
        })
        address = response['message']['datas']['key']
        tag = None
        if address.find('_') >= 0:
            arr = address.split('_')
            address = arr[0]  # WARNING: MAY BE tag_address INSTEAD OF address_tag FOR SOME CURRENCIESnot !
            tag = arr[1]
        return {
            'currency': code,
            'address': address,
            'tag': tag,
            'info': response,
        }

    async def fetch_order_book(self, symbol, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        marketFieldName = self.get_market_field_name()
        request = {}
        request[marketFieldName] = market['id']
        orderbook = await self.publicGetDepth(self.extend(request, params))
        return self.parse_order_book(orderbook)

    async def fetch_tickers(self, symbols=None, params={}):
        await self.load_markets()
        response = await self.publicGetAllTicker(params)
        result = {}
        anotherMarketsById = {}
        marketIds = list(self.marketsById.keys())
        for i in range(0, len(marketIds)):
            tickerId = marketIds[i].replace('_', '')
            anotherMarketsById[tickerId] = self.marketsById[marketIds[i]]
        ids = list(response.keys())
        for i in range(0, len(ids)):
            market = anotherMarketsById[ids[i]]
            result[market['symbol']] = self.parse_ticker(response[ids[i]], market)
        return result

    async def fetch_ticker(self, symbol, params={}):
        await self.load_markets()
        market = self.market(symbol)
        marketFieldName = self.get_market_field_name()
        request = {}
        request[marketFieldName] = market['id']
        response = await self.publicGetTicker(self.extend(request, params))
        ticker = response['ticker']
        return self.parse_ticker(ticker, market)

    def parse_ticker(self, ticker, market=None):
        timestamp = self.milliseconds()
        symbol = None
        if market is not None:
            symbol = market['symbol']
        last = self.safe_float(ticker, 'last')
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(ticker, 'high'),
            'low': self.safe_float(ticker, 'low'),
            'bid': self.safe_float(ticker, 'buy'),
            'bidVolume': None,
            'ask': self.safe_float(ticker, 'sell'),
            'askVolume': None,
            'vwap': None,
            'open': None,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': None,
            'percentage': None,
            'average': None,
            'baseVolume': self.safe_float(ticker, 'vol'),
            'quoteVolume': None,
            'info': ticker,
        }

    async def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        if limit is None:
            limit = 1000
        request = {
            'market': market['id'],
            'type': self.timeframes[timeframe],
            'limit': limit,
        }
        if since is not None:
            request['since'] = since
        response = await self.publicGetKline(self.extend(request, params))
        data = self.safe_value(response, 'data', [])
        return self.parse_ohlcvs(data, market, timeframe, since, limit)

    def parse_trade(self, trade, market=None):
        timestamp = trade['date'] * 1000
        side = 'buy' if (trade['trade_type'] == 'bid') else 'sell'
        return {
            'info': trade,
            'id': str(trade['tid']),
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': market['symbol'],
            'type': None,
            'side': side,
            'price': self.safe_float(trade, 'price'),
            'amount': self.safe_float(trade, 'amount'),
        }

    async def fetch_trades(self, symbol, since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        marketFieldName = self.get_market_field_name()
        request = {}
        request[marketFieldName] = market['id']
        response = await self.publicGetTrades(self.extend(request, params))
        return self.parse_trades(response, market, since, limit)

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        if type != 'limit':
            raise InvalidOrder(self.id + ' allows limit orders only')
        await self.load_markets()
        order = {
            'price': self.price_to_precision(symbol, price),
            'amount': self.amount_to_precision(symbol, amount),
            'tradeType': '1' if (side == 'buy') else '0',
            'currency': self.market_id(symbol),
        }
        response = await self.privateGetOrder(self.extend(order, params))
        return {
            'info': response,
            'id': response['id'],
        }

    async def cancel_order(self, id, symbol=None, params={}):
        await self.load_markets()
        order = {
            'id': str(id),
            'currency': self.market_id(symbol),
        }
        order = self.extend(order, params)
        return await self.privateGetCancelOrder(order)

    async def fetch_order(self, id, symbol=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchOrder() requires a symbol argument')
        await self.load_markets()
        order = {
            'id': str(id),
            'currency': self.market_id(symbol),
        }
        order = self.extend(order, params)
        response = await self.privateGetGetOrder(order)
        #
        #     {
        #         'total_amount': 0.01,
        #         'id': '20180910244276459',
        #         'price': 180.0,
        #         'trade_date': 1536576744960,
        #         'status': 2,
        #         'trade_money': '1.96742',
        #         'trade_amount': 0.01,
        #         'type': 0,
        #         'currency': 'eth_usdt'
        #     }
        #
        return self.parse_order(response, None)

    async def fetch_orders(self, symbol=None, since=None, limit=50, params={}):
        if symbol is None:
            raise ExchangeError(self.id + 'fetchOrders requires a symbol parameter')
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'currency': market['id'],
            'pageIndex': 1,  # default pageIndex is 1
            'pageSize': limit,  # default pageSize is 50
        }
        method = 'privateGetGetOrdersIgnoreTradeType'
        # tradeType 交易类型1/0[buy/sell]
        if 'tradeType' in params:
            method = 'privateGetGetOrdersNew'
        response = None
        try:
            response = await getattr(self, method)(self.extend(request, params))
        except Exception as e:
            if isinstance(e, OrderNotFound):
                return []
            raise e
        return self.parse_orders(response, market, since, limit)

    async def fetch_open_orders(self, symbol=None, since=None, limit=10, params={}):
        if symbol is None:
            raise ExchangeError(self.id + 'fetchOpenOrders requires a symbol parameter')
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'currency': market['id'],
            'pageIndex': 1,  # default pageIndex is 1
            'pageSize': limit,  # default pageSize is 10
        }
        method = 'privateGetGetUnfinishedOrdersIgnoreTradeType'
        # tradeType 交易类型1/0[buy/sell]
        if 'tradeType' in params:
            method = 'privateGetGetOrdersNew'
        response = None
        try:
            response = await getattr(self, method)(self.extend(request, params))
        except Exception as e:
            if isinstance(e, OrderNotFound):
                return []
            raise e
        return self.parse_orders(response, market, since, limit)

    def parse_order(self, order, market=None):
        #
        # fetchOrder
        #
        #     {
        #         'total_amount': 0.01,
        #         'id': '20180910244276459',
        #         'price': 180.0,
        #         'trade_date': 1536576744960,
        #         'status': 2,
        #         'trade_money': '1.96742',
        #         'trade_amount': 0.01,
        #         'type': 0,
        #         'currency': 'eth_usdt'
        #     }
        #
        side = 'buy' if (order['type'] == 1) else 'sell'
        type = 'limit'  # market order is not availalbe in ZB
        timestamp = None
        createDateField = self.get_create_date_field()
        if createDateField in order:
            timestamp = order[createDateField]
        symbol = None
        if 'currency' in order:
            # get symbol from currency
            market = self.marketsById[order['currency']]
        if market:
            symbol = market['symbol']
        price = order['price']
        filled = order['trade_amount']
        amount = order['total_amount']
        remaining = amount - filled
        cost = self.safe_float(order, 'trade_money')
        average = None
        status = self.parse_order_status(self.safe_string(order, 'status'))
        if (cost is not None) and(filled is not None) and(filled > 0):
            average = cost / filled
        return {
            'info': order,
            'id': order['id'],
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'symbol': symbol,
            'type': type,
            'side': side,
            'price': price,
            'average': average,
            'cost': cost,
            'amount': amount,
            'filled': filled,
            'remaining': remaining,
            'status': status,
            'fee': None,
        }

    def parse_order_status(self, status):
        statuses = {
            '0': 'open',
            '1': 'canceled',
            '2': 'closed',
            '3': 'open',  # partial
        }
        return self.safe_string(statuses, status, status)

    def get_create_date_field(self):
        return 'trade_date'

    def nonce(self):
        return self.milliseconds()

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'][api]
        if api == 'public':
            url += '/' + self.version + '/' + path
            if params:
                url += '?' + self.urlencode(params)
        else:
            query = self.keysort(self.extend({
                'method': path,
                'accesskey': self.apiKey,
            }, params))
            nonce = self.nonce()
            query = self.keysort(query)
            auth = self.rawencode(query)
            secret = self.hash(self.encode(self.secret), 'sha1')
            signature = self.hmac(self.encode(auth), self.encode(secret), hashlib.md5)
            suffix = 'sign=' + signature + '&reqTime=' + str(nonce)
            url += '/' + path + '?' + auth + '&' + suffix
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, httpCode, reason, url, method, headers, body, response):
        if response is None:
            return  # fallback to default error handler
        if body[0] == '{':
            feedback = self.id + ' ' + body
            if 'code' in response:
                code = self.safe_string(response, 'code')
                if code in self.exceptions:
                    ExceptionClass = self.exceptions[code]
                    raise ExceptionClass(feedback)
                elif code != '1000':
                    raise ExchangeError(feedback)
            # special case for {"result":false,"message":"服务端忙碌"}(a "Busy Server" reply)
            result = self.safe_value(response, 'result')
            if result is not None:
                if not result:
                    message = self.safe_string(response, 'message')
                    if message == u'服务端忙碌':
                        raise ExchangeNotAvailable(feedback)
                    else:
                        raise ExchangeError(feedback)
