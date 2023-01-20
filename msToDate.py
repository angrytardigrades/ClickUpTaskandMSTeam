import datetime

def Mstodate (time_in_milliseconds):
    My_Date = datetime.datetime.fromtimestamp(time_in_milliseconds / 1000.0, tz=datetime.timezone.utc)
    return(My_Date)
