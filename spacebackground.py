#!/usr/bin/env python
import json
import urllib2
import os
import os.path
import urllib
from optparse import OptionParser
from bs4 import BeautifulSoup

PARSER = OptionParser()
PARSER.add_option("-v", "--verbose", action="store_true",
                  help="explain what is being done")
PARSER.add_option("-f", "--failures", action="store_true",
                  help="log only failures")
(OPTIONS, ARGS) = PARSER.parse_args()

VALID_EXTS = ['.jpg', '.png', '.gif']

def download_images():
    reddit_dir = os.path.expanduser('~/.redditbackgrounds')

    if not os.path.exists(reddit_dir): 
        os.makedirs(reddit_dir)

    url = "http://www.reddit.com/r/spaceporn.json"
    try:
        request = urllib2.Request(url)
        request.add_header('User-Agent', 'a spaceporn scrapper')
        opener = urllib2.build_opener()
        contents = opener.open(request).read()

        listing = json.loads(contents)

        if 'error' in listing:
            errno = listing['error']
            v_log("Error: %s" % errno, failure=True)
            if errno == 429:
                v_log('Too many requests. Wait 30 sec and try again!',
                     failure=True)
                exit()

        picture_listings = listing['data']['children']
        for pic in picture_listings:
            data = pic['data']
            # prevent filename length errors by limiting title size
            title = data['title'][:124]
            # remove any illegal characters from the title string
            title = title.replace('/', '-')
            pic_url = data['url']
            ext = os.path.splitext(pic_url)[1]
            valid = ext and ext in VALID_EXTS

            if not valid:
                # try checking html for image
                pic_url = get_largest_image_from_html(pic_url)
                ext = os.path.splitext(pic_url)[1]
                valid = ext and ext in VALID_EXTS

            path = os.path.join(reddit_dir, title + ext)
            if not os.path.exists(path) and valid:
                v_log("Creating '%s' from %s" % (title + ext, pic_url))
                try:
                    opener = MyOpener()
                    urllib.urlretrieve(pic_url, path)
                except IOError as ex:
                    v_log("Unable to read %s" % pic_url, failure=True)
                    v_log("Reason: {0}".format(ex), failure=True)
            else:
                v_log("Ignoring %s" % pic_url, failure= not valid)
    except IOError as ex:
        v_log('IO Error: {0}'.format(ex), failure=True)

def v_log(string, failure=False):
    if OPTIONS.failures:
        if failure: 
            print(string)
    else:
        if OPTIONS.verbose: 
            print(string)

class MyOpener(urllib.FancyURLopener):
    version = 'space background scraper'

def get_largest_image_from_html(url):
    # assuming html
    imgs = []
    try:
        html = urllib.urlopen(url).read()
        soup = BeautifulSoup(html)
        # return the largest image
        tags = soup(images_with_width_and_height)
        imgs = [int(t.attrs['width']) * int(t.attrs['height']) for t in tags]
        if imgs:
            idx = imgs.index(max(imgs))
            return tags[idx]['src']
        else: return None
    except IOError as ex:
        v_log("Unable to read %s" % url, failure=True)
        v_log("Reason: {0}".format(ex), failure=True)

def images_with_width_and_height(tag):
    return tag.name == 'img' and \
           tag.has_key('width') and \
           tag.has_key('height') and \
           tag.has_key('src')
if __name__ == '__main__':
    download_images()

