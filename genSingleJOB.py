import urllib.request
from bs4 import BeautifulSoup
from Job import Job
import re
from datetime import datetime
import json


TAG_RE = re.compile(r'<[^>]+>')

def remove_tags(text):
    return TAG_RE.sub('', text)

def getpage_u(URL):
    request = urllib.request.Request(URL,
                                     None, {
                                         'User-agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5'})
    try:
        response = urllib.request.urlopen(request)
    except:
        print("something wrong")
        response=''

    content = response.read()

    print(content)
    return str(content)

def getString(keyword, html,terminator,offset):
    startp = html.find(keyword)
    i=len(keyword)+offset
    outp=''
    while (html[startp+i])!=terminator:
        outp += html[startp+i]
        i+=1

    return outp


def parseAccenture(soup, job,html):
    tag = soup.find("meta", property="og:title")
    #print(tag.attrs['content'])
    job.title = tag.attrs['content']

    tag = soup.find("div", itemprop="description")
    job.description = remove_tags(str(tag))

    ### THIS WORKS - but expensive
    #lsoup = BeautifulSoup(tag.text, 'html.parser')
    #print(lsoup._most_recent_element.strip)
    #desc = lsoup._most_recent_element
    #job.description = desc.strip()

    # ----THESE WORK BUT MAYBE CRUDE
    #job.location=getString('<strong>Location:</strong>',html,'<',0)
    #job.datepublished = getString('Date published:',html,'<',9)

    paras = soup.find_all('p')
    for para in paras:
        if 'Location' in para.text:
            job.location = para.text.split(':')[1]
        elif 'Date published' in para.text:
            jobdate2 = datetime.strptime(para.text.split(':')[1].strip(),"%d-%b-%Y")
            job.datepublished = jobdate2.strftime("%d/%m/%Y")

    return job;

def parseCWJobs(soup, job,html):

    datep_icon = soup.body.find('li', attrs={'class': 'date-posted icon'})
    job.datepublished = datep_icon.next_element.next_element.text

    if job.datepublished == 'Expired':
        job.expired()
        return job;

    locn_pos = soup.body.find('div', attrs={'class': 'travelTime-locationText'})

    if locn_pos is None:
        location_icon = soup.body.find('li', attrs={'class': 'location icon'})
        job.location = location_icon.next_element.next_element.text
    else:
        job.location = locn_pos.next_element.next_element.text

    salary_icon = soup.body.find('li', attrs={'class': 'salary icon'})
    job.salary = salary_icon.next_element.next_element.text

    jobp = soup.body.find('script', attrs={'id':'jobPostingSchema'})

    ##to cope with double quotes embedded inside JSON objects
    if jobp is None:
        job.title = 'Not Specified'
        job.description = 'Not Specified'
        job.company = 'Not Specified'
    else:
        z = str(jobp.text).replace('\\\\"','')

        ##remove carriage returns etc
        a = z.replace('\\n', ' ').replace("'",'').replace('\\r', ' ').replace('\\', ' ')

        ##load into a JSON object (dictionary)
        d = json.loads(a)

        job.title=(d["title"])
        job.description= (d["description"]).replace('xe2 x80 x93','-').replace(' xe2 x80 x99',"'").replace('xe2 x80 xa6',"...").replace('xc2 xb7','&#x25CF;').replace('xc2 xa3','£').replace('xe2 x80 x9d','"').replace('xe2 x80 x9c','"')
        job.company = (d["hiringOrganization"]["name"])
        job.addressLocality =(d["jobLocation"]["address"]["addressLocality"])
        job.addressRegion = (d["jobLocation"]["address"]["addressRegion"])

        job.setCSDesc()

    return job;

def generateXMLBS(template,URL):

    html=getpage_u(URL)

    soup = BeautifulSoup(html, 'html.parser')

    job = Job(URL,template)

    if template=="Accenture":
        parseAccenture(soup,job,str(html))
    elif template == "CWJobs":
            parseCWJobs(soup, job, str(html))
    elif template == "TotalJobs":
        parseCWJobs(soup, job,  (html))

    xml = [job.createXML(),job.description]
    #print (xml)

    return xml


def generateXML(template,URL):
    html = getpage(URL)

    print(html)

    if template=="CWJobs":
        xml = ParseCWJobs(html)
    elif template=="TotalJobs":
        xml = ParseCWJobs(html)

    return xml


