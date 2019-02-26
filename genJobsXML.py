import csv
import genSingleJOB as gg
XMLList=[]

def createXMLfile(XMLList,filename):
    i=0
    with open(filename, encoding='utf-16', mode="w")as fp:
        #fp.write('<?xml version="1.0" encoding="ISO-8859-1"?>' + "\n" + '<jobs>' + "\n")
        fp.write('<?xml version="1.0"?>' + "\n" + '<jobs>' + "\n")

        for line in XMLList:
            fp.write(line[0] + "\n")
            i+=1
        fp.write('</jobs>')
        print ("Created " + filename + "; Job Count= " + str(i))

def createMarkupfile(HTMLList, filename):
    i = 0
    with open(filename, encoding='utf-16', mode="w")as fp:
        fp.write('<!DOCTYPE html><html lang="en">')

        for line in XMLList:
            fp.write(line[1] + "\n")
            i += 1
        fp.write('</html>')
        print("Created " + filename + "; Job Count= " + str(i))

if 1==2:
    filename = 'url.csv'
    filename = 'url - Accenture.csv'
    filename = 'url - cwjobs.url'
    print ("Opening File " + filename)
    with open(filename) as csvfile:
        readCSV = csv.reader(csvfile, delimiter='|')
        for row in readCSV:
            #XMLList.append(gg.generateXML(row[0],row[1]))
            XMLList.append(gg.generateXMLBS(row[0], row[1]))
else:
    #XMLList.append(gg.generateXMLBS("CWJobs", "https://www.cwjobs.co.uk/"))
    XMLList.append(gg.generateXMLBS("TotalJobs","https://www.totaljobs.com/job/senior-business-analyst/hsbc-job85232216"))

createXMLfile(XMLList,'CSout.XML')
createMarkupfile(XMLList,'CSHTML.html')
