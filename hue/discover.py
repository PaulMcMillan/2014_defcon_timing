"""Basic code to find a hue device. Finds one, and only one, and will
probably get confused if there are other similar devices available via
SSDP on your network.


"""

import ssdp
import requests
import xml.etree.ElementTree as ET

XMLNS = {'hue': 'urn:schemas-upnp-org:device-1-0'}


def find_hues():
    hue_ssdp_list = ssdp.discover('urn:schemas-upnp-org:device:basic:1',
                                  timeout=1, max_wait=1)
    for hue_ssdp in hue_ssdp_list:
        description_xml = requests.get(hue_ssdp.location)
        root = ET.XML(description_xml.text)
        base_url = root.find('hue:URLBase', namespaces=XMLNS).text
        yield base_url


def find_hue():
    return find_hues().next()


if __name__ == '__main__':
    for hue_url in find_hues():
        print hue_url
