#!/usr/bin/env python

# This script is able to read the MK Smart datahub to query data.
    # working:
    #     - post and get for all episode4 api's
    #     -
    # todo:
    #     - ROSify
    #         - expose to some useful ROS server/topic?
    #     - put (what even are you?)
    #     - authentication & testing with real data


import json
import urllib2, urllib, httplib, base64
import sys
import datetime
import os, ssl

class ApiQuerier():

    # URL Format: https://api.pp.mksmart.org/sciroc-competition/TeamName/Request
    base_url = "https://api.mksmart.org/"
    url_dataset = "sciroc-competition/"
    url = ""
    teamid = "hearts"
    teamkey = "65222466-231c-4efa-bbe3-5cb7e862cfc7"

    # SCHEMA URL NEEDS TO BE EXPANDED AS NEEDED:
    ## Completed for episode4
    schema_url = {
        "RobotStatus" : "sciroc-robot-status/",
        "RobotLocation" : "sciroc-robot-location/",
        "Shop" : "master/sciroc-episode4-shop/",
        "Table": "sciroc-episode3-table/"
    }

    # INIT
    def __init__(self):

        # Generate the base_url
        self.url = self.base_url + self.url_dataset
        print "Base URL: " + self.url

    # GET request from the API server:
    # q = query of the server, i.e RobotStatus, RobotLocation, Shop.
    #   these are converted to the asociate url and will return the results
        # example use (returns the status of "RobotStatus"):
        #     qb.get("RobotStatus")
    def get(self, q):

        try:
            # Check if the URL already has an ID (i.e some start with master)
            if( self.schema_url[q][:6] == "master" ):
                url = self.url + self.schema_url[q]
            else:
                url = self.url + self.teamid + "/" + self.schema_url[q]

            # Print URL:
            print "GET URL: " + url

            # Fetch URL json data from server:
            ## This solved the problem for ROS Kinetic
            #http://blog.pengyifan.com/how-to-fix-python-ssl-certificate_verify_failed/
            if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
                getattr(ssl, '_create_unverified_context', None)):
                ssl._create_default_https_context = ssl._create_unverified_context

            request = urllib2.Request(url)
            base64string = base64.b64encode('%s:%s' % (self.teamkey, ''))
            request.add_header("Authorization", "Basic %s" % base64string)

            try:
                result = urllib2.urlopen(request)
            except urllib2.URLError as e:
                    print e.reason
            j = json.load(result)
            # Print it out:
            # print "dataset found, format as follows:"
            # print j
            return j

        # Check for URL failures:
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
        # example use (loads default schema and posts for RobotLocation):
        #     d = qb.load_schema("RobotLocation")
        #     qb.post("RobotLocation", d)

    def post(self, q, data):

        try:
            # Check if the URL already has an ID (i.e some start with master)
            if( self.schema_url[q][:6] == "master" ):
                url = self.url + self.schema_url[q]
            else:
                url = self.url + self.teamid + "/" + self.schema_url[q]

            #url = self.url + self.schema_url[q] + data["@id"]
            url = url + data["@id"] + "?"
            print "POST URL: " + url

            print data
            # Encode payload:
            encoded_data = urllib.urlencode(data)
            print encoded_data

            # Fetch URL json data from server:
            request = urllib2.Request(url)

            # Add Authorization and headers:
            base64string = base64.b64encode('%s:%s' % (self.teamkey, ''))
            request.add_header("Authorization", "Basic %s" % base64string)
            request.add_header("Content-type", "application/json")
            request.add_header("Accept", "*/*")

            # Open URL
            result = urllib2.urlopen(request, json.dumps(data))

            # Get JSON:
            #j = json.load(result)

            print result

            #r = h.getresponse()
            #print r.read()

        except urllib2.HTTPError as err:
            if err.code == 404:
                print "404 - page not found"
            elif err.code == 500:
                print "500 - server error"
            elif err.code == 401:
                print "401 - auth error"
            else:
                print str(err.code) + " - unknown error"
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


if __name__ == '__main__':
    ### EXAMPLE USE OF MODULE:

    ## Set up the object:
    qb = ApiQuerier()

    ## Get an item from the server:
    print "Getting Shop:"
    ret = qb.get("Shop")
    print ret

    ## Send object to server:
    print "Sending Robot Status rqst"
    # load the data schema for the item:
    d = qb.load_schema("RobotStatus")
    # edit as needed:
    d["@id"] = u"hearts"
    d["message"] = u"enroute"
    d["episode"] = u"4"
    d["team"] = "hearts"
    #shitty way of making the correct format for timestamp:
    t = str(datetime.datetime.now()).replace(" ", "T")
    t = t[:len(t)-3]+"Z"
    d["timestamp"] = t
    d["x"] = 4
    d["y"] = 2
    d["z"] = 0
    # send:
    qb.post("RobotStatus", d)
