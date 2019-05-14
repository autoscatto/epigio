import xmltv
import pandas as pd
from dateutil import parser
import datetime

from pprint import pprint

# If you need to change the locale:
# xmltv.locale = 'Latin-1'

# If you need to change the date format used in the XMLTV file:
# xmltv.date_format = '%Y%m%d%H%M%S %Z'
#https://www.bloggoiptv.com/fonti-per-le-guide-epg/

#http://www.epg-guide.com/it.gz
filename = '../it.xml'


def programme_to_pdrow(x):
    x.pop('desc', None)
    if not isinstance(x['stop'], datetime.datetime):
        x['stop'] = parser.parse(x['stop'])
    if not isinstance(x['start'], datetime.datetime):
        x['start'] = parser.parse(x['start'])
    x['duration'] = x['stop'] - x['start']
    x['category'] = "|".join([z[0] for z in x.get('category', [])])
    x['title'] = "|".join([z[0] for z in x.get('title', [])])

    return x


with open(filename, 'r') as f:
    data = xmltv.read_programmes(f)

p = pd.DataFrame([programme_to_pdrow(j) for j in data])
gg=p.groupby('title')[['title']].count()
vv=gg.title.sort_values(ascending=False)
