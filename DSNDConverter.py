import sys

# Mozna Escape id
def process_xml(path):
    import xml.etree.ElementTree as ET
    dbname = input("Jmeno DB pro " + path+" ")
    header=""
    insertString = "INSERT INTO " + dbname+" "
    tree = None
    try:
        tree = ET.parse(path)
    except (ET.ParseError):
        with open(path, 'r+',encoding="utf-8") as original:
            data = original.read()
            original.close()
        with open(path, 'w', encoding="utf-8") as modified:
            data="<root>\n" + data.replace("&","&amp;") + "</root>"
            modified.write(data)
            modified.close()
        tree = ET.parse(path,parser=ET.XMLParser(encoding="utf-8"))
    root = tree.getroot()
    values=[]
    insertString = insertString + "(" + list(root[0].attrib.keys())[0] + ","
    for child in root:
        for node in child:
            if node.tag not in values:
                values.append(node.tag)
    for val in values:
        insertString=insertString+val+","
    insertString=insertString[:-1]+") VALUES "
    header=insertString
    finishString=""
    insertString=""
    for child in root:
        insertString=header
        insertString=insertString+"("+list(child.attrib.values())[0]+","
        dict={}
        for node in child:
            dict[node.tag]=node.text
        for val in values:
            if val not in list(dict.keys()):
                insertString = insertString + "NULL" + ","
            else:
                insertString = insertString + "'"+dict[val].replace("\\'","''")+"'" + ","
        insertString=insertString[:-1]+");\n"
        finishString=finishString+insertString
    with open(path.replace(path.split(".")[-1], "converted.sql"), "w") as file:
        file.write(finishString[:-1].replace("&","&."))
        file.close()

def process_json(path):
    import json
    insertString=""
    header=""
    finishString=""
    with open(path,"r",encoding="utf-8") as file:
        validJSON=""
        lines=file.readlines()
        i=0
        for line in lines:
            try:
                if "{" in line:
                    line=line.replace(line.split("\"")[1],str(i))
                    i=i+1
                    raise Exception(".")
                line=line.split(":")[0]+":"+"\""+line.split(":")[1][1:-1]+"\",\n"
                validJSON=validJSON+line
            except:
                validJSON=validJSON+line
            if "}" in line:
                validJSON=validJSON[:-6]+"\n},\n"
        validJSON=validJSON[:-4]+"\"\n}\n}"
        validJSON=json.loads(validJSON)
        values=[]
        for x in validJSON:
            for val in list(validJSON[x].keys()):
                if val not in values:
                    values.append(val)
        dbname = input("Jmeno DB pro " + path+" ")
        insertString="INSERT INTO "+dbname+" ("
        for val in values:
            insertString=insertString+val+","
        insertString=insertString[:-1]+") VALUES "
        header=insertString
        insertString=""
        for x in validJSON:
            insertString=header
            insertString=insertString+"("
            for val in values:
                if val not in validJSON[x]:
                    insertString=insertString+"''"+","
                else:
                    insertString=insertString+"'"+validJSON[x][val].replace(",","")+"'"+","
            insertString=insertString[:-1]+");\n"
            finishString=finishString+insertString
        file.close()
    with open(path.replace(path.split(".")[-1], "converted.sql"), "w") as file:
        file.write(finishString[:-1].replace("&","&."))
        file.close()
def process_html(path):
    from bs4 import BeautifulSoup
    import datetime
    dbname = input("Jmeno DB pro " + path+" ")
    insertString = "INSERT INTO " + dbname + " ("
    header=""
    finishString=""
    with open(path, 'r',encoding="utf-8") as file:
        data=file.read()
        soup=BeautifulSoup(data,"html.parser")
        table=soup.find('table')
        tr=table.find('tr')
        for th in tr.findAll('th'):
            insertString=insertString+th.text+","
        insertString=insertString[:-1]+") VALUES "
        header=insertString
        i=0
        for row in table.findAll('tr'):
            if i==0:
                pass
            else:
                insertString=header
                insertString=insertString+"("
                for td in row.findAll('td'):
                    try:
                        datetime.datetime.strptime(td.text, '%Y-%m-%d')
                        insertString=insertString+"TO_DATE('"+td.text+"','YYYY-MM-DD')"+","
                    except:
                        insertString=insertString+"'"+td.text+"'"+","
                insertString=insertString[:-1]+");\n"
                finishString=finishString+insertString
            i=i+1
        file.close()
    with open(path.replace(path.split(".")[-1], "converted.sql"), "w") as file:
        file.write(finishString[:-1].replace("&","&."))
        file.close()

def process_csv(path):
    insertString=""
    header=""
    finishString=""
    with open(path,"r",encoding="utf-8") as file:
        lines=file.readlines()
        dbname = input("Jmeno DB pro " + path+" ")
        insertString="INSERT INTO "+dbname+" ("
        for line in lines:
            print(line)
            break
        columns=input("Napište jména sloupců, v pořadí jako je uvedeno výše, oddělené čárkami ")
        insertString=insertString+columns.replace("\"","")+") VALUES "
        header=insertString
        for line in lines:
            insertString=header
            insertString=insertString+"("+line.replace("\"","'")[:-1]+");\n"
            finishString=finishString+insertString
        file.close()
    with open(path.replace(path.split(".")[-1],"converted.sql"),"w") as file:
        file.write(finishString[:-1].replace("&","&."))
        file.close()

def process_sql(path):
    header=""
    insertString=""
    finishString=""
    dbname = input("Jmeno DB pro " + path + " ")
    with open(path,"r",encoding="utf-8") as file:
        lines=file.readlines()
        i=0
        for line in lines:
            if i==0:
                header=line
                header=header.replace(header.split("INTO ")[1].split(" ")[0],dbname)
                i=i+1
                continue
            else:
                finishString=finishString + header.replace("\n","")+line.replace("\n","").replace("\"","'")+";\n"
        file.close()
    with open(path.replace(path.split(".")[-1], "converted.sql"), "w") as file:
        file.write(finishString[:-1])
        file.close()

def process_txt(path):
    header = ""
    insertString = ""
    finishString = ""
    with open(path, "r", encoding="utf-8") as file:
        lines=file.readlines()
        dbname = input("Jmeno DB pro " + path+" ")
        insertString="INSERT INTO "+dbname+" ("
        for line in lines:
            print(line)
            break
        columns=input("Napište jména sloupců, v pořadí jako je uvedeno výše, oddělené čárkami ")
        insertString=insertString+columns.replace("\"","")+") VALUES "
        header=insertString
        i=0
        for line in lines:
            i=i+1
            insertString=header+"("
            for key in line.split(", ",len(columns.split(", "))-1):
                insertString=insertString+"'"+key.replace("\n","")+"',"
            insertString=insertString[:-1]+")\n"
            finishString=finishString+insertString
        file.close()
    with open(path.replace(path.split(".")[-1], "converted.sql"), "w") as file:
        file.write(finishString[:-1])
        file.close()
file_paths = sys.argv[1:]
for path in file_paths:
    ext = path.split(".")[-1]
    if ext == "xml":
        process_xml(path)
    elif ext == "csv":
        process_csv(path)
    elif ext == "html":
        process_html(path)
    elif ext == "sql":
        process_sql(path)
    elif ext == "json":
        process_json(path)
    elif ext=="txt":
        process_txt(path)
    else:
        pass
