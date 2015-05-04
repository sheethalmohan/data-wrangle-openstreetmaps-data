from collections import defaultdict
import xml.etree.cElementTree as ET
import pprint
import re
import os
#Set the proper current working directory
os.getcwd()
os.chdir('C:/Users/sheethal/Desktop/DWMDB')


street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
expected = ["Street", "Avenue", "Boulevard", "Drive",
            "Court", "Place", "Square", "Lane", "Road",
            "Trail", "Parkway", "Commons", "Cirle",
            "Cove", "Highway", "Park", "Way", "South"]

# Updated mapping reflects changes needed in charlotte.osm file
mapping = { "E": "East",
            "W": "West",
            "N": "North",
            "S": "South",
            "Rd": "Road",
            "Rd.": "Road",
            "ln": "Lane",
            "ln.": "Lane",
            "Ln": "Lane",
            "Ln.": "Lane",
            "Dr": "Drive",
            "Dr.": "Drive",
            "St": "Street",
            "St.": "Street",
            "Ste": "Suite",
            "Ste.": "Suite",
            "Cir": "Circle",
            "Ave": "Avenue",
            "Ave.": "Avenue",
            "Hwy": "Highway",
            "Hwy.": "Highway",
            "Pky": "Parkway",
            "Pky.": "Parkway",
            "Fwy": "Freeway",
            "Fwy.": "Freeway",
            "Blvd": "Boulevard",
            "Blvd.": "Boulevard"
            }


def audit_street_type(street_types, street_name):
    """
    Adds potentially problematic street names to
    list 'street_types'
    """
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    """
    Returns a list of problematic street type values
    for use with the update() name mapping.
    """
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    parser = ET.iterparse(osm_file, events=("start",))
    for event, elem in parser:
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
        # Safe to clear() now that descendants have been accessed
        elem.clear()
    del parser
    return street_types


def update(name, mapping):
    """
    Implemented in data.py
    Updates ALL substrings in string 'name' to
    their values in dictionary 'mapping'
    """
    words = name.split()
    for w in range(len(words)):
        if words[w] in mapping:
            if words[w-1].lower() not in ['suite', 'ste.', 'ste']: # For example, don't update 'Suite E' to 'Suite East'
                words[w] = mapping[words[w]]
    name = " ".join(words)
    return name

# EXPERIMENTAL UNUSED METHOD
# Opted not to use in data.py over the more generalized
# and more optimal 'update()' method above
def update_name(name, mapping):
    """
    If the last substring of string 'name' is an int,
    updates all substrings in 'name', else updates
    only the last substring.
    """
    m = street_type_re.search(name)
    m = m.group()
    # Fix all substrings in an address ending with a number.
    # Example: 'S Tryon St Ste 105' to 'South Tryon Street Suite 105'
    try:
        __ = int(m)
        words = name.split()[:-1]
        for w in range(len(words)):
            if words[w] in mapping:
                words[w] = mapping[words[w]]
        words.append(m)
        address = " ".join(words)
        return address
    # Otherwise, fix only the last substring in the address
    # Example: 'This St.' to 'This Street'
    except ValueError:        
        i = name.index(m)
        if m in mapping:
            name = name[:i] + mapping[m]
    return name


def main_test():
    st_types = audit("raleigh_north-carolina.osm")
    
    pprint.pprint(dict(st_types))
    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update(name, mapping)
            print name, "=>", better_name
            if name == "West Stanly St.":
                assert better_name == "West Stanly Street"
            if name == "S Tryon St Ste 105":
                assert better_name == "South Tryon Street Suite 105"

if __name__ == '__main__':
    main_test()

