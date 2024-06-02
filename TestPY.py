from datetime import datetime

def convert_date(date_str):
    year = "20" + date_str[:2]
    month = date_str[2:4]
    day = date_str[4:6]
    dt = datetime(int(year), int(month), int(day))
    return dt.strftime("%m/%d/%Y")

date_str = "210301"
print(convert_date(date_str))  # Output: 01/03/2021

date_str = "210301"
print(convert_date(date_str))  # Output: 01/03/21

print(convert_date("240511"))