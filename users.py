# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 22:29:40 2020

@author: Andrei
"""


"""
Your task is to explore the data a bit more.
The first task is a fun one - find out how many unique users
have contributed to the map in this particular area!

The function process_map should return a set of unique user IDs ("uid")
"""

import xml.etree.cElementTree as ET
import pprint
from collections import defaultdict

osm_file = r'Chicago.xml'

def get_user(element):
    if element.tag in ["node", "way", "relation"]:
        return element.attrib["uid"]
   


def unique_user_count(filename):
    users = defaultdict(int)
    for event, element in ET.iterparse(filename):
        uid = get_user(element)
        if(uid):
            users[uid] += 1
    return users

def process_map(osm_file):
    users = set()
    for event, element in ET.iterparse(osm_file):
        if 'uid' in element.attrib:
            users.add(element.get('uid'))

    return users


if __name__ == "__main__":
    process_map(osm_file)
    pprint.pprint(process_map(osm_file))