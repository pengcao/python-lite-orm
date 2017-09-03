#!/usr/bin/env python
# encoding: utf-8
'''
@author: caopeng
@license: (C) Copyright 2013-2017.
@contact: deamoncao100@gmail.com
@software: garner
@file: GPSTransf.py
@time: 2017/5/26 20:07
@desc:
'''

import math

MERCATOR = 20037508.3427892
THETA = 180

class GPSTransf(object):

    # 墨卡托转经纬度
    @staticmethod
    def mercator2LatLng(mercatorX,mercatorY):
        lon = mercatorX/MERCATOR*THETA
        lat = mercatorY/MERCATOR*THETA
        lat = THETA / math.pi * (2 * math.atan(math.exp(lat * math.pi / THETA)) - math.pi / 2)
        return {'lon':lon,'lat':lat}

