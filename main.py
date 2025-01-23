import csv,os,json,logging
import datetime as dt
import modules.calendar as cal
from datetime import timedelta
from modules.holiday import Holiday

SLUG_FORMAT="%Y-%m-%d"
SATURDAY = 5
SUNDAY = 6

log_format = '%(asctime)s[%(filename)s:%(lineno)d][%(levelname)s] %(message)s'
log_level = os.getenv("LOGLEVEL", logging.INFO)
logging.basicConfig(format=log_format, datefmt='%Y-%m-%d %H:%M:%S%z', level=log_level)

if __name__ == '__main__':

  jp_holidays : dict[str, Holiday] = {}
  ly_holidays : dict[str, Holiday] = {}

  logging.info("opening syukujitsu.csv...")
  with open('syukujitsu.csv', encoding="Shift-JIS") as csvfile:
    events = csv.DictReader(csvfile)
    for event in events:
      holiday_datetime = dt.datetime.strptime(event["国民の祝日・休日月日"], "%Y/%m/%d")
      jp_slug = holiday_datetime.strftime(SLUG_FORMAT)
      jp_holidays[jp_slug] = Holiday(
        date=holiday_datetime,
        name=event["国民の祝日・休日名称"]
      )
  jp_holidays_slugs = list(jp_holidays.keys())

  logging.info("creating items...")
  for slug, event in jp_holidays.items():

    # 1/1があったら年末年始の予定を作る(CSVは1/1から時系列で並んでいること前提)
    if event.month == 1 and event.day == 1:
      for m,d in [[1,2], [1,3], [1,4], [12,29], [12,30], [12,31]]:
        ly_slug = "{y}-{m}-{d}".format(y=event.year, m=m, d=d)
        ly_holidays[ly_slug] = Holiday(dt.datetime(event.year, m, d), "年末年始休日")

    # 祝日の中に土曜日があった場合、前営業日まで遡って休日を作る
    if event.weekday == SATURDAY:
      all_holidays_slugs = jp_holidays_slugs + list(ly_holidays.keys())
      yesterday = event.start_at
      while True:
        yesterday = yesterday - timedelta(days=1)
        yesterday_slug = yesterday.strftime(SLUG_FORMAT)
        if (yesterday_slug not in all_holidays_slugs
            and yesterday.weekday() not in [SATURDAY,SUNDAY]):
          ly_holidays[yesterday_slug] = Holiday(yesterday, "ハッピーフライデー")
          break

  # それぞれics/jsonで出力
  logging.info("generating ical/json ...")
  ly_cal = cal.initCal("LY Holiday")
  lyj_cal = cal.initCal("LYJ Holiday")
  ly_list = []
  lyj_list = []

  for ly_holiday in list(ly_holidays.values()):
    ly_cal.add_component(ly_holiday.createIcalEvent())
    ly_list.append(ly_holiday.createDict())
  for lyj_holiday in list(jp_holidays.values()) + list(ly_holidays.values()):
    lyj_cal.add_component(lyj_holiday.createIcalEvent())
    lyj_list.append(lyj_holiday.createDict())

  if not os.path.exists("./dist"):
    os.mkdir("./dist")
  with open("./dist/ly-holidays.ics", mode='w') as f:
    f.write(ly_cal.to_ical().decode("utf-8"))
  with open("./dist/lyj-holidays.ics", mode='w') as f:
    f.write(lyj_cal.to_ical().decode("utf-8"))
  with open("./dist/ly-holidays.json", mode='w') as f:
    json.dump(ly_list,f)
  with open("./dist/lyj-holidays.json", mode='w') as f:
    json.dump(lyj_list,f)

  logging.info("all process were finished successfully!")
