# -*- coding: utf-8 -*-
"""
Created on Fri May 15 18:36:18 2020

@author: Andrei
"""


import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

osm_file = r'Chicago.xml'

problemchars = re.compile(r'\,|\.\b')
street_type_re = re.compile(r'\b[a-zA-Z]+\.?$', re.IGNORECASE)
postcode_type_re = re.compile(r'([6]){1}')
street_types = defaultdict(set)

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", "Route"
            "Trail", "Parkway", "Commons" ,"Way", "Circle", "Highway", "Park", "Terrace", "Trail", "Lane" ]

mapping = { "Ave": "Avenue",
            "Blvd": "Boulevard",
            "Dr" : "Drive",
            "Hwy" : "Highway",
            "Rd" : "Road",
            "Rd." : "Road",
            "E." : "East",
            "E" : "East",
            "W." : "West",
            "W" : "West",
            "N" : "North",
            "S" : "South",
            "St" : "Street",
            "St." : "Street",
            "Streets" : "Street",
            "Bouevard" : "Boulevard"
            }

expected_zip = ["60601", "60602", "60603", "60604", "60605", "60606", "60607", "60608", "60609", "60610", "60611", "60612", "60613", "60614", "60615", "60616", "60618", "60621", "60622", "60623", "60624", "60629", "60632", "60634", "60636", "60637", "60642", "60647", "60653", "60654", "60657", "60661", "60696", "60202", "60651", "60651", "60626"]

zip_mapping = {
               "606476" : "60647",
               "60067" : "60607",
               "606476" : "60647",
               "60067" : "60607",
               "60064" : "60614"
               
            }

def audit_street_type(prob_streets, street_types, street_name):

	if problemchars.search(street_name):
		prob_streets[problemchars.search(street_name).group()].add(street_name)

	else:
		m = street_type_re.search(street_name)
		if m:
			street_type = m.group()
			if street_type not in expected:
				street_types[street_type].add(street_name)
                
def audit_postal_code(postal_code_types, postal_code):  
    if postal_code not in expected_zip:
        postal_code_types[postal_code].add(postal_code)
    return postal_code_types               

def is_street_name(elem):
	return (elem.attrib['k'] == "addr:street")

def is_postal_code(elem):
    return (elem.attrib['k'] == "addr:postcode")

def audit(osm_file):
    
    street_types = defaultdict(set)
    prob_streets = defaultdict(set)
    postal_code_types = defaultdict(set)
    
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag =="way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                   audit_street_type(prob_streets, street_types, tag.attrib['v'])
                if is_postal_code(tag):
                    audit_postal_code(postal_code_types, tag.attrib['v'])
                    

    return street_types, dict(postal_code_types)

def update_name(name, mapping):

	
		if name in mapping:
			name = mapping[name]
		else:
		    name = name.split(' ')

		    for i in range(len(name)):
		        if name[i] in mapping:
		        	name[i] = mapping[name[i]]
		    else:
		    	name = ' '.join(name)

		return name
    
def update_postal_code(postal_code, zip_mapping):
    
    if postal_code in zip_mapping:
        postal_code = zip_mapping[postal_code]
    if len(postal_code) != 5:
                postal_code = postal_code[0:5]
    return postal_code    
     
if __name__ == '__main__':
    
    street_types = audit(osm_file)[0]
        
    pprint.pprint(dict(street_types))
    
    for street_type, ways in street_types.items():
       for name in ways:
        better_name = update_name(name, mapping)
        print (name, "=>", better_name  )

    postal_code_types = audit(osm_file)[1]
    pprint.pprint(dict(postal_code_types))
    
    for postal_code_types, ways in postal_code_types.items():
        for postcode in ways:
            better_postcode = update_postal_code(postcode, zip_mapping)
            print (postcode, "=>", better_postcode)
       