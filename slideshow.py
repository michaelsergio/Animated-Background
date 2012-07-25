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

