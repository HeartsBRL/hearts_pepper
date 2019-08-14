import json
import urllib2, urllib, httplib
import sys

class api_querier():

    # URL Format: https://api.pp.mksmart.org/sciroc-competition/TeamName/Request
    base_url = "https://api.pp.mksmart.org/"
    url_dataset = "sciroc-competition/"
    url = ""

    schema_url = {
        "RobotStatus" : "sciroc-robot-status/",
        "RobotLocation" : "sciroc-robot-location/",
        "Shop" : "sciroc-episode4-shop/"
    }

    # INIT
    def __init__(self, teamName):

        # Generate the base_url
        self.url = self.base_url + self.url_dataset + teamName + "/"
        print "Base URL: " + self.url

    # GET request from the API server:
    # q = query of the server, i.e RobotStatus, RobotLocation, Shop.
    #   these are converted to the asociate url and will return the results
    def get(self, q):

        try:
            url = self.url + self.schema_url[q]
            print "GET URL: " + url
            j = json.load(urllib2.urlopen(url))
            print "dataset found, format as follows:"
            print j["@id"]
        except urllib2.HTTPError as err:
            if err.code == 404:
                print "404 - page not found"
            elif err.code == 500:
                print "500 - server error"
            elif err.code == 401:
                print "401 - auth error"
            else:
                print err.code + " - unknown error"
        except:
            print("Unexpected error:", sys.exc_info()[0])

    def put(self, q):

        print "put"

    # POST request to the server:
    # q = query of the server, i.e RobotStatus, RobotLocation, Shop.
    # data = JSON schama of data to pass to the server,
    #           these are checked against the server schema before sending
    def post(self, q, data):

        try:
            url = self.url + self.schema_url[q] + data["@id"]
            print "POST URL: " + url

            # generate headers for the server:
            headers = {"Content-type": "application/json",
                       "Accept": "*/*"}

            #
            data = urllib.urlencode(data)
            u = urllib2.urlopen(url, data)
            h.request('POST', q, data, headers)

            r = h.getresponse()
            print r.read()

        except urllib2.HTTPError as err:
            if err.code == 404:
                print "404 - page not found"
            elif err.code == 500:
                print "500 - server error"
            elif err.code == 401:
                print "401 - auth error"
            else:
                print err.code + " - unknown error"
        except:
            print("Unexpected error:", sys.exc_info()[0])

    # Check object against default schema
    # @TODO load schema and compare elements are the same (and type) as default
    def check_schema(self, schema):

        print "check schema"

    # Load a schema from the default, which loads as an object that can be used
    #   schema = must match schema file i.e RobotStatus, RobotLocation, Shop.
    def load_schema(self, schema):

        # load associated schema file from the schema directory:
        with open("schema/" + schema) as json_file:
            d = json.load(json_file)

        return d

qb = api_querier("master")

#qb.get("RobotStatus")

d = qb.load_schema("RobotLocation")

qb.post("RobotLocation", d)
