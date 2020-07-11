import testdata
from testdata import datetime

EVENT_TYPES = ["USER_DISCONNECT", "USER_CONNECTED", "USER_LOGIN", "USER_LOGOUT"]


class EventsFactory(testdata.DictFactory):
    start_time = testdata.DateIntervalFactory(datetime.datetime.now(), datetime.timedelta(minutes=12))
    end_time = testdata.RelativeToDatetimeField("start_time", datetime.timedelta(minutes=20))
    event_code = testdata.RandomSelection(EVENT_TYPES)


for event in EventsFactory.generate(100):
    print(event)
