from babel import dates, numbers, units
from datetime import datetime, timedelta
from pytz import timezone
from time import time

#l = 'he_il' # Hebrew
#l = 'ja_jp' # Japanese
#l = 'ko_kr' # Korean
#l = 'fr' # French
#l = 'ar' # Arabic
#l = 'zh_tw' # Chinese (traditional)
#l = 'zh_cn' # Chinese (simplified)
#l = 'ru_ru' # Russian

class LocaleExtension:
    """ Set the locale, and define locale functions """

    needs = {'themes'}
    provides = {'locale'}

    def __init__(self, userlang='en_us'):
        self.userlang = userlang

    def prepare(self, context):
        try:
            langs = context.request.accept_language.header_value.split(',')
        except:
            langs = []

        try:
            lang = langs[0]
        except:
            lang = self.userlang

        self.userlocale = lang.replace('-', '_')
        context.userlocale = self.userlocale

        context.time_ago = self.time_ago
        context.format_decimal = self.format_decimal
        context.format_time = self.format_time
        context.time_length = self.time_length
        context.format_percent = self.format_percent
        context.format_size = self.format_size

    def time_ago(self, dtime, threshold=2, add_direction=True, return_diff=False):
        if type(dtime) == str:
            dtime = datetime.strptime(dtime, '%Y-%m-%d %H:%M %z').replace(tzinfo=None)
        if type(dtime) != datetime:
            dtime = datetime.fromtimestamp(time() - (60*60*24*dtime))
        tdiff = dtime - datetime.utcnow()
        ret_diff = dates.format_timedelta(tdiff, threshold=threshold, add_direction=add_direction, locale=self.userlocale)
        ret_secs = tdiff.total_seconds()
        if return_diff:
            return [ret_diff, ret_secs]
        else:
            return ret_diff

    def format_decimal(self, number):
        return numbers.format_decimal(number, locale=self.userlocale)

    def format_time(self, seconds, is_avg=False):
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

    def time_length(self, tlen, threshold=0.85, granularity='second'):
        return dates.format_timedelta(timedelta(seconds=int(tlen)), threshold=threshold, granularity=granularity, locale=self.userlocale)

    def format_percent(self, number):
        return numbers.format_percent(number, format="#.#%", locale=self.userlocale)

    def format_size(self, number):
        if number is None:
            return ""
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
        return units.format_unit(number, unit, length='short', format="#.#", locale=self.userlocale)

