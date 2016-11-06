from babel import dates, numbers, units
from datetime import datetime, timedelta
from time import time

l = 'en'
#l = 'he_il' # Hebrew
#l = 'ja_jp' # Japanese
#l = 'ko_kr' # Korean
#l = 'fr' # French
#l = 'ar' # Arabic
#l = 'zh_tw' # Chinese (traditional)
#l = 'zh_cn' # Chinese (simplified)
#l = 'ru_ru' # Russian


def format_time(seconds, is_avg=False):
	try:
		ft = dates.format_time(int(seconds), format='HH:mm:ss')
	except:
		return seconds
	v = ft.split(':')
	if v[0] == '00':
		v.pop(0)
		rv = ':'.join(v)
	else:
		rv = ft
	if is_avg:
		rv = '~' + rv
	return rv

def time_ago(dtime, add_direction=True):
	if type(dtime) != datetime:
		dtime = datetime.fromtimestamp(time() - (60*60*24*dtime))
	return dates.format_timedelta(dtime - datetime.utcnow(), threshold=2, add_direction=add_direction, locale=l)

def format_decimal(number):
	return numbers.format_decimal(number, locale=l)

def time_length(tlen):
	return dates.format_timedelta(timedelta(seconds=int(tlen)), locale=l)

def format_percent(number):
	return numbers.format_percent(number, format="#.#%", locale=l)

def format_size(number):
	s = 1024
	kb = s
	mb = kb * s
	gb = mb * s
	tb = gb * s

	if number >= tb:
		number /= tb
		unit = 'terabyte'
	elif number >= gb:
		number /= gb
		unit = 'gigabyte'
	elif number >= mb:
		number /= mb
		unit = 'megabyte'
	elif number >= kb:
		number /= kb
		unit = 'kilobyte'
	else:
		unit = 'byte'
	return units.format_unit(number, unit, length='short', format="#.#", locale=l)
	
