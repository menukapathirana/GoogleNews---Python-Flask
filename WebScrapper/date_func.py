from datetime import *

def weekOld(day):
	d = datetime.today()
	fetchdate = day
	d = datetime.strftime(d,"%Y-%m-%d %H:%M:%S")
	d = datetime.strptime(d,"%Y-%m-%d %H:%M:%S")
	due = d - timedelta(days=7)
	x = fetchdate - due
	return x.days
