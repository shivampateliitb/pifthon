import logging
from fileinput import filename
from xml.etree import ElementTree as ET


def main():
    logging.basicConfig(filename='pifthon.log', level=logging.DEBUG)
    logging.info("Logging started")
    
    '''tree = ET.parse('inputs/input.xml')
    root = tree.getroot()
    
    print(root[0][1].__getitem__(0))'''
    
    logging.info("Logging completed")
    
if __name__ == '__main__':
    main()