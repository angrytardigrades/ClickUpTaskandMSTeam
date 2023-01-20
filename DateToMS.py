from datetime import datetime
 
def Datetoms (my_datetime):
    epoch = datetime.utcfromtimestamp(0)
    return (my_datetime - epoch).total_seconds() * 1000.0
 
test = 123

print(type(test))