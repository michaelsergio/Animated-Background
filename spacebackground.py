#!/usr/bin/env python

import json
import urllib2
import os
import os.path
import urllib
from urllib import FancyURLopener
from optparse import OptionParser
#from bs4 import BeautifulSoup

parser = OptionParser()
parser.add_option("-v", "--verbose", action="store_true",
                  help="explain what is being done")
parser.add_option("-f", "--failures", action="store_true",
                  help="log only failures")
(options, args) = parser.parse_args()

valid_exts = ['.jpg', '.png', '.gif']

def downloadImages():
    reddit_dir = os.path.expanduser('~/.redditbackgrounds')

    if not os.path.exists(reddit_dir): os.makedirs(reddit_dir)

    url = "http://www.reddit.com/r/spaceporn.json"
    try:
        request = urllib2.Request(url)
        request.add_header('User-Agent', 'a spaceporn scrapper')
        opener = urllib2.build_opener()
        contents = opener.open(request).read();

        listing = json.loads(contents)

        if 'error' in listing:
            errno = listing['error']
            vLog("Error: %s" % error, failure=True)
            if errno == 429:
                vLog('Too many requests. Wait 30 sec and try again!', failure=True)
                exit()

        picture_listings = listing['data']['children']
        for pic in picture_listings:
            data = pic['data']
            # prevent filename length errors by limiting title size
            title = data['title'][:124]
            pic_url = data['url']
            ext = os.path.splitext(pic_url)[1]
            valid = ext and ext in valid_exts

            path = os.path.join(reddit_dir, title + ext)
            if not os.path.exists(path) and valid:
                vLog("Creating '%s' from %s" % (title + ext, pic_url))
                try:
                    opener = MyOpener()
                    urllib.urlretrieve(pic_url, path)
                except IOError as e:
                    vLog("Unable to read %s" % pic_url, failure=True)
                    vLog("Reason: {0}".format(e), failure=True)
            else:
                vLog("Ignoring %s" % pic_url, failure= not valid)
    except IOError as e:
        vLog('IO Error: {0}'.format(e), failure=True)

def vLog(string, failure=False):
    if options.failures:
        if failure: print(string)
    else:
        if options.verbose: print(string)

class MyOpener(urllib.FancyURLopener):
    version = 'space background logger'

if __name__ == '__main__':
    downloadImages()

