'use strict';

// ---------------------------------------------------------------------------

const acx = require ('./acx.js');

// ---------------------------------------------------------------------------

module.exports = class wadax extends acx {
    describe () {
        return this.deepExtend (super.describe (), {
            'id': 'wadax',
            'name': 'Wadax',
            'countries': [ 'EU' ],
            'has': {
                'CORS': false,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/45444675-c9ce6680-b6d0-11e8-95ab-3e749a940de1.jpg',
                'extension': '.json',
                'api': 'https://wadax.io/v2',
                'www': 'https://wadax.io',
                'doc': 'https://wadax.io/doc/api',
            },
        });
    }
};
