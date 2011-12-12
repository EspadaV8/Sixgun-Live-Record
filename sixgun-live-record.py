#!/usr/bin/env python2
from icalendar import Calendar, Event, vDatetime, vDDDTypes
from datetime import datetime, timedelta
import pytz, urllib2, os

# URL of the ical LO calendar
cal_location = "https://www.google.com/calendar/ical/sixgun.org_kb0f1ok5gvtnfk50t8ni3s62j8%40group.calendar.google.com/public/basic.ics"

# URL of the mp3 stream
stream = "http://65.60.11.2:8216/live"

# Filename to save the ical file to
file_name = "sixgun.ics"

# Check to see if the file exists (possible race condition)
if not os.path.isfile(file_name):
    file(file_name, 'w').close()

# Open the file for writing, download the ical and save it locally
f = open(file_name, 'r+')
u = urllib2.urlopen(cal_location)
data = u.read()
f.write(data)

# There should be some checking here to see if the calendars have changed
# but Google update the DTSTAMP every time the ical is downloaded so any
# hash checking will fail

# Create an Calendar from the ical data
cal = Calendar.from_string(data)

# Get the current date/time UTC style
now = datetime.now(pytz.utc)

# Go over all the entries
for c in cal.walk():
    # If it's a VFREEBURY entry then check it out
    if c.name == "VFREEBUSY":
        # Get the starting time and make sure that it's a datetime instance
        # and it's in the future
        dtstart = str(c['dtstart'])
        ds = vDDDTypes.from_ical(dtstart)
        if(isinstance(ds, datetime)) and (ds > now):
            # Start 30 minutes before the live stream is meant to start
            early = ds - timedelta(minutes=30)

            dtend = str(c['dtend'])
            de = vDDDTypes.from_ical(dtend)

            # Finish 90 minutes after the stream is meant to finish
            late = de + timedelta(minutes=90)

            # Get the duration of the stream
            dur = late - early

            # Example crontab entry to record the stream
            print early.strftime("%M %H %d %m %w %Y"),"streamripper","-l",dur.seconds,stream
