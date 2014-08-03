import xml.etree.ElementTree as ET

if __name__ == '__main__':

    top = ET.Element('list')
    depList = []
    tmpQueue = []

    name = raw_input("Please enter your Service's name:")
    
    depName = raw_input("Please enter the factors %s depends on:"%(name))
    depList = depName.split()
    for i in range(len(depList)):
        tmpQueue.append(depList[i])

    gateName = raw_input("Whether they need to work together (yes/no)?")
    # if gateName = yes then gate should be "OR"
    # otherwise gate should be "AND"

    node = ET.Element('node')
    node.attrib['id'] = name

    subNode = ET.Element('gate')
    if gateName == "yes":
        subNode.text = "OR"
    else:
        subNode.text = "AND"
    node.append(subNode)
    for item in depList:
        subNode = ET.Element('dep')
        subNode.text = item
        node.append(subNode)
    
    top.append(node)
    q = raw_input("Whether you want to quite (press Q/q)?")

    while(q != "q" and q != "Q"):

        while tmpQueue:
            tmpNode = tmpQueue[0]
            del tmpQueue[0]
            name = raw_input("Whether %s has dependencies (yes/no)?"%(tmpNode))
            if name == "no":
                continue
    
            depName = raw_input("Please enter the factors %s depends on:"%(tmpNode))
            depList = depName.split()

            gateName = raw_input("Whether they need to work together (yes/no)?")

            node = ET.Element('node')
            node.attrib['id'] = tmpNode

            subNode = ET.Element('gate')
            if gateName == "yes":
                subNode.text = "OR"
            else:
                subNode.text = "AND"
            node.append(subNode)
            for item in depList:
                subNode = ET.Element('dep')
                subNode.text = item
                node.append(subNode)
    
            top.append(node)
        q = raw_input("Whether you want to quite (press Q/q)?")

    file = open("result.xml", 'w')
    ET.ElementTree(top).write(file)
    file.close()
