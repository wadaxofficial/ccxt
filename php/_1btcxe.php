<?php

namespace ccxt;

// PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
// https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

use Exception as Exception; // a common import

class _1btcxe extends Exchange {

    public function describe () {
        return array_replace_recursive (parent::describe (), array (
            'id' => '_1btcxe',
            'name' => '1BTCXE',
            'countries' => array ( 'PA' ), // Panama
            'comment' => 'Crypto Capital API',
            'has' => array (
                'CORS' => true,
                'withdraw' => true,
            ),
            'timeframes' => array (
                '1d' => '1year',
            ),
            'urls' => array (
                'logo' => 'https://user-images.githubusercontent.com/1294454/27766049-2b294408-5ecc-11e7-85cc-adaff013dc1a.jpg',
                'api' => 'https://1btcxe.com/api',
                'www' => 'https://1btcxe.com',
                'doc' => 'https://1btcxe.com/api-docs.php',
            ),
            'api' => array (
                'public' => array (
                    'get' => array (
                        'stats',
                        'historical-prices',
                        'order-book',
                        'transactions',
                    ),
                ),
                'private' => array (
                    'post' => array (
                        'balances-and-info',
                        'open-orders',
                        'user-transactions',
                        'btc-deposit-address/get',
                        'btc-deposit-address/new',
                        'deposits/get',
                        'withdrawals/get',
                        'orders/new',
                        'orders/edit',
                        'orders/cancel',
                        'orders/status',
                        'withdrawals/new',
                    ),
                ),
            ),
        ));
    }

    public function fetch_markets ($params = array ()) {
        return array (
            array( 'id' => 'USD', 'symbol' => 'BTC/USD', 'base' => 'BTC', 'quote' => 'USD' ),
            array( 'id' => 'EUR', 'symbol' => 'BTC/EUR', 'base' => 'BTC', 'quote' => 'EUR' ),
            array( 'id' => 'CNY', 'symbol' => 'BTC/CNY', 'base' => 'BTC', 'quote' => 'CNY' ),
            array( 'id' => 'RUB', 'symbol' => 'BTC/RUB', 'base' => 'BTC', 'quote' => 'RUB' ),
            array( 'id' => 'CHF', 'symbol' => 'BTC/CHF', 'base' => 'BTC', 'quote' => 'CHF' ),
            array( 'id' => 'JPY', 'symbol' => 'BTC/JPY', 'base' => 'BTC', 'quote' => 'JPY' ),
            array( 'id' => 'GBP', 'symbol' => 'BTC/GBP', 'base' => 'BTC', 'quote' => 'GBP' ),
            array( 'id' => 'CAD', 'symbol' => 'BTC/CAD', 'base' => 'BTC', 'quote' => 'CAD' ),
            array( 'id' => 'AUD', 'symbol' => 'BTC/AUD', 'base' => 'BTC', 'quote' => 'AUD' ),
            array( 'id' => 'AED', 'symbol' => 'BTC/AED', 'base' => 'BTC', 'quote' => 'AED' ),
            array( 'id' => 'BGN', 'symbol' => 'BTC/BGN', 'base' => 'BTC', 'quote' => 'BGN' ),
            array( 'id' => 'CZK', 'symbol' => 'BTC/CZK', 'base' => 'BTC', 'quote' => 'CZK' ),
            array( 'id' => 'DKK', 'symbol' => 'BTC/DKK', 'base' => 'BTC', 'quote' => 'DKK' ),
            array( 'id' => 'HKD', 'symbol' => 'BTC/HKD', 'base' => 'BTC', 'quote' => 'HKD' ),
            array( 'id' => 'HRK', 'symbol' => 'BTC/HRK', 'base' => 'BTC', 'quote' => 'HRK' ),
            array( 'id' => 'HUF', 'symbol' => 'BTC/HUF', 'base' => 'BTC', 'quote' => 'HUF' ),
            array( 'id' => 'ILS', 'symbol' => 'BTC/ILS', 'base' => 'BTC', 'quote' => 'ILS' ),
            array( 'id' => 'INR', 'symbol' => 'BTC/INR', 'base' => 'BTC', 'quote' => 'INR' ),
            array( 'id' => 'MUR', 'symbol' => 'BTC/MUR', 'base' => 'BTC', 'quote' => 'MUR' ),
            array( 'id' => 'MXN', 'symbol' => 'BTC/MXN', 'base' => 'BTC', 'quote' => 'MXN' ),
            array( 'id' => 'NOK', 'symbol' => 'BTC/NOK', 'base' => 'BTC', 'quote' => 'NOK' ),
            array( 'id' => 'NZD', 'symbol' => 'BTC/NZD', 'base' => 'BTC', 'quote' => 'NZD' ),
            array( 'id' => 'PLN', 'symbol' => 'BTC/PLN', 'base' => 'BTC', 'quote' => 'PLN' ),
            array( 'id' => 'RON', 'symbol' => 'BTC/RON', 'base' => 'BTC', 'quote' => 'RON' ),
            array( 'id' => 'SEK', 'symbol' => 'BTC/SEK', 'base' => 'BTC', 'quote' => 'SEK' ),
            array( 'id' => 'SGD', 'symbol' => 'BTC/SGD', 'base' => 'BTC', 'quote' => 'SGD' ),
            array( 'id' => 'THB', 'symbol' => 'BTC/THB', 'base' => 'BTC', 'quote' => 'THB' ),
            array( 'id' => 'TRY', 'symbol' => 'BTC/TRY', 'base' => 'BTC', 'quote' => 'TRY' ),
            array( 'id' => 'ZAR', 'symbol' => 'BTC/ZAR', 'base' => 'BTC', 'quote' => 'ZAR' ),
        );
    }

