import urllib2
import os
import os.path
import urllib
from urllib import FancyURLopener
from optparse import OptionParser
from bs4 import BeautifulSoup

reddit_dir = os.path.expanduser('./test/')

edgecases = [
"http://www.flickr.com/photos/ironrodart/7460869724/lightbox/",
"http://www.flickr.com/photos/zolashine/7459750484/in/photostream/lightbox/",
"http://www.flickr.com/photos/gsfc/6150743502/lightbox/",
"http://www.nasa.gov/mission_pages/aim/multimedia/ISS031-E-116058.html"
]

class MyOpener(urllib.FancyURLopener):
    version = 'space background logger'

def download(pic_url, title):
    try:
        ext = os.path.splitext(pic_url)[1]
        path = os.path.join(reddit_dir, title + ext)
        
        if not ext:
            pic_url = getLargestImageFromPage(pic_url)
            ext = os.path.splitext(pic_url)[1]
            path = os.path.join(reddit_dir, title + ext)

        try:
            opener = MyOpener()
            urllib.urlretrieve(pic_url, path)
        except IOError as e:
            print("Unable to read %s" % pic_url)
            print("Reason: {0}".format(e))
    except IOError as e:
        print('IO Error: {0}'.format(e))

def getLargestImageFromPage(url):
    imgs = []
    # assuming html
    try:
        opener = MyOpener()
        html = urllib.urlopen(url).read()
        soup = BeautifulSoup(html)
        # return the largest image
        tags = soup(images_with_width_and_height)
        imgs = [int(t.attrs['width']) * int(t.attrs['height']) for t in tags]
        if imgs:
            idx = imgs.index(max(imgs))
            return tags[idx]['src']
        else: return None
    except IOError as e:
        print("Unable to read %s" % pic_url)
        print("Reason: {0}".format(e))

def images_with_width_and_height(tag):
    return tag.name == 'img' and \
           tag.has_key('width') and \
           tag.has_key('height') and \
           tag.has_key('src')

i = 0
for url in edgecases:
    download(url, str(i))
    i += 1
