'use strict';

//  ---------------------------------------------------------------------------

const Exchange = require ('./base/Exchange');
const { ExchangeError } = require ('./base/errors');

//  ---------------------------------------------------------------------------

module.exports = class mixcoins extends Exchange {
    describe () {
        return this.deepExtend (super.describe (), {
            'id': 'mixcoins',
            'name': 'MixCoins',
            'countries': [ 'GB', 'HK' ],
            'rateLimit': 1500,
            'version': 'v1',
            'has': {
                'CORS': false,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/30237212-ed29303c-9535-11e7-8af8-fcd381cfa20c.jpg',
                'api': 'https://mixcoins.com/api',
                'www': 'https://mixcoins.com',
                'doc': 'https://mixcoins.com/help/api/',
            },
            'api': {
                'public': {
                    'get': [
                        'ticker',
                        'trades',
                        'depth',
                    ],
                },
                'private': {
                    'post': [
                        'cancel',
                        'info',
                        'orders',
                        'order',
                        'transactions',
                        'trade',
                    ],
                },
            },
            'markets': {
                'BTC/USD': { 'id': 'btc_usd', 'symbol': 'BTC/USD', 'base': 'BTC', 'quote': 'USD', 'baseId': 'btc', 'quoteId': 'usd', 'maker': 0.0015, 'taker': 0.0025 },
                'ETH/BTC': { 'id': 'eth_btc', 'symbol': 'ETH/BTC', 'base': 'ETH', 'quote': 'BTC', 'baseId': 'eth', 'quoteId': 'btc', 'maker': 0.001, 'taker': 0.0015 },
                'BCH/BTC': { 'id': 'bch_btc', 'symbol': 'BCH/BTC', 'base': 'BCH', 'quote': 'BTC', 'baseId': 'bch', 'quoteId': 'btc', 'maker': 0.001, 'taker': 0.0015 },
                'LSK/BTC': { 'id': 'lsk_btc', 'symbol': 'LSK/BTC', 'base': 'LSK', 'quote': 'BTC', 'baseId': 'lsk', 'quoteId': 'btc', 'maker': 0.0015, 'taker': 0.0025 },
                'BCH/USD': { 'id': 'bch_usd', 'symbol': 'BCH/USD', 'base': 'BCH', 'quote': 'USD', 'baseId': 'bch', 'quoteId': 'usd', 'maker': 0.001, 'taker': 0.0015 },
                'ETH/USD': { 'id': 'eth_usd', 'symbol': 'ETH/USD', 'base': 'ETH', 'quote': 'USD', 'baseId': 'eth', 'quoteId': 'usd', 'maker': 0.001, 'taker': 0.0015 },
            },
        });
    }

    async fetchBalance (params = {}) {
        await this.loadMarkets ();
        const response = await this.privatePostInfo (params);
        const balance = this.safeValue (response['result'], 'wallet');
        const result = { 'info': balance };
        const currencies = Object.keys (this.currencies);
        for (let i = 0; i < currencies.length; i++) {
            const code = currencies[i];
            const currencyId = this.currencyid (code);
            const account = this.account ();
            if (currencyId in balance) {
                account['free'] = this.safeFloat (balance[currencyId], 'avail');
                account['used'] = this.safeFloat (balance[currencyId], 'lock');
                account['total'] = this.sum (account['free'], account['used']);
            }
            result[code] = account;
        }
        return this.parseBalance (result);
    }

    async fetchOrderBook (symbol, limit = undefined, params = {}) {
        await this.loadMarkets ();
        const request = {
            'market': this.marketId (symbol),
        };
        const response = await this.publicGetDepth (this.extend (request, params));
        return this.parseOrderBook (response['result']);
    }

    async fetchTicker (symbol, params = {}) {
        await this.loadMarkets ();
        const request = {
            'market': this.marketId (symbol),
        };
        const response = await this.publicGetTicker (this.extend (request, params));
        const ticker = this.safeValue (response, 'result');
        const timestamp = this.milliseconds ();
        const last = this.safeFloat (ticker, 'last');
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': this.iso8601 (timestamp),
            'high': this.safeFloat (ticker, 'high'),
            'low': this.safeFloat (ticker, 'low'),
            'bid': this.safeFloat (ticker, 'buy'),
            'bidVolume': undefined,
            'ask': this.safeFloat (ticker, 'sell'),
            'askVolume': undefined,
            'vwap': undefined,
            'open': undefined,
            'close': last,
            'last': last,
            'previousClose': undefined,
            'change': undefined,
            'percentage': undefined,
            'average': undefined,
            'baseVolume': this.safeFloat (ticker, 'vol'),
            'quoteVolume': undefined,
            'info': ticker,
        };
    }

    parseTrade (trade, market) {
        const timestamp = parseInt (trade['date']) * 1000;
        return {
            'id': trade['id'].toString (),
            'info': trade,
            'timestamp': timestamp,
            'datetime': this.iso8601 (timestamp),
            'symbol': market['symbol'],
            'type': undefined,
            'side': undefined,
            'price': this.safeFloat (trade, 'price'),
            'amount': this.safeFloat (trade, 'amount'),
        };
    }

    async fetchTrades (symbol, since = undefined, limit = undefined, params = {}) {
        await this.loadMarkets ();
        const market = this.market (symbol);
        const request = {
            'market': market['id'],
        };
        const response = await this.publicGetTrades (this.extend (request, params));
        return this.parseTrades (response['result'], market, since, limit);
    }

    async createOrder (symbol, type, side, amount, price = undefined, params = {}) {
        await this.loadMarkets ();
        const request = {
            'market': this.marketId (symbol),
            'op': side,
            'amount': amount,
        };
        if (type === 'market') {
            request['order_type'] = 1;
            request['price'] = price;
        } else {
            request['order_type'] = 0;
        }
        const response = await this.privatePostTrade (this.extend (request, params));
        return {
            'info': response,
            'id': response['result']['id'].toString (),
        };
    }

    async cancelOrder (id, symbol = undefined, params = {}) {
        await this.loadMarkets ();
        const request = {
            'id': id,
        };
        return await this.privatePostCancel (this.extend (request, params));
    }

    sign (path, api = 'public', method = 'GET', params = {}, headers = undefined, body = undefined) {
        let url = this.urls['api'] + '/' + this.version + '/' + path;
        if (api === 'public') {
            if (Object.keys (params).length) {
                url += '?' + this.urlencode (params);
            }
        } else {
            this.checkRequiredCredentials ();
            let nonce = this.nonce ();
            body = this.urlencode (this.extend ({
                'nonce': nonce,
            }, params));
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Key': this.apiKey,
                'Sign': this.hmac (this.encode (body), this.secret, 'sha512'),
            };
        }
        return { 'url': url, 'method': method, 'body': body, 'headers': headers };
    }

    async request (path, api = 'public', method = 'GET', params = {}, headers = undefined, body = undefined) {
        const response = await this.fetch2 (path, api, method, params, headers, body);
        if ('status' in response) {
            if (response['status'] === 200) {
                return response;
            }
        }
        throw new ExchangeError (this.id + ' ' + this.json (response));
    }
};
