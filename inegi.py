import requests
import tools

URL_INEGI= "http://gaia.inegi.org.mx/NLB/tunnel/TableAliasV60/busqueda"


def bulk_coords_convert(array):
    output = []
    for line in array:
        try:
            response = crossing(line["calle_1"],
			  line["calle_2"], line["municipio"])
            current_coords = {"longitud":response["match"]["long"],
			  "latitud":response["match"]["lat"]}
            output.append(dict(line, **current_coords))
        except:
            current_coords ={"longitud":"NA","latitud":"NA"}
            output.append(dict(line, **current_coords))
    return output

def crossing(street1, street2, city):
    query = street1 + ", " + city + " --" + " " + street2
    response = call_inegi(query)
    output = get_inegi_intersection(response)
    return output

def call_inegi(query):
    query = tools.normalize_data(query)
    request_headers={"Content-Type":"application/json"}
    request_body = '{"idUser":"", "pagina":1, "paramProy":"",
	  "proyName":"mdm6", "searchCriteria":"'+ query +'",
	  "tabla":"geolocator", "where":""}'

	r = requests.get(URL_INEGI, headers=request_headers, data = request_body )
    output = r.json()
    return output

def get_inegi_intersection(response):
    try:
        x1, y1 = tools.extract_point(response)
        x2, y2 =  tools.convert_coordinates(x1,y1)
        response["match"] = {}
        response["match"]["long"] = x2
        response["match"]["lat"] = y2
    except:
        response["match"] = {}
        response["match"]["long"] = "NA"
        response["match"]["lat"] = "NA"
    return response
