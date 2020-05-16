# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 21:38:14 2020

@author: Andrei
"""

"""
Your task is to use the iterative parsing to process the map file and
find out not only what tags are there, but also how many, to get the
feeling on how much of which data you can expect to have in the map.
Fill out the count_tags function. It should return a dictionary with the 
tag name as the key and number of times this tag can be encountered in 
the map as value.

"""


import xml.etree.cElementTree as ET
import pprint
from collections import defaultdict

osm_file = r'Chicago.xml'

def count_tags(filename):
        tags_dict = defaultdict(int)
        
        # Iterative Parsing
        for event, node in ET.iterparse(filename):
            tags_dict[node.tag] += 1
        return tags_dict
   

if __name__ == "__main__":
    tags = count_tags(osm_file)
    pprint.pprint(tags)