    public function fetch_balance ($params = array ()) {
        $response = $this->privatePostBalancesAndInfo ();
        $balance = $response['balances-and-info'];
        $result = array( 'info' => $balance );
        $currencies = is_array($this->currencies) ? array_keys($this->currencies) : array();
        for ($i = 0; $i < count ($currencies); $i++) {
            $currency = $currencies[$i];
            $account = $this->account ();
            $account['free'] = $this->safe_float($balance['available'], $currency, 0.0);
            $account['used'] = $this->safe_float($balance['on_hold'], $currency, 0.0);
            $account['total'] = $this->sum ($account['free'], $account['used']);
            $result[$currency] = $account;
        }
        return $this->parse_balance($result);
    }

    public function fetch_order_book ($symbol, $limit = null, $params = array ()) {
        $response = $this->publicGetOrderBook (array_merge (array (
            'currency' => $this->market_id($symbol),
        ), $params));
        return $this->parse_order_book($response['order-book'], null, 'bid', 'ask', 'price', 'order_amount');
    }

    public function fetch_ticker ($symbol, $params = array ()) {
        $response = $this->publicGetStats (array_merge (array (
            'currency' => $this->market_id($symbol),
        ), $params));
        $ticker = $response['stats'];
        $last = $this->safe_float($ticker, 'last_price');
        return array (
            'symbol' => $symbol,
            'timestamp' => null,
            'datetime' => null,
            'high' => $this->safe_float($ticker, 'max'),
            'low' => $this->safe_float($ticker, 'min'),
            'bid' => $this->safe_float($ticker, 'bid'),
            'bidVolume' => null,
            'ask' => $this->safe_float($ticker, 'ask'),
            'askVolume' => null,
            'vwap' => null,
            'open' => $this->safe_float($ticker, 'open'),
            'close' => $last,
            'last' => $last,
            'previousClose' => null,
            'change' => $this->safe_float($ticker, 'daily_change'),
            'percentage' => null,
            'average' => null,
            'baseVolume' => null,
            'quoteVolume' => $this->safe_float($ticker, 'total_btc_traded'),
            'info' => $ticker,
        );
    }

    public function parse_ohlcv ($ohlcv, $market = null, $timeframe = '1d', $since = null, $limit = null) {
        return [
            $this->parse8601 ($ohlcv['date'] . ' 00:00:00'),
            null,
            null,
            null,
            floatval ($ohlcv['price']),
            null,
        ];
    }

