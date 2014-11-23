import urllib2
from datetime import datetime, timedelta
import numpy
import mailjet
import requests
from requests.auth import HTTPBasicAuth
import os
import NLP

mailjet_api = mailjet.Api(api_key='bbbb2a82e844e6e6a8e68819b34bfa55', secret_key='a351a09703c3cce4c51308d301254f02')
payload = {"from":"nrsheth2@illinois.edu", "to":"niharrsheth@gmail.com", "subject":"Current Stock Information"}

f = open('button.html', 'r')
buttoncontent = f.read()
f.close()

g = open('senddata.html', 'w+')

today = datetime.now()
degree = 4
stockList = ["YHOO", "CAT", "GOOG", "BABA", "STJ", "INTC", "BAC", "ATI", "LUV", "GRPN", "WAIR", "OTIV", "AMDA", "ICLDW", "FB"]

rangevar = 5

successes = {}

d = str(today.month - 1).zfill(2)
e = str(today.day - 2).zfill(2)
f = str(today.year)

pastDate = today - timedelta(days=7)
a = str(pastDate.month - 1).zfill(2)
b = str(pastDate.day - 2).zfill(2)
c = str(pastDate.year)
positives = ""
prices = {}
for m in stockList:
    data = urllib2.urlopen("http://ichart.finance.yahoo.com/table.csv?s="+m+"&a="+a+"&b="+b+"&c="+c+"&d="+d+"&e="+e+"&f="+f+"&g=d&ignore=.csv")
        
    data.readline()
    cur = data.readline()
    prices[m] = cur.split(',')[1]

    info = []
    yvalues = []
    for j,i in enumerate(data.readlines()):
        #print i
        info = i.split(",")
        yvalues.append(float(info[4])-float(info[1]))
    
    coeff = numpy.polyfit(range(rangevar)[::-1], yvalues, degree)
    #NLPVal = NLP.calc([m])
    #print NLPVal
    blah = coeff[0]*rangevar**4 + coeff[1]*rangevar**3 + coeff[2]*rangevar**2 + coeff[3]*rangevar + coeff[4]
    if blah>0:
        positives += m+" "
        successes[m] = blah/float(info[4])*100*(1)#+NLPVal)
        print "val:", successes[m]
    #print blah
    print m, blah/float(info[4])*100
t = sorted(successes, key=successes.get, reverse=True)
positives = ""
for i in xrange(3): positives += t[i] + " "
buttoncontent = buttoncontent.replace("Stock1t", t[0])
buttoncontent = buttoncontent.replace("Stock2t", t[1])
buttoncontent = buttoncontent.replace("Stock3t", t[2])
buttoncontent = buttoncontent.replace("price1", prices[t[0]])
buttoncontent = buttoncontent.replace("price2", prices[t[1]])
buttoncontent = buttoncontent.replace("price3", prices[t[2]])
g.write(buttoncontent)
g.close()
requests.get("https://api.mailjet.com/v3/send", auth=HTTPBasicAuth('bbbb2a82e844e6e6a8e68819b34bfa55', 'a351a09703c3cce4c51308d301254f02'), params=payload)
os.system('curl -X POST --user "bbbb2a82e844e6e6a8e68819b34bfa55:a351a09703c3cce4c51308d301254f02" https://api.mailjet.com/v3/send -F from="nrsheth2@illinois.edu" -F to="niharrsheth@gmail.com" -F subject="Hai" -F inlineattachment="@senddata.html" -F text="Here are the recommended purchases:\n'+positives+'\nThese stocks demonstrate strong trends and are likely to increase in value today."')
