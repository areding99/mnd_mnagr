import datetime


def get_weekday(date: datetime.datetime) -> str:
    today = date.weekday()

    if today == 0:
        return "Monday"
    elif today == 1:
        return "Tuesday"
    elif today == 2:
        return "Wednesday"
    elif today == 3:
        return "Thursday"
    elif today == 4:
        return "Friday"
    elif today == 5:
        return "Saturday"
    else:
        return "Sunday"
