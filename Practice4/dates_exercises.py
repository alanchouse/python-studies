

# 1
import datetime

print(datetime.datetime.now() - datetime.timedelta(5))

# 2

import datetime
 
print(datetime.datetime.now() - datetime.timedelta(1)) # Вчера
print(datetime.datetime.now())                         # Сегодня
print(datetime.datetime.now() + datetime.timedelta(1)) # Завтра

# 3

import datetime
 
print(datetime.datetime.now().replace(microsecond=0))

# 4 

import datetime

date1 = datetime.datetime(2026, 5, 20)
date2 = datetime.datetime(2026, 5, 15)
print((date1 - date2).total_seconds())