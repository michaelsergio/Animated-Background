#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os.path
import sys
from xml.etree.cElementTree import Element, ElementTree, SubElement

def make_xml(files, delay=5):
    background = Element('background')

    starttime = SubElement(background, 'starttime')
    hour = SubElement(starttime, 'hour')
    minute = SubElement(starttime, 'minute')
    second = SubElement(starttime, 'second')
    hour.text = '00'
    minute.text = '00'
    second.text = '01'

    while files:
        img = files[0]

        static = SubElement(background, 'static')
        duration = SubElement(static, 'duration')
        filename = SubElement(static, 'file')
        duration.text = str(delay)
        filename.text = img
        
        files = files[1:]
        if files:
            peek = files[0]
            transition = SubElement(background, 'transition')
            transition_duration = SubElement(transition, 'duration')
            from_img = SubElement(transition, 'from')
            to_img = SubElement(transition, 'to')

            transition_duration.text = '5.0'
            from_img.text = img
            print peek
            to_img.text = peek


    doc = ElementTree(background)
    return doc

if __name__ == '__main__':
    test_files = [
    'Arctic Sea Ice Maximum By NASA Goddard Photo and Video [1280 x 720].jpg',
    'Aurora Over Raufarhöfn [798 x 1200].jpg',
    'Biri Island, Samar Philippines [950 x 632].jpg',
    'Dust Pillar of the Carina Nebula [1536x1218].jpg',
    'Eagle Nebula [1920x1080].jpg',
    'Expanding Bubble in Space [649 x 638].jpg',
    'Hubble telescope spots rare gravitational arc from distant, hefty galaxy cluster residing 10 billion light-years away; this .jpg',
    'In the Shadow of Saturn [2766x1364].jpg',
    'Light and Shadow in the Carina Nebula [978 x 631].jpg',
    "Milky Way over Piton de l'Eau, Reunion Island; the photographer waited for nearly two years for the sky and clouds to be jus.jpg",
    'Mountain biker in Moab, Utah with an amazing night-sky backdrop. [1600x1067] [x-post r-adrenalineporn].jpg',
    'NASA astronaut Robert L. Curbeam, Jr. (left) and European Space Agency astronaut Christer Fuglesang, both STS-116 mission sp.jpg',
    'Nebula 1920x1080.jpg',
    'NGC 3314 A &amp; B photographed by Hubble [3276x2928] .jpg',
    'Northern Lights over Crater Lake (via Brad ?Goldpaint) [960 x 540].jpg',
    'Northern Star Lights over Grand Tetons - GTNP [1600 x 1067] [OC].jpg',
    'Readying Orion for Flight: Orion will return home at a speed of 25,000 miles, almost 5,000 miles per hour faster than any hu.jpg',
    'Reflection Nebula in Orion [667 x 678].jpg',
    "Saturn's Jet Streams in False Color [924x877].jpg",
    'Simeis 188 in Stars, Dust and Gas [2200x1459].jpg',
    'Star Trail over Mono Lake, California [2048x1363] [OC].jpg',
    'Tarantula Nebula [3600 x 2880].jpg',
    'The East Coast by night from the International Space Station [3405x2266].png',
    'The Milky Way over Alderson, WV [4912x3264] [OC].jpg'
    ]

    SRC_DIR = '/home/sergio/.redditbackgrounds'
    image_files = [os.path.join(SRC_DIR, image_file) for image_file in test_files]

    make_xml(image_files).write(sys.stdout, encoding="utf-8")

