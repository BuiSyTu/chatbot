from datetime import date

def get_current_date():  
    todays_date = date.today()
    
    year = todays_date.year
    month = todays_date.month
    day = todays_date.day

    weekdays = {
        0: 'thứ hai',
        1: 'thứ ba',
        2: 'thứ tư',
        3: 'thứ năm',
        4: 'thứ sáu',
        5: 'thứ bảy',
        6: 'chủ nhật'
    }
    day_in_week =  weekdays[todays_date.weekday()]

    return f'Hôm nay là thứ {day_in_week} ngày {day}/{month}/{year}'
