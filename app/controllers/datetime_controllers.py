from datetime import datetime
from pytz import timezone

class DatetimeControllers():
  def __init__(self) -> None:
      pass

  @staticmethod
  def format():
    return "%d/%m/%Y"

  @staticmethod
  def time_now_brasil():
    format_date = "%d/%m/%Y"
    now_utc = datetime.now(timezone('UTC'))
    now_brasil = now_utc.astimezone(timezone('Brazil/East'))
    return now_brasil.strftime(format_date)

  @classmethod
  def is_person_already_been_updated_today(clt, person):
    time = clt.time_now_brasil()
    for honor in person['honors']:
      if honor['date'] == time:
        return True
    return False
