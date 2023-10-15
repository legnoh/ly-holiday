import datetime as dt
import base64,zoneinfo
from icalendar import Event

ORIGIN_TZ=zoneinfo.ZoneInfo("Asia/Tokyo")

class Holiday:

  def __init__(self, date: dt.datetime.date, name: str):
    
    self.start_at = date
    self.end_at = self.start_at + dt.timedelta(days=1)

    self.start_ts = dt.datetime(
      self.start_at.year,
      self.start_at.month,
      self.start_at.day,
      tzinfo=ORIGIN_TZ
    )
    self.end_ts = dt.datetime(
      self.end_at.year,
      self.end_at.month,
      self.end_at.day,
      tzinfo=ORIGIN_TZ
    )

    self.year = date.year
    self.month = date.month
    self.day = date.day
    self.weekday = date.weekday()
    self.name = name

    self.created_at = dt.datetime.now(ORIGIN_TZ)
  
  def createIcalEvent(self):

    # UIDを作る
    raw_uid = "{s}{t}".format(s=self.start_at,t=self.name)
    uid_enc = raw_uid.encode('utf-8')
    uid = base64.b64encode(uid_enc)

    event = Event()
    event.add('UID', uid)
    event.add('SUMMARY', self.name)
    event.add('DTSTART', self.start_at.date())
    event.add('DTEND', self.end_at.date())
    event.add('TRANSP', 'OPAQUE')
    event.add('DTSTAMP', self.created_at)
    return event
  
  def createDict(self):
    return {
      "name": self.name,
      "date": self.start_at.strftime("%Y-%m-%d"),
      "start_time": int(self.start_ts.timestamp()),
      "end_time": int(self.end_ts.timestamp()),
    }
