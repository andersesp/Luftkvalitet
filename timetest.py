
timestamp = "23:00:00"
hour = timestamp[0] + timestamp[1]
if hour == "23":
    hour = 0
else:
    hour = int(hour) + 1

hour = str(hour)
newtimestamp = ""
if len(hour) == 1:
    newtimestamp += "0"
    newtimestamp += hour
else:
    newtimestamp += hour[0]
    newtimestamp += hour[1]

for i in range(2, len(timestamp),1):
    newtimestamp += timestamp[i]
print newtimestamp
