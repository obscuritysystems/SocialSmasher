import pycurl
import json
import StringIO
import urllib
import pprint
import dateutil.parser
import datetime 
import sys
from twython import Twython, TwythonError
from facepy import GraphAPI
graph = GraphAPI('')

TWITTER_APP_KEY            = ''
TWITTER_APP_SECRET         = ''
TWITTER_OAUTH_TOKEN        = ''
TWITTER_OAUTH_TOKEN_SECRET = ''

# Requires Authentication as of Twitter API v1.1
twitter = Twython(TWITTER_APP_KEY, TWITTER_APP_SECRET, TWITTER_OAUTH_TOKEN, TWITTER_OAUTH_TOKEN_SECRET)
calendar = 'pdf2umolrh2hnclgvfpr9k681c%40group.calendar.google.com'


def calender_events(calendar,attributes):
    
    url_attri   = urllib.urlencode(attributes)
    url         = 'https://www.googleapis.com/calendar/v3/calendars/%s/events?%s' % (calendar,url_attri)
    print url 
    return curl_wrapper(url)



def event_detail(calendar,eventid,attributes):
    
    url_attri   = urllib.urlencode(attributes)
    url         = 'https://www.googleapis.com/calendar/v3/calendars/%s/events/%s?%s' % (calendar,eventid,url_attri)
    print url
    return curl_wrapper(str(url))

def curl_wrapper(url):
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.CONNECTTIMEOUT, 5)
    c.setopt(pycurl.FOLLOWLOCATION,2)
    c.setopt(c.TIMEOUT, 8)
    b = StringIO.StringIO()
    c.setopt(c.COOKIEFILE, '') 
    c.setopt(c.FAILONERROR, True)
    c.setopt(c.HTTPHEADER, ['Accept: application/json', 'Content-Type: application/x-www-form-urlencoded'])
    c.setopt(pycurl.WRITEFUNCTION, b.write)
    try:
       c.perform()
       raw = b.getvalue()
       return raw
       #d = json.loads(b.getvalue())

    except pycurl.error, error:
        errno, errstr = error
        print 'An error occurred: ', errstr
        return None

date_format = "%Y-%m-%dT00:00:00-06:00"
today =  datetime.datetime.today()
tomorrow = today + datetime.timedelta(days=10)
print today.strftime(date_format)
print tomorrow.strftime(date_format)

parameters = {'timeMax':tomorrow.strftime(date_format),
              'timeMin':today.strftime(date_format),
              'key':''}

calendar = 'pdf2umolrh2hnclgvfpr9k681c%40group.calendar.google.com'

raw_json = calender_events(calendar,parameters)
events = json.loads(raw_json)

#print events 
print "\n"
pp = pprint.PrettyPrinter(depth=6)

print len(events['items'])
for event in events['items']:
    print event['id']
    raw_event_details =  event_detail(calendar,event['id'],parameters)
    event_details = json.loads(raw_event_details)
    #pp.pprint(event_details)
    print event_details['summary']
    print event_details['description']
    print event_details['start']['dateTime']
    print event_details['end']['dateTime']
    yourdate = dateutil.parser.parse( event_details['start']['dateTime'])
    print yourdate
'''
    try:
        info = event_details['summary'] + ' starts: '  + event_details['start']['dateTime'] +' Ends:'+ event_details['end']['dateTime']
    except:
        try:
            info = event_details['summary'] + ' '  + event_details['start']['date']
        except:
            print "could not tweet" + event['id'] 
    try:
        twitter.update_status(status=info)
    except TwythonError as e:
        print e
    try:

        graph.post(path="Nemusbot/feed", message=info, caption=info, description=info)
    except:
        pass
'''