    public function fetch_ohlcv ($symbol, $timeframe = '1d', $since = null, $limit = null, $params = array ()) {
        $market = $this->market ($symbol);
        $response = $this->publicGetHistoricalPrices (array_merge (array (
            'currency' => $market['id'],
            'timeframe' => $this->timeframes[$timeframe],
        ), $params));
        $ohlcvs = $this->to_array($this->omit ($response['historical-prices'], 'request_currency'));
        return $this->parse_ohlcvs($ohlcvs, $market, $timeframe, $since, $limit);
    }

    public function parse_trade ($trade, $market) {
        $timestamp = intval ($trade['timestamp']) * 1000;
        return array (
            'id' => $trade['id'],
            'info' => $trade,
            'timestamp' => $timestamp,
            'datetime' => $this->iso8601 ($timestamp),
            'symbol' => $market['symbol'],
            'order' => null,
            'type' => null,
            'side' => $trade['maker_type'],
            'price' => $this->safe_float($trade, 'price'),
            'amount' => $this->safe_float($trade, 'amount'),
        );
    }

    public function fetch_trades ($symbol, $since = null, $limit = null, $params = array ()) {
        $market = $this->market ($symbol);
        $request = array (
            'currency' => $market['id'],
        );
        if ($limit !== null) {
            $request['limit'] = $limit;
        }
        $response = $this->publicGetTransactions (array_merge ($request, $params));
        $trades = $this->to_array($this->omit ($response['transactions'], 'request_currency'));
        return $this->parse_trades($trades, $market, $since, $limit);
    }

    public function create_order ($symbol, $type, $side, $amount, $price = null, $params = array ()) {
        $request = array (
            'side' => $side,
            'type' => $type,
            'currency' => $this->market_id($symbol),
            'amount' => $amount,
        );
        if ($type === 'limit') {
            $request['limit_price'] = $price;
        }
        $result = $this->privatePostOrdersNew (array_merge ($request, $params));
        return array (
            'info' => $result,
            'id' => $result,
        );
    }

    public function cancel_order ($id, $symbol = null, $params = array ()) {
        $request = array (
            'id' => $id,
        );
        return $this->privatePostOrdersCancel (array_merge ($request, $params));
    }

    public function withdraw ($code, $amount, $address, $tag = null, $params = array ()) {
        $this->check_address($address);
        $this->load_markets();
        $currency = $this->currency ($code);
        $request = array (
            'currency' => $currency['id'],
            'amount' => floatval ($amount),
            'address' => $address,
        );
        $response = $this->privatePostWithdrawalsNew (array_merge ($request, $params));
        return array (
            'info' => $response,
            'id' => $response['result']['uuid'],
        );
    }

    public function sign ($path, $api = 'public', $method = 'GET', $params = array (), $headers = null, $body = null) {
        if ($this->id === 'cryptocapital') {
            throw new ExchangeError($this->id . ' is an abstract base API for _1btcxe');
        }
        $url = $this->urls['api'] . '/' . $path;
        if ($api === 'public') {
            if ($params) {
                $url .= '?' . $this->urlencode ($params);
            }
        } else {
            $this->check_required_credentials();
            $query = array_merge (array (
                'api_key' => $this->apiKey,
                'nonce' => $this->nonce (),
            ), $params);
            $request = $this->json ($query);
            $query['signature'] = $this->hmac ($this->encode ($request), $this->encode ($this->secret));
            $body = $this->json ($query);
            $headers = array( 'Content-Type' => 'application/json' );
        }
        return array( 'url' => $url, 'method' => $method, 'body' => $body, 'headers' => $headers );
    }

    public function request ($path, $api = 'public', $method = 'GET', $params = array (), $headers = null, $body = null) {
        $response = $this->fetch2 ($path, $api, $method, $params, $headers, $body);
        if (gettype ($response) === 'string') {
            if (mb_strpos($response, 'Maintenance') !== false) {
                throw new ExchangeNotAvailable($this->id . ' on maintenance');
            }
        }
        if (is_array($response) && array_key_exists('errors', $response)) {
            $errors = array();
            for ($e = 0; $e < count ($response['errors']); $e++) {
                $error = $response['errors'][$e];
                $errors[] = $error['code'] . ' => ' . $error['message'];
            }
            $errors = implode(' ', $errors);
            throw new ExchangeError($this->id . ' ' . $errors);
        }
        return $response;
    }
}
