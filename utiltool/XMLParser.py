import sys
try: 
    import xml.etree.cElementTree as ET 
except ImportError: 
    import xml.etree.ElementTree as ET 


    #Parse XML file
    root = ET.parse('XMLParser.xml')
    operator = root.findall('Operator')
    for operator_list in operator:
    	print '*'*20
    	if operator_list.attrib.has_key('Type'):
    		print "Type:" + operator_list.attrib['Type']
    	for param in operator_list:
    		print param.tag + ':' +param.text
    print '='*20






