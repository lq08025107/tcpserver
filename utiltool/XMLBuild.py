import xml.dom

def create_element(doc,tag,attr):
    
    elementNode=doc.createElement(tag)
    
    textNode=doc.createTextNode(attr)
    
    elementNode.appendChild(textNode)
    return elementNode

dom1=xml.dom.getDOMImplementation()
doc=dom1.createDocument(None,"WarningsData",None)
top_element = doc.documentElement
WarningDatas=[{'DynamicInfo': 'null', 'AlarmTime': u'12:00:00', 'number': u'001', 'id': u'001', 'name': u'python check'}, 
              {'DynamicInfo': 'null', 'AlarmTime': u'12:00:00', 'number': u'002', 'id': u'002', 'name': u'python learn'}]
for WarningData in WarningDatas:
    sNode=doc.createElement('WarningData')
    #sNode.setAttribute('id',str(book['id']))
    headNode=create_element(doc,'DynamicInfo',WarningData['DynamicInfo'])
    AlarmTimeNode=create_element(doc,'AlarmTime',WarningData['AlarmTime'])
    numberNode=create_element(doc,'number',WarningData['number'])
    
    sNode.appendChild(headNode)
    sNode.appendChild(AlarmTimeNode)
    sNode.appendChild(pageNode)
    top_element.appendChild(sNode)

xmlfile=open('WarningDatas.xml','w')
doc.writexml(xmlfile,addindent=' '*4, newl='\n', encoding='utf-8')
xmlfile.close()