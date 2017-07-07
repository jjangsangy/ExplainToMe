from dateutil.parser import parser

def datetimefilter(value, format='%Y/%m/%d %H:%M'):
    p = parser()
    dt = p.parse(value)
    return dt.strftime(format)
