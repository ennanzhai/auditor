import xml.etree.ElementTree as ET
from tool_xml import *
import Queue

tree = ET.parse("hard-1.xml")
root = tree.getroot()
top = ET.Element('top')

name = " "
tmpQueue = Queue.Queue()

for itemList in root:
    if itemList.tag == "list":
        for child in itemList:
            if child.tag == "node":  # iterating each machine
                tmpQueue = Queue.Queue()
                name = child.attrib['id']
                tmpQueue.put(child)
                while not tmpQueue.empty():
                    tmpNode = tmpQueue.get()     
                    x = 0

                    wChild = ET.Element('node')
                    for item in tmpNode:
                        if item.tag == "node":
                            if x == 0:
                                wChild.attrib['id'] = name + "-" \
                                        + tmpNode.attrib['id']
                                tmpChild = ET.Element('gate')
                                tmpChild.text = 'OR'
                                wChild.append(tmpChild)
                                x = 1

                            tmpChild = ET.Element('dep')
                            tmpChild.text = name + "-" + item.attrib['id']
                            wChild.append(tmpChild)
                            tmpQueue.put(item)
                    if x == 1:
                        top.append(wChild)
                        print(wChild.attrib['id'])

file = open("a.xml", 'w')
#str = prettify(top)
ET.ElementTree(top).write(file)
file.close()


'''
child = xml.SubElement(root, 'node')
child.attrib['id'] = "tiger"

xml.SubElement(child, 'dep')


#Create a child element
child = xml.Element('child')
root.append(child)

#This is how you set an attribute on an element
child.attrib['name'] = "Charlie"
dep = xml.Element('dep')
dep.text = "ffff"
child.append(dep)


#Now lets write it to an .xml file on the hard drive

#Open a file
file = open("a.xml", 'w')

#Create an ElementTree object from the root element
xml.ElementTree(root).write(file)

#Close the file like a good programmer
file.close()
'''

'''
import xml.dom.minidom as Dom

if __name__ == "__main__":
    doc = Dom.Document()
    root_node = doc.createElement("book_store")
    root_node.setAttribute("name", "newhua")
    root_node.setAttribute("website", "http://www.zhixing123.cn")
    doc.appendChild(root_node)

    book_node = doc.createElement("book1")

    book_name_node = doc.createElement("name")
    book_name_value = doc.createTextNode("hamlet")
    book_name_node.appendChild(book_name_value)
    book_node.appendChild(book_name_node)

    book_author_node = doc.createElement("author")
    book_author_value = doc.createTextNode("William Shakespeare")
    book_author_node.appendChild(book_author_value)
    book_node.appendChild(book_author_node)

    root_node.appendChild(book_node)

    f = open("book_store.xml", "w+")
    f.write(doc.toprettyxml(indent = "\t", newl = "\n", encoding = "utf-8"))
    f.close()
'''
