from skyfield.api import Topos, load, EarthSatellite,position_of_radec,wgs84,Star
from datetime import timedelta


planets = load('de421.bsp')                                  
earth, mars = planets['earth'], planets['mars']        
site = planets['earth'] + wgs84.latlon(45, 5)


      

ts = load.timescale(builtin=True)
t = ts.now()                                      # <===== ③
t1=ts.now()+timedelta(seconds=0) 
astrometric = earth.at(t).observe(mars)           # <===== ④
ra, dec, distance = astrometric.radec()

print(type(dec.degrees))

astrometric1 = earth.at(t1).observe(mars)           # <===== ④
ra1, dec1, distance1 = astrometric1.radec()


star = Star(ra_hours=ra.hours,dec_degrees=dec.degrees)
astrometric = site.at(t).observe(star)
apparent = astrometric.apparent()
altaz = apparent.altaz()
print (altaz)

star1 = Star(ra_hours=ra1.hours,dec_degrees=dec1.degrees)
astrometric1 = site.at(t1).observe(star)
apparent1 = astrometric1.apparent()
altaz1 = apparent1.altaz()
print (altaz1)

#------------------------------------------------

'''
osaka = Topos('34.6914 N', '135.4917 E')
line1 = '1 25544U 98067A   20226.06311231  .00000634  00000-0  19556-4 0  9992'
line2 = '2 25544  51.6462  66.9823 0001637  29.7739 108.2756 15.49160058240839'
iss = EarthSatellite(line1, line2, 'ISS (ZARYA)', ts)
satellites = load.tle('http://celestrak.com/NORAD/elements/stations.txt')
iss = satellites['ISS (ZARYA)']
alt, az, distance = (iss - osaka).at(t0).altaz()

print('Elevation:{0:.1f} 度'.format(alt.degrees))
print('Azmzh:{0:.1f} 度'.format(az.degrees))
print('距離:{0:.0f} km'.format(distance.km))
'''