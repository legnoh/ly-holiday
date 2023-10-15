from icalendar import Calendar

def initCal(name:str) -> Calendar:
  cal = Calendar()
  cal.add("X-WR-CALNAME", name)
  cal.add("COLOR", "#FF2968")
  cal.add("X-APPLE-CALENDAR-COLOR", "#FF2968")
  cal.add("TZID", "Asia/Tokyo")
  cal.add("X-WR-TIMEZONE", "Asia/Tokyo")
  return cal
