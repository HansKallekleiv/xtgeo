# -*- coding: utf-8 -*-
"""The XTGeo common package"""
from __future__ import division, absolute_import
from __future__ import print_function

# flake8: noqa
from xtgeo.common.xtgeo_dialog import XTGeoDialog
from xtgeo.common.xtgeo_dialog import XTGDescription
from xtgeo.common.xtgeo_dialog import XTGShowProgress

from xtgeo.common.exceptions import WellNotFoundError

from xtgeo.common._fileutils import _get_fhandle, _close_fhandle
