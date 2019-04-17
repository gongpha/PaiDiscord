def th_format_date_diff(time=False):
    # from https://stackoverflow.com/questions/1551382/user-friendly-time-format-in-python/1551394#1551394
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """
    from datetime import datetime
    now = datetime.now()
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time,datetime):
        diff = now - time
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "ไม่นานมานี้"
        if second_diff < 60:
            return str(int(second_diff)) + " วินาทีที่แล้ว"
        if second_diff < 120:
            return "นาทีที่แล้ว"
        if second_diff < 3600:
            return str(int(second_diff / 60)) + " นาทีที่แล้ว"
        if second_diff < 7200:
            return "ชั่วโมงที่แล้ว"
        if second_diff < 86400:
            return str(int(second_diff / 3600)) + " ชั่วโมงที่แล้ว"
    if day_diff == 1:
        return "เมื่อวาน"
    if day_diff < 7:
        return str(int(day_diff)) + " วันที่แล้ว"
    if day_diff < 31:
        return str(int(day_diff / 7)) + " สัปดาห์ที่แล้ว"
    if day_diff < 365:
        return str(int(day_diff / 30)) + " เดือนที่แล้ว"
    return str(int(day_diff / 365)) + " ปีที่แล้ว"
