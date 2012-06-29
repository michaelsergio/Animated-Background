#!/usr/bin/env python
import json
import urllib2
import os
import os.path
import urllib
from urlparse import urlparse, urljoin
from optparse import OptionParser
from bs4 import BeautifulSoup
from makeslideshow import make_xml

VALID_EXTS = ['.jpg', '.png', '.gif']
USER_AGENT = 'A /r/spaceporn scrapper (mikeserg@gmail.com)'
REDDIT_DIR = os.path.expanduser('~/.redditbackgrounds')

def download_images():
    images = []

    if not os.path.exists(REDDIT_DIR): 
        os.makedirs(REDDIT_DIR)

    url = "http://www.reddit.com/r/spaceporn.json"
    try:
        #request = urllib2.Request(url)
        #request.add_header('User-Agent', USER_AGENT)
        #opener = urllib2.build_opener()
        #contents = opener.open(request).read()
        contents = urllib.urlopen(url).read()

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

            path = os.path.join(REDDIT_DIR, title + ext)
            if not os.path.exists(path) and valid:
                v_log("Creating '%s' from %s" % (title + ext, pic_url))
                try:
                    urllib.urlretrieve(pic_url, path)
                    images.append(path)
                except IOError as ex:
                    v_log("Unable to read %s" % pic_url, failure=True)
                    v_log("Reason: {0}".format(ex), failure=True)
            else:
                v_log("Ignoring %s" % pic_url, failure= not valid)
                if valid:
                    images.append(path)
    except IOError as ex:
        v_log('IO Error: {0}'.format(ex), failure=True)
    return images

def v_log(string, failure=False):
    if OPTIONS.failures:
        if failure: 
            print(string)
    else:
        if OPTIONS.verbose: 
            print(string)

class MyOpener(urllib.FancyURLopener):
    version = USER_AGENT

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
            src = tags[idx]['src']
            # if image comes back like /hello/world
            # add net_loc: http://example.com/hello/world
            src_parse = urlparse(src)
            if src_parse.netloc == '':
                org_parse = urlparse(url)
                img_url = urljoin(url, src_parse.netloc)
            else:
                img_url = src

            return img_url
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
    # Check for command line flags
    PARSER = OptionParser()
    PARSER.add_option("-v", "--verbose", action="store_true",
                      help="explain what is being done")
    PARSER.add_option("-f", "--failures", action="store_true",
                      help="log only failures")
    PARSER.add_option("-d", "--delay", default="60",
                      help="sets the delay inbetween the slideshow (in seconds)")
    (OPTIONS, ARGS) = PARSER.parse_args()

    # Set my user agent to get paste urllib bans
    OPENER = MyOpener()
    urllib._urlopener = OPENER
    urllib2._urlopener = OPENER

    # in seconds


    # retrieve all images
    all_images = download_images()

    xml_name = "slideshow.xml"
    xml_path = os.path.join(REDDIT_DIR, xml_name)
    xml_file = open(xml_path, 'w')
    make_xml(all_images, int(OPTIONS.delay)).write(xml_file)

    os.system('gsettings set org.gnome.desktop.background picture-uri file://%s'
               % xml_path)
