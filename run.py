#!/usr/bin/env python

import os

from app import app

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    if app.config.get('FACEBOOK_CONSUMER_KEY') and \
       app.config.get('FACEBOOK_CONSUMER_SECRET'):
        app.run(host='0.0.0.0', port=port)
    else:
        print 'Cannot start application without Facebook App Id and Secret set'
