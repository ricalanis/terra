from pyproj import Proj, transform
import unicodedata
import string
import random

def convert_coordinates(x,y):
    inProj = Proj(init='epsg:3857')
    outProj = Proj(init='epsg:4326')
    x2,y2 = transform(inProj,outProj,x,y)
    return(x2,y2)

def extract_point(response_json):
    for alias in response_json['data']['value'][0]["fields"]["fields"]:
        if 'POINT' in alias["value"]:
            point_text = alias["value"]
    point_text = point_text.replace("POINT(","")
    point_text = point_text.replace(")","")
    x, y = point_text.split(" ")
    return float(x), float(y)

def normalize_data(s):
    s = s.lower()
    return ''.join(c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn')

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