# Result:
'''
{'100': set(['100']),
 '1000': set(['Six Forks Road #1000']),
 '17': set(['US Highway 17']),
 '501': set(['US 15;US 501']),
 '54': set(['Highway 54',
            'State Highway 54',
            'West Highway 54',
            'West NC Highway 54']),
 '55': set(['Highway 55', 'NC Highway 55', 'US 55']),
 '70': set(['US 70']),
 '751': set(['NC Highway 751']),
 'Ave': set(['E. Winmore Ave',
             'East Winmore Ave',
             'Fernway Ave',
             'Glenwood Ave',
             'Mountford Ave',
             'S Boylan Ave',
             'S. Boylan Ave']),
 'Blvd': set(['Capital Blvd',
              'Martin Luther King Jr Blvd',
              'Martin Luther King Jr. Blvd',
              'Martin Luther King Junior Blvd',
              'Southpoint Autopark Blvd',
              'Witherspoon Blvd']),
 'Blvd.': set(['Durham-Chapel Hill Blvd.',
               'N Fordham Blvd.',
               'Southpoint Auto Park Blvd.']),
 'Bypass': set(['US 15 501 Bypass']),
 'CIrcle': set(['Meadowmont Village CIrcle']),
 'Cir': set(['Braddock Cir', 'Daybrook Cir']),
 'Circle': set(['Alliance Circle',
                'Arrow Leaf Circle',
                'Barriedale Circle',
                'Davis Circle',
                'Davis Grove Circle',
                'Duck Pond Circle',
                'Euphoria Circle',
                'Golden Horseshoe Circle',
                'Hayloft Circle',
                'Kintyre Circle',
                'Lake Hollow Circle',
                'Langley Circle',
                'Meadowmont Village Circle',
                'Meadowvale Circle',
                'Medallion Circle',
                'Mount Rogers Circle',
                'Northwood Circle',
                'Page Point Circle',
                'Parkbrook Circle',
                'Parkleaf Circle',
                'Parkmist Circle',
                'Parkmount Circle',
                'Parkvine Circle',
                'Phaeton Circle',
                'Pine Top Circle',
                'Piper Stream Circle',
                'Quarrystone Circle',
                'Ravens Point Circle',
                'Redbud Circle',
                'Ricky Circle',
                'Rockland Circle',
                'Shady Meadow Circle',
                'Talton Circle']),
 'Crescent': set(['West Acres Crescent']),
 'Crossing': set(['Oldham Forest Crossing']),
 'Ct': set(['Ashley Springs Ct', 'Bevel Ct', 'Gulf Ct']),
 'Dr': set(['Calabria Dr',
            'Crab Orchard Dr',
            'Gold Star Dr',
            'Sablewood Dr',
            'Stinson Dr',
            'Triangle Plantation Dr',
            'University Dr',
            'Waterford Lake Dr']),
 'East': set(['US Highway 70 East']),
 'Ext': set(['New Hope Commons Boulevard Ext']),
 'Extension': set(['Weaver Dairy Road Extension']),
 'Fork': set(['Dry Fork']),
 'Grove': set(['Newton Grove']),
 'Hill': set(['Chapel Hill']),
 'Hills': set(['The Circle at North Hills']),
 'LaurelcherryStreet': set(['LaurelcherryStreet']),
 'Ln': set(['Sunbow Falls Ln']),
 'Loop': set(['Amiable Loop', 'Farrow Glen Loop']),
 'PI': set(['Alexander Promenade PI']),
 'Pkwy': set(['Skyland Ridge Pkwy']),
 'Pky': set(['Brier Creek Pky', 'brier Creek Pky']),
 'Pl': set(['Balaji Pl']),
 'Plaza': set(['City Hall Plaza', 'Exchange Plaza', 'Park Forty Plaza']),
 'Point': set(['Rocky Point']),
 'Practice': set(['Triangle Family Practice']),
 'Rd': set(['Buck Jones Rd', 'Creedmoor Rd', 'N Roxboro Rd', 'Six Forks Rd']),
 'Rd.': set(['Bayleaf Church Rd.']),
 'Run': set(['Deep Gap Run', 'Morgans Corner Run']),
 'ST': set(['W EDENTON ST']),
 'St': set(['9th St',
            'Hillsborough St',
            'Holloway St',
            'Kinsey St',
            'Main at North Hills St',
            'Tucker St',
            'W Franklin St']),
 'St,': set(['Morris St,']),
 'St.': set(['E Rosemary St.',
             'East Corcoran St.',
             'East Franklin St.',
             'W Rosemary St.',
             'W. Franklin St.',
             'W. Pettigrew St.',
             'West Rosemary St.']),
 'Suite': set(['N Duke St Suite']),
 'West': set(['Highway 54 West',
              'Highway 55 West',
              'Highway West',
              'NC Highway 55 West'])}
The Circle at North Hills => The Circle at North Hills
Morris St, => Morris St,
NC Highway 55 West => NC Highway 55 West
Highway 54 West => Highway 54 West
Highway West => Highway West
Highway 55 West => Highway 55 West
E Rosemary St. => East Rosemary Street
East Franklin St. => East Franklin Street
W. Franklin St. => W. Franklin Street
West Rosemary St. => West Rosemary Street
East Corcoran St. => East Corcoran Street
W Rosemary St. => West Rosemary Street
W. Pettigrew St. => W. Pettigrew Street
Creedmoor Rd => Creedmoor Road
Buck Jones Rd => Buck Jones Road
N Roxboro Rd => North Roxboro Road
Six Forks Rd => Six Forks Road
Chapel Hill => Chapel Hill
US 15 501 Bypass => US 15 501 Bypass
N Duke St Suite => N Duke Street Suite
Shady Meadow Circle => Shady Meadow Circle
Alliance Circle => Alliance Circle
Northwood Circle => Northwood Circle
Parkleaf Circle => Parkleaf Circle
Quarrystone Circle => Quarrystone Circle
Phaeton Circle => Phaeton Circle
Euphoria Circle => Euphoria Circle
Page Point Circle => Page Point Circle
Medallion Circle => Medallion Circle
Hayloft Circle => Hayloft Circle
Mount Rogers Circle => Mount Rogers Circle
Ricky Circle => Ricky Circle
Piper Stream Circle => Piper Stream Circle
Redbud Circle => Redbud Circle
Duck Pond Circle => Duck Pond Circle
Barriedale Circle => Barriedale Circle
Talton Circle => Talton Circle
Parkvine Circle => Parkvine Circle
Arrow Leaf Circle => Arrow Leaf Circle
Meadowvale Circle => Meadowvale Circle
Lake Hollow Circle => Lake Hollow Circle
Meadowmont Village Circle => Meadowmont Village Circle
Langley Circle => Langley Circle
Davis Grove Circle => Davis Grove Circle
Ravens Point Circle => Ravens Point Circle
Rockland Circle => Rockland Circle
Parkmount Circle => Parkmount Circle
Parkmist Circle => Parkmist Circle
Golden Horseshoe Circle => Golden Horseshoe Circle
Parkbrook Circle => Parkbrook Circle
Pine Top Circle => Pine Top Circle
Kintyre Circle => Kintyre Circle
Davis Circle => Davis Circle
US Highway 70 East => US Highway 70 East
Balaji Pl => Balaji Pl
Dry Fork => Dry Fork
Bayleaf Church Rd. => Bayleaf Church Road
Deep Gap Run => Deep Gap Run
Morgans Corner Run => Morgans Corner Run
Triangle Family Practice => Triangle Family Practice
Sunbow Falls Ln => Sunbow Falls Lane
Alexander Promenade PI => Alexander Promenade PI
Crab Orchard Dr => Crab Orchard Drive
Gold Star Dr => Gold Star Drive
Calabria Dr => Calabria Drive
Stinson Dr => Stinson Drive
University Dr => University Drive
Waterford Lake Dr => Waterford Lake Drive
Triangle Plantation Dr => Triangle Plantation Drive
Sablewood Dr => Sablewood Drive
US 15;US 501 => US 15;US 501
NC Highway 751 => NC Highway 751
Weaver Dairy Road Extension => Weaver Dairy Road Extension
LaurelcherryStreet => LaurelcherryStreet
Newton Grove => Newton Grove
Exchange Plaza => Exchange Plaza
Park Forty Plaza => Park Forty Plaza
City Hall Plaza => City Hall Plaza
Tucker St => Tucker Street
Main at North Hills St => Main at North Hills Street
Holloway St => Holloway Street
Hillsborough St => Hillsborough Street
9th St => 9th Street
W Franklin St => West Franklin Street
Kinsey St => Kinsey Street
Braddock Cir => Braddock Circle
Daybrook Cir => Daybrook Circle
New Hope Commons Boulevard Ext => New Hope Commons Boulevard Ext
US 70 => US 70
Oldham Forest Crossing => Oldham Forest Crossing
100 => 100
Skyland Ridge Pkwy => Skyland Ridge Pkwy
Farrow Glen Loop => Farrow Glen Loop
Amiable Loop => Amiable Loop
N Fordham Blvd. => North Fordham Boulevard
Southpoint Auto Park Blvd. => Southpoint Auto Park Boulevard
Durham-Chapel Hill Blvd. => Durham-Chapel Hill Boulevard
US Highway 17 => US Highway 17
Rocky Point => Rocky Point
US 55 => US 55
Highway 55 => Highway 55
NC Highway 55 => NC Highway 55
West Highway 54 => West Highway 54
Highway 54 => Highway 54
West NC Highway 54 => West NC Highway 54
State Highway 54 => State Highway 54
Brier Creek Pky => Brier Creek Parkway
brier Creek Pky => brier Creek Parkway
W EDENTON ST => West EDENTON ST
West Acres Crescent => West Acres Crescent
Capital Blvd => Capital Boulevard
Southpoint Autopark Blvd => Southpoint Autopark Boulevard
Martin Luther King Junior Blvd => Martin Luther King Junior Boulevard
Witherspoon Blvd => Witherspoon Boulevard
Martin Luther King Jr. Blvd => Martin Luther King Jr. Boulevard
Martin Luther King Jr Blvd => Martin Luther King Jr Boulevard
S Boylan Ave => South Boylan Avenue
Fernway Ave => Fernway Avenue
Glenwood Ave => Glenwood Avenue
East Winmore Ave => East Winmore Avenue
E. Winmore Ave => E. Winmore Avenue
Mountford Ave => Mountford Avenue
S. Boylan Ave => S. Boylan Avenue
Meadowmont Village CIrcle => Meadowmont Village CIrcle
Gulf Ct => Gulf Ct
Ashley Springs Ct => Ashley Springs Ct
Bevel Ct => Bevel Ct
Six Forks Road #1000 => Six Forks Road #1000
'''
    
