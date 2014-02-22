'''
Created on Jan 10, 2014

@author: Horacio G. de Oro
'''

import httplib
import json
import sys


def main():
    if len(sys.argv) == 1:
        conn = httplib.HTTPConnection("127.0.0.1:8000")
        conn.request("GET", "/angular/get_arduino_data/")
        r1 = conn.getresponse()
        r1.status, r1.reason
        raw_data = r1.read()
        data = json.loads(raw_data)
        #    import pprint
        #    pprint.pprint(data)
        arduino_data = data['enhanced_arduino_type']
        # print " * A0: {}".format(arduino_data['analog_pins_struct'][0]['status']['read_value'])
        pin_read = arduino_data['analog_pins_struct'][0]['status']['read_value']
        value = ((5.0 * pin_read * 100.0) / 1024.0)
        print "temp.value %.2f" % value
    else:
        if sys.argv[1] == "config":
            print "graph_title Temperature"
            print "graph_args --vertical-label Temperature"
            print "graph_category arduino"
            print "temp.label Temperature"
            print "temp.type GAUGE"


if __name__ == '__main__':
    main()
