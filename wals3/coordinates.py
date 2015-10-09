from math import floor
import re

DEGREES = u"\xb0"
MINUTES = u"\u2032"
SECONDS = u"\u2033"

PATTERNS = {
    'lat_alnum': re.compile("(?P<degrees>[0-9]+)d(?P<minutes>[0-9]+)?(?P<seconds>'[0-9]+'')?(?P<hemisphere>S|N)"),
    'lon_alnum': re.compile("(?P<degrees>[0-9]+)d(?P<minutes>[0-9]+)?(?P<seconds>'[0-9]+'')?(?P<hemisphere>E|W)"),
    'lat_degminsec': re.compile(u'(?P<degrees>[0-9]+)\s*%s\s*((?P<minutes>[0-9]+)\s*%s\s*)?((?P<seconds>[0-9\.]+)\s*%s\s*)?(?P<hemisphere>S|N)' % (DEGREES, MINUTES, SECONDS)),
    'lon_degminsec': re.compile(u'(?P<degrees>[0-9]+)\s*%s\s*((?P<minutes>[0-9]+)\s*%s\s*)?((?P<seconds>[0-9\.]+)\s*%s\s*)?(?P<hemisphere>E|W)' % (DEGREES, MINUTES, SECONDS)),
}


def dec2degminsec(dec):
    """
    convert a floating point number of degrees to a triple
    (int degrees, int minutes, float seconds)
    
    >>> assert dec2degminsec(30.50) == (30, 30, 0.0)
    """
    degrees = int(floor(dec))
    dec = (dec - int(floor(dec)))*60
    minutes = int(floor(dec))
    dec = (dec - int(floor(dec)))*60
    seconds = dec
    return degrees, minutes, seconds


def degminsec2dec(degrees, minutes, seconds):
    """
    convert a triple (int degrees, int minutes, float seconds) to
    a floating point number of degrees
    
    >>> assert dec2degminsec(degminsec2dec(30,30,0.0)) == (30,30,0.0)
    """
    dec = float(degrees)
    if minutes:
        dec += float(minutes) / 60
    if seconds:
        dec += float(seconds) / 3600    
    return dec


class Coordinates(object):
    """
    >>> c = Coordinates('13dN', 0)
    >>> assert c.latitude >= 13
    >>> assert c.latitude <= 13.1
    >>> c = Coordinates(0, 0)
    >>> assert c.lat_to_string() == '0dN'
    >>> assert c.lon_to_string() == '0dE'
    >>> c = Coordinates(12.17, 92.83)
    >>> assert c.lat_to_string() == '12d10N'
    >>> assert c.lon_to_string() == '92d49E'
    >>> c = Coordinates(-12.17, -92.83)
    >>> assert c.lat_to_string() == '12d10S'
    >>> assert c.lon_to_string() == '92d49W'
    >>> lat, lon = '12d30N', '60d30E'
    >>> c = Coordinates(lat, lon)
    >>> assert c.lat_to_string() == lat
    >>> assert c.lon_to_string() == lon
    >>> for lat in range(-90, 90):
    ...     lat += 0.44446444444
    ...     c = Coordinates(lat, 0.222)
    ...     c2 = Coordinates(c.lat_to_string('degminsec'), c.lon_to_string('degminsec'), format='degminsec')
    ...     assert abs(lat - c2.latitude) < 0.001

    >>> for lon in range(-180, 180):
    ...     lon += 0.44443444444
    ...     c = Coordinates(-0.1111, lon)
    ...     c2 = Coordinates(c.lat_to_string('degminsec'), c.lon_to_string('degminsec'), format='degminsec')
    ...     assert abs(lon - c2.longitude) < 0.001
    """
    def __init__(self, lat, lon, format='alnum'):
        if isinstance(lat, float):
            self.latitude = lat
        elif isinstance(lat, int):
            self.latitude = float(lat)
        else:
            self.latitude = self.lat_from_string(lat, format)

        if isinstance(lon, float):
            self.longitude = lon
        elif isinstance(lon, int):
            self.longitude = float(lon)
        else:
            self.longitude = self.lon_from_string(lon, format)

    def _match(self, string, type, format):
        if not isinstance(string, unicode):
            if not hasattr(string, 'decode'): raise TypeError(string)
            try:
                string = string.decode('utf8')
            except:
                try:
                    string = string.decode('latin1')
                except:
                    raise

        if type+'_'+format in PATTERNS:
            p = PATTERNS[type+'_'+format]
        else:
            p = PATTERNS[type+'_alnum']

        m = p.match(string)
        if not m:
            raise ValueError(string)
        return m

    def lat_from_string(self, lat, format='alnum'):
        m = self._match(lat, 'lat', format)
        dec = degminsec2dec(m.group('degrees'),  m.group('minutes'), m.group('seconds'))
        if m.group('hemisphere') == 'S': dec = -dec
        return dec

    def lon_from_string(self, lon, format='alnum'):
        m = self._match(lon, 'lon', format)
        dec = degminsec2dec(m.group('degrees'),  m.group('minutes'), m.group('seconds'))
        if m.group('hemisphere') == 'W':
            dec = -dec
        return dec

    def _format(self, degrees, minutes, seconds, hemisphere, format):
        seconds = int(round(seconds))
        if seconds == 60:
            minutes += 1
            seconds = 0

        if 120 > minutes >= 60:
            degrees += 1
            minutes -= 60

        if format == 'alnum':
            res = "%sd" % degrees
            if minutes:
                res += "%02d" % minutes
            res += hemisphere
            return res
        res = "%s%s" % (degrees, DEGREES)

        if minutes: res += " %s%s" % (minutes, MINUTES)

        if seconds: res += " %s%s" % (seconds, SECONDS)
        res += " %s" % hemisphere
        return res

    def lat_to_string(self, format='alnum'):
        if self.latitude < 0: hemisphere = 'S'
        else: hemisphere = 'N'
        degrees, minutes, seconds = dec2degminsec(abs(self.latitude))
        return self._format(degrees, minutes, seconds, hemisphere, format)

    def lon_to_string(self, format='alnum'):
        if self.longitude < 0: hemisphere = 'W'
        else: hemisphere = 'E'
        degrees, minutes, seconds = dec2degminsec(abs(self.longitude))
        return self._format(degrees, minutes, seconds, hemisphere, format)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
