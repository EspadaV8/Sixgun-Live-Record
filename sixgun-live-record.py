#!/usr/bin/env python2
from icalendar import Calendar, Event, vDatetime, vDDDTypes
from datetime import datetime, timedelta
import pytz, urllib2, os

cal_location = "https://www.google.com/calendar/ical/sixgun.org_kb0f1ok5gvtnfk50t8ni3s62j8%40group.calendar.google.com/public/basic.ics"
stream = "http://65.60.11.2:8216/live"
file_name = "sixgun.ics"

if not os.path.isfile(file_name):
    file(file_name, 'w').close()

f = open(file_name, 'r+')
u = urllib2.urlopen(cal_location)
data = u.read()
f.write(data)

cal = Calendar.from_string(data)
now = datetime.now(pytz.utc)

for c in cal.walk():
    if c.name == "VFREEBUSY":
        dtstart = str(c['dtstart'])
        ds = vDDDTypes.from_ical(dtstart)
        if(isinstance(ds, datetime)) and (ds > now):
            early = ds - timedelta(minutes=30)

            dtend = str(c['dtend'])
            de = vDDDTypes.from_ical(dtend)
            late = de + timedelta(minutes=90)

            dur = late - early

            print early.strftime("%M %H %d %m %w %Y"),"streamripper",stream,"-l",dur.seconds
