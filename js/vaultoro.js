'use strict';

// ---------------------------------------------------------------------------

const Exchange = require ('./base/Exchange');

// ---------------------------------------------------------------------------

module.exports = class vaultoro extends Exchange {
    describe () {
        return this.deepExtend (super.describe (), {
            'id': 'vaultoro',
            'name': 'Vaultoro',
            'countries': [ 'CH' ],
            'rateLimit': 1000,
            'version': '1',
            'has': {
                'CORS': true,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/27766880-f205e870-5ee9-11e7-8fe2-0d5b15880752.jpg',
                'api': 'https://api.vaultoro.com',
                'www': 'https://www.vaultoro.com',
                'doc': 'https://api.vaultoro.com',
            },
            'commonCurrencies': {
                'GLD': 'Gold',
            },
            'api': {
                'public': {
                    'get': [
                        'bidandask',
                        'buyorders',
                        'latest',
                        'latesttrades',
                        'markets',
                        'orderbook',
                        'sellorders',
                        'transactions/day',
                        'transactions/hour',
                        'transactions/month',
                    ],
                },
                'private': {
                    'get': [
                        'balance',
                        'mytrades',
                        'orders',
                    ],
                    'post': [
                        'buy/{symbol}/{type}',
                        'cancel/{id}',
                        'sell/{symbol}/{type}',
                        'withdraw',
                    ],
                },
            },
        });
    }

    async fetchMarkets (params = {}) {
        let result = [];
        let markets = await this.publicGetMarkets ();
        let market = markets['data'];
        let baseId = market['MarketCurrency'];
        let quoteId = market['BaseCurrency'];
        let base = this.commonCurrencyCode (baseId);
        let quote = this.commonCurrencyCode (quoteId);
        let symbol = base + '/' + quote;
        let id = market['MarketName'];
        result.push ({
            'id': id,
            'symbol': symbol,
            'base': base,
            'quote': quote,
            'baseId': baseId,
            'quoteId': quoteId,
            'info': market,
        });
        return result;
    }

    async fetchBalance (params = {}) {
        await this.loadMarkets ();
        const response = await this.privateGetBalance (params);
        const balances = this.safeValue (response, 'data');
        const result = { 'info': balances };
        for (let i = 0; i < balances.length; i++) {
            const balance = balances[i];
            const currencyId = balance['currency_code'];
            const uppercaseId = currencyId.toUpperCase ();
            const code = this.commonCurrencyCode (uppercaseId);
            const free = this.safeFloat (balance, 'cash');
            const used = this.safeFloat (balance, 'reserved');
            const total = this.sum (free, used);
            const account = {
                'free': free,
                'used': used,
                'total': total,
            };
            result[code] = account;
        }
        return this.parseBalance (result);
    }

    async fetchOrderBook (symbol, limit = undefined, params = {}) {
        await this.loadMarkets ();
        const response = await this.publicGetOrderbook (params);
        const orderbook = {
            'bids': response['data'][0]['b'],
            'asks': response['data'][1]['s'],
        };
        return this.parseOrderBook (orderbook, undefined, 'bids', 'asks', 'Gold_Price', 'Gold_Amount');
    }

    async fetchTicker (symbol, params = {}) {
        await this.loadMarkets ();
        let quote = await this.publicGetBidandask (params);
        let bidsLength = quote['bids'].length;
        let bid = quote['bids'][bidsLength - 1];
        let ask = quote['asks'][0];
        let response = await this.publicGetMarkets (params);
        let ticker = response['data'];
        let timestamp = this.milliseconds ();
        let last = this.safeFloat (ticker, 'LastPrice');
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': this.iso8601 (timestamp),
            'high': this.safeFloat (ticker, '24hHigh'),
            'low': this.safeFloat (ticker, '24hLow'),
            'bid': bid[0],
            'bidVolume': undefined,
            'ask': ask[0],
            'askVolume': undefined,
            'vwap': undefined,
            'open': undefined,
            'close': last,
            'last': last,
            'previousClose': undefined,
            'change': undefined,
            'percentage': undefined,
            'average': undefined,
            'baseVolume': undefined,
            'quoteVolume': this.safeFloat (ticker, '24hVolume'),
            'info': ticker,
        };
    }

    parseTrade (trade, market) {
        const timestamp = this.parse8601 (this.safeString (trade, 'Time'));
        return {
            'id': undefined,
            'info': trade,
            'timestamp': timestamp,
            'datetime': this.iso8601 (timestamp),
            'symbol': market['symbol'],
            'order': undefined,
            'type': undefined,
            'side': undefined,
            'price': trade['Gold_Price'],
            'amount': trade['Gold_Amount'],
        };
    }

    async fetchTrades (symbol, since = undefined, limit = undefined, params = {}) {
        await this.loadMarkets ();
        const market = this.market (symbol);
        const response = await this.publicGetTransactionsDay (params);
        return this.parseTrades (response, market, since, limit);
    }

    async createOrder (symbol, type, side, amount, price = undefined, params = {}) {
        await this.loadMarkets ();
        const market = this.market (symbol);
        const method = 'privatePost' + this.capitalize (side) + 'SymbolType';
        const request = {
            'symbol': market['quoteId'].toLowerCase (),
            'type': type,
            'gld': amount,
            'price': price || 1,
        };
        const response = await this[method] (this.extend (request, params));
        return {
            'info': response,
            'id': response['data']['Order_ID'],
        };
    }

    async cancelOrder (id, symbol = undefined, params = {}) {
        await this.loadMarkets ();
        const request = {
            'id': id,
        };
        return await this.privatePostCancelId (this.extend (request, params));
    }

    sign (path, api = 'public', method = 'GET', params = {}, headers = undefined, body = undefined) {
        let url = this.urls['api'] + '/';
        if (api === 'public') {
            url += path;
        } else {
            this.checkRequiredCredentials ();
            let nonce = this.nonce ();
            url += this.version + '/' + this.implodeParams (path, params);
            let query = this.extend ({
                'nonce': nonce,
                'apikey': this.apiKey,
            }, this.omit (params, this.extractParams (path)));
            url += '?' + this.urlencode (query);
            headers = {
                'Content-Type': 'application/json',
                'X-Signature': this.hmac (this.encode (url), this.encode (this.secret)),
            };
        }
        return { 'url': url, 'method': method, 'body': body, 'headers': headers };
    }
};
