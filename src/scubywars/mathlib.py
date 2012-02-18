
from math import *


def angle(x, y):
    return atan2(-y, x)

def sqr(x):
    return x * x

def length(x, y):
    return sqrt(x * x + y * y)

def dist(x1, y1, x2, y2):
    return length(x2 - x1, y2 - y1)
    
def vector(x1, y1, x2, y2):
    return (x2 - x1, y2 - y1)
    
def norm(x, y):
    try:
	return (x / length(x, y), y / length(x, y))
    except:
	return (x, y)

def scale(x, y, s):
    try:
	return ((x / length(x, y)) * s, (y / length(x, y)) * s)
    except:
	return (x, y)

def cross (x1, y1, x2, y2):
    return x1 * y2 - x2 * y1

def dot (x1, y1, x2, y2):
    return x1 * x2 + y1 * y2

def rot (x, y, dir):
    return (x * cos(dir) - y * sin (dir), x * sin(dir) + y * cos(dir))

# calculate angular distance of object to current direction

def anglediff(x1, y1, x2, y2, dirx, diry):
    v2x, v2y = norm(dirx, diry)
    x, y = vector(x1, y1, x2, y2)
    v1x, v1y = norm(x, y)

    phi = acos(dot(v1x, v1y, v2x, v2y))
    if cross(v1x, v1y, v2x, v2y) < 0:
	phi *= -1
    return phi

def anglediff_bad2(x1, y1, x2, y2, dirx, diry):
    v2x, v2y = norm(dirx, diry)
    x, y = vector(x1, y1, x2, y2)
    v1x, v1y = norm(x, y)
    
    return atan2(v2y, v2x) - atan2(v1y, v1x)

def anglediff_bad(x1, y1, x2, y2, dirx, diry):
    my_angle = angle(dirx, diry)
    x, y = vector(x1, y1, x2, y2)
    enemy_angle = angle(x, y)

    diff = enemy_angle - my_angle;
    cdiff = diff + 2 * pi

    if fabs(cdiff) < fabs(diff):
	return cdiff
    return diff

def is_right(diff):
    return diff > 0.0

def is_behind(diff):
    return fabs(diff) > pi / 2 

def will_hit(x1, y1, sx1, sy1, r1, x2, y2, sx2, sy2, r2, maxdist, margin):
    d = dist(x1, y1, x2, y2)
    # if out of range, return 0
    if d > maxdist:
	return 0
    
    # if distance increases, return 0
    while 1:
	x1 += sx1
	y1 += sy1
	x2 += sx2
	y2 += sy2

	d2 = dist(x1 , y1, x2, y2)

	if d2 >= d:
	    return 0

	if d2 < (r1 + r2) * margin:
	    return 1

	d = d2

