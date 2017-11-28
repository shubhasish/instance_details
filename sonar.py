import json
import requests
import sys
import os

help = "Enter a valid argument:\n\n" \
       "host: Host of the SonarQube server (Default 'localhost')\n" \
       "port: Port of the SonarQube server (Default '9000')\n" \
       "ccount: Threshold critical issues count\n" \
       "project: Project being Analyzed (Default 'All')\n"



arguments = sys.argv[1:]

#url = "http://172.19.24.29:9001/api/issues/search"
parameters = {"host":"localhost","port":"9000","ccount": 1 ,"project":None}
for argument in arguments:
    if "host" in argument:
        parameters['host'] = argument.split('=')[1]
    elif "port" in argument:
        parameters['port'] = argument.split('=')[1]
    elif "ccount" in argument:
        parameters['ccount'] = argument.split('=')[1]
    elif "project" in argument:
        parameters['project'] = argument.split('=')[1]
    else:
        print help
        os._exit(1)

url = "http://%s:%s/api/issues/search"%(parameters['host'],parameters['port'])

print "Getting Sonar Analysis for project: %s"%parameters['project']
print "Project URL: %s"%url
response = requests.get(url)
response_json =  response.json()
issues = response_json['issues']

types = {}

if parameters['project']:
    for issue in issues:
        project = issue['project']
        if parameters['project'] in project:
            severity = issue['severity']
            if severity in types:
                types[severity] = types[severity] + 1
            else:
                types[severity] = 1

else:
    for issue in issues:
        severity = issue['severity']
        if severity in types:
            types[severity] = types[severity] + 1
        else:
            types[severity] = 1

print "Total Critical Issues found: %s"%types['CRITICAL']
if types['CRITICAL'] > parameters['ccount']:
    print "Marking script as unsuccessful"
    os._exit(1)
else:
    print "Marking script as successful"
    os._exit(0)