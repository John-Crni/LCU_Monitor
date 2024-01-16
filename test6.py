from skyfield.api import load, Topos
from astropy.coordinates import SkyCoord,FK5
from astropy import units as u
from astropy.time import Time
from astropy.coordinates import Angle


def convert_coordinates_to_degrees(ra_str, dec_str):
    """
    Convert coordinates in (hh mm ss.s, +-dd mm ss.s) format to degrees.

    Parameters:
    - ra_str: Right ascension string in (hh mm ss.s) format.
    - dec_str: Declination string in (+-dd mm ss.s) format.

    Returns:
    - ra_deg: Right ascension in degrees.
    - dec_deg: Declination in degrees.
    """
    # Convert RA and Dec strings to SkyCoord object
    coordinates = SkyCoord(ra=ra_str, dec=dec_str, unit=(u.hourangle, u.deg))

    # Get RA and Dec in degrees
    ra_deg = coordinates.ra.degree
    dec_deg = coordinates.dec.degree

    return ra_deg, dec_deg

ra_str = "4 30 30"
dec_str = "+15 20 15"

ra_1950,dec_1950=convert_coordinates_to_degrees(ra_str=ra_str, dec_str=dec_str)

b1950_coordinates = SkyCoord(ra=ra_1950*u.deg, dec=dec_1950*u.deg, frame='fk4', equinox='B1950')
j2000_coordinates = b1950_coordinates.transform_to(FK5(equinox='J2000'))


# 1950年の赤道座標をSkyCoordオブジェクトに変換
#coord_1950 = SkyCoord(ra=ra_1950*u.deg, dec=dec_1950*u.deg, obstime=t_1950)

# 1950年の赤道座標を2000年に変換
#coord_2000 = coord_1950.transform_to('icrs')

# 変換後の座標を表示
print("B1950座標:"+ str(b1950_coordinates.ra)+"DEC:"+str(b1950_coordinates.dec))
print("J2000座標:"+ str(j2000_coordinates.ra)+"DEC:"+str(j2000_coordinates.dec))

