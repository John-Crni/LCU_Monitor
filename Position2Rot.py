from skyfield.api import Topos, load, EarthSatellite,position_of_radec,wgs84,Star

ts = load.timescale()
t0 = ts.now()

planets = load('de421.bsp')                                  
earth, mars = planets['earth'], planets['mars']        
site = planets['earth'] + wgs84.latlon(45, 5)
      

ts = load.timescale(builtin=True)
t = ts.now()                                      # <===== ③
astrometric = earth.at(t).observe(mars)           # <===== ④
ra, dec, distance = astrometric.radec()

print("RA=")
t = ts.now() 
star = Star(ra_hours=ra.hours,dec_degrees=dec.degrees)
astrometric = site.at(t).observe(star)
apparent = astrometric.apparent()
altaz = apparent.altaz()
print (altaz)

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