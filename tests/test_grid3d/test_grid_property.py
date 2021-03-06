# coding: utf-8
"""Testing: test_grid_property"""
from __future__ import division, absolute_import
from __future__ import print_function

import os
import pytest

import numpy as np
import numpy.ma as npma

from xtgeo.xyz import Polygons
from xtgeo.grid3d import Grid
from xtgeo.grid3d import GridProperty
from xtgeo.common import XTGeoDialog
from xtgeo.common.exceptions import KeywordNotFoundError

import test_common.test_xtg as tsetup

# pylint: disable=logging-format-interpolation
# pylint: disable=invalid-name

# set default level
xtg = XTGeoDialog()

logger = xtg.basiclogger(__name__)

if not xtg.testsetup():
    raise SystemExit

td = xtg.tmpdir
testpath = xtg.testpath

# =============================================================================
# Do tests
# =============================================================================

testfile1 = '../xtgeo-testdata/3dgrids/reek/reek_sim_poro.roff'
testfile2 = '../xtgeo-testdata/3dgrids/eme/1/emerald_hetero.roff'
# testfile3 = '../xtgeo-testdata/3dgrids/bri/B.GRID'
# testfile4 = '../xtgeo-testdata/3dgrids/bri/B.INIT'
testfile5 = '../xtgeo-testdata/3dgrids/reek/REEK.EGRID'
testfile6 = '../xtgeo-testdata/3dgrids/reek/REEK.INIT'
testfile7 = '../xtgeo-testdata/3dgrids/reek/REEK.UNRST'
testfile8 = '../xtgeo-testdata/3dgrids/reek/reek_sim_zone.roff'
testfile8a = '../xtgeo-testdata/3dgrids/reek/reek_sim_grid.roff'
testfile9 = testfile1
testfile10 = '../xtgeo-testdata/3dgrids/bri/b_grid.roff'
testfile11 = '../xtgeo-testdata/3dgrids/bri/b_poro.roff'
polyfile = '../xtgeo-testdata/polygons/reek/1/polset2.pol'

testfile12a = '../xtgeo-testdata/3dgrids/reek/reek_sim_grid.grdecl'
testfile12b = '../xtgeo-testdata/3dgrids/reek/reek_sim_poro.grdecl'


def test_create():
    """Create a simple property"""

    x = GridProperty()
    assert x.ncol == 5, 'NCOL'
    assert x.nrow == 12, 'NROW'

    m = GridProperty(discrete=True)
    (repr(m.values))


def test_create_actnum():
    """Test creating ACTNUM"""
    x = GridProperty()
    act = x.get_actnum()

    print(x.values)
    print(act.values)
    print(x.nactive)
    print(x.ntotal)

    assert x.nactive < x.ntotal


def test_roffbin_import1():
    """Test of import of ROFF binary"""

    logger.info('Name is {}'.format(__name__))

    x = GridProperty()
    logger.info("Import roff...")
    x.from_file(testfile1, fformat="roff", name='PORO')

    logger.info(repr(x.values))
    logger.info(x.values.dtype)
    logger.info("Porosity is {}".format(x.values))
    logger.info("Mean porosity is {}".format(x.values.mean()))
    assert x.values.mean() == pytest.approx(0.1677, abs=0.001)


def test_roffbin_import1_roffapiv2():
    """Test of import of ROFF binary using new API"""

    logger.info('Name is {}'.format(__name__))

    x = GridProperty()
    logger.info("Import roff...")
    x.from_file(testfile1, fformat="roff", name='PORO', _roffapiv=2)

    logger.info(repr(x.values))
    logger.info(x.values.dtype)
    logger.info("Porosity is {}".format(x.values))
    logger.info("Mean porosity is {}".format(x.values.mean()))
    assert x.values.mean() == pytest.approx(0.1677, abs=0.001)


def test_roffbin_import1_new():
    """Test ROFF import, new code May 2018"""
    logger.info('Name is {}'.format(__name__))

    x = GridProperty()
    logger.info("Import roff...")
    x.from_file(testfile1, fformat="roff", name='PORO')
    logger.info("Porosity is {}".format(x.values))
    logger.info("Mean porosity is {}".format(x.values.mean()))


def test_roffbin_import2():
    """Import roffbin, with several props in one file."""

    logger.info('Name is {}'.format(__name__))
    dz = GridProperty()
    logger.info("Import roff...")
    dz.from_file(testfile2, fformat="roff", name='Z_increment')

    logger.info(repr(dz.values))
    logger.info(dz.values.dtype)
    logger.info("Mean DZ is {}".format(dz.values.mean()))

    hc = GridProperty()
    logger.info("Import roff...")
    hc.from_file(testfile2, fformat="roff", name='Oil_HCPV')

    logger.info(repr(hc.values))
    logger.info(hc.values.dtype)
    logger.info(hc.values3d.shape)
    _ncol, nrow, _nlay = hc.values3d.shape

    assert nrow == 100, 'NROW from shape (Emerald)'

    logger.info("Mean HCPV is {}".format(hc.values.mean()))
    tsetup.assert_almostequal(hc.values.mean(), 1446.4611912446985, 0.0001)


def test_roffbin_import2_roffapiv2():
    """Import roffbin, with several props in one file. API version 2"""

    logger.info('Name is {}'.format(__name__))
    dz = GridProperty()
    logger.info("Import roff...")
    dz.from_file(testfile2, fformat="roff", name='Z_increment', _roffapiv=2)

    logger.info(repr(dz.values))
    logger.info(dz.values.dtype)
    logger.info("Mean DZ is {}".format(dz.values.mean()))

    hc = GridProperty()
    logger.info("Import roff...")
    hc.from_file(testfile2, fformat="roff", name='Oil_HCPV', _roffapiv=2)

    logger.info(repr(hc.values))
    logger.info(hc.values.dtype)
    logger.info(hc.values3d.shape)
    _ncol, nrow, _nlay = hc.values3d.shape

    assert nrow == 100, 'NROW from shape (Emerald)'

    logger.info("Mean HCPV is {}".format(hc.values.mean()))
    tsetup.assert_almostequal(hc.values.mean(), 1446.4611912446985, 0.0001)

# def test_eclinit_import():
#     """Property import from Eclipse, a grid object first. Eclipse GRID"""

#     logger.info('Name is {}'.format(__name__))
#     gg = Grid(testfile3, fformat="grid")

#     actval = gg.get_actnum().values

#     print(actval[10, 0: 14, 3])

#     po = GridProperty()
#     logger.info("Import INIT...")
#     po.from_file(testfile4, fformat="init", name='PORO', grid=gg)
#     logger.debug(po.values[10, 0: 14, 3])
#     assert po.ncol == 20, 'NX from B.INIT'

#     logger.debug(po.values[0:400])
#     assert float(po.values3d[1:2, 13:14, 0:1]) == \
#         pytest.approx(0.17146, abs=0.001), 'PORO in cell 2 14 1'

#     # discrete prop
#     eq = GridProperty(testfile4, fformat="init", name='EQLNUM', grid=gg)
#     logger.info(eq.values[0:400])
#     assert eq.values3d[12:13, 13:14, 0:1] == 3, 'EQLNUM in cell 13 14 1'


def test_eclinit_import_reek():
    """Property import from Eclipse. Reek"""

    # let me guess the format (shall be egrid)
    gg = Grid(testfile5, fformat='egrid')
    assert gg.ncol == 40, "Reek NX"

    logger.info("Import INIT...")
    po = GridProperty(testfile6, name='PORO', grid=gg)

    logger.info(po.values.mean())
    assert po.values.mean() == pytest.approx(0.1677, abs=0.0001)

    pv = GridProperty(testfile6, name='PORV', grid=gg)
    logger.info(pv.values.mean())


def test_eclunrst_import_reek():
    """Property UNRST import from Eclipse. Reek"""

    gg = Grid(testfile5, fformat='egrid')

    logger.info("Import RESTART (UNIFIED) ...")
    press = GridProperty(testfile7, name='PRESSURE', fformat='unrst',
                         date=19991201, grid=gg)

    tsetup.assert_almostequal(press.values.mean(), 334.5232, 0.0001)


def test_eclunrst_import_soil_reek():
    """Property UNRST import from Eclipse, computing SOIL. Reek"""

    gg = Grid(testfile5, fformat='egrid')

    logger.info("Import RESTART (UNIFIED) ...")
    swat = GridProperty(testfile7, name='SWAT', fformat='unrst',
                        date=19991201, grid=gg)

    tsetup.assert_almostequal(swat.values.mean(), 0.8780, 0.001)

    sgas = GridProperty(testfile7, name='SGAS', fformat='unrst',
                        date=19991201, grid=gg)

    tsetup.assert_almostequal(sgas.values.mean(), 0.000, 0.001)

    soil = GridProperty(testfile7, name='SOIL', fformat='unrst',
                        date=19991201, grid=gg)

    tsetup.assert_almostequal(soil.values.mean(), 1.0 - 0.8780, 0.001)


def test_grdecl_import_reek():
    """Property GRDECL import from Eclipse. Reek"""

    rgrid = Grid(testfile12a, fformat='grdecl')

    assert rgrid.dimensions == (40, 64, 14)

    poro = GridProperty(testfile12b, name='PORO', fformat='grdecl',
                        grid=rgrid)

    poro2 = GridProperty(testfile1, name='PORO', fformat='roff',
                         grid=rgrid)

    tsetup.assert_almostequal(poro.values.mean(), poro2.values.mean(), 0.001)
    tsetup.assert_almostequal(poro.values.std(), poro2.values.std(), 0.001)

    with pytest.raises(KeywordNotFoundError):
        poro3 = GridProperty(testfile12b, name='XPORO', fformat='grdecl',
                             grid=rgrid)
        logger.debug('Keyword failed as expected for instance %s', poro3)

    # Export to ascii grdecl and import that again...
    exportfile = os.path.join(td, 'reekporo.grdecl')
    poro.to_file(exportfile, fformat='grdecl')
    porox = GridProperty(exportfile, name='PORO', fformat='grdecl',
                         grid=rgrid)
    tsetup.assert_almostequal(poro.values.mean(), porox.values.mean(), 0.001)

    # Export to binary grdecl and import that again...
    exportfile = os.path.join(td, 'reekporo.bgrdecl')
    poro.to_file(exportfile, fformat='bgrdecl')
    porox = GridProperty(exportfile, name='PORO', fformat='bgrdecl',
                         grid=rgrid)
    tsetup.assert_almostequal(poro.values.mean(), porox.values.mean(), 0.001)


# def test_export_roff():
#     """Property import from Eclipse. Then export to roff."""

#     gg = Grid()
#     gg.from_file(testfile3, fformat="grid")
#     po = GridProperty()
#     logger.info("Import INIT...")
#     po.from_file(testfile4, fformat="init", name='PORO', grid=gg)

#     po.to_file(os.path.join(td, 'bdata.roff'), name='PORO')

#     po.to_file(os.path.join(td, 'bdata.roffasc'), name='PORO',
#                fformat='roffasc')

#     pox = GridProperty(os.path.join(td, 'bdata.roff'), name='PORO')

#     pox.to_file(os.path.join(td, 'bdata2.roffasc'), name='POROAGAIN',
#                 fformat='roffasc')

#     print(po.values.mean())

#     assert po.values.mean() == pytest.approx(pox.values.mean(), abs=0.0001)


def test_io_roff_discrete():
    """Import ROFF discrete property; then export to ROFF int."""

    logger.info('Name is {}'.format(__name__))
    po = GridProperty()
    po.from_file(testfile8, fformat="roff", name='Zone')

    logger.info("\nCodes ({})\n{}".format(po.ncodes, po.codes))

    # tests:
    assert po.ncodes == 3
    logger.debug(po.codes[3])
    assert po.codes[3] == 'Below_Low_reek'

    # export discrete to ROFF ...TODO
    po.to_file(os.path.join(td, 'reek_zone_export.roff'), name='Zone',
               fformat='roff')

    # fix some zero values (will not be fixed properly as grid ACTNUM differs?)
    val = po.values
    val = npma.filled(val, fill_value=3)  # trick
    print(val.min(), val.max())
    po.values = val
    print(po.values.min(), po.values.max())
    po.values[:, :, 13] = 1  # just for fun test
    po.to_file(os.path.join(td, 'reek_zonefix_export.roff'), name='ZoneFix',
               fformat='roff')


def test_io_ecl2roff_discrete():
    """Import Eclipse discrete property; then export to ROFF int."""

    logger.info('Name is {}'.format(__name__))
    po = GridProperty()
    mygrid = Grid(testfile5)
    po.from_file(testfile6, fformat="init", name='SATNUM', grid=mygrid)

    print(po.codes)
    assert po.ncodes == 1
    assert isinstance(po.codes[1], str)

    po.to_file(os.path.join(td, 'ecl2roff_disc.roff'), name='SATNUM',
               fformat='roff')


def test_io_ecl_dates():
    """Import Eclipse with some more flexible dates settings"""

    logger.info('Name is {}'.format(__name__))
    po = GridProperty()
    px = GridProperty()
    mygrid = Grid(testfile5)
    po.from_file(testfile7, fformat="unrst", name='PRESSURE', grid=mygrid,
                 date='first')
    assert po.date == 19991201
    px.from_file(testfile7, fformat="unrst", name='PRESSURE', grid=mygrid,
                 date='last')
    assert px.date == 20030101


def test_io_to_nonexisting_folder():
    """Import a prop and try to save in a nonexisting folder"""

    po = GridProperty()
    mygrid = Grid(testfile5)
    po.from_file(testfile7, fformat="unrst", name='PRESSURE', grid=mygrid,
                 date='first')
    with pytest.raises(OSError):
        po.to_file(os.path.join("TMP_NOT", "dummy.grdecl"), fformat="grdecl")


def test_get_all_corners():
    """Get X Y Z for all corners as XTGeo GridProperty objects"""

    grid = Grid(testfile8a)
    allc = grid.get_xyz_corners()

    x0 = allc[0]
    y0 = allc[1]
    z0 = allc[2]
    x1 = allc[3]
    y1 = allc[4]
    z1 = allc[5]

    # top of cell layer 2 in cell 5 5 (if 1 index start as RMS)
    assert x0.values3d[4, 4, 1] == pytest.approx(457387.718, abs=0.01)
    assert y0.values3d[4, 4, 1] == pytest.approx(5935461.29790, abs=0.01)
    assert z0.values3d[4, 4, 1] == pytest.approx(1728.9429, abs=0.01)

    assert x1.values3d[4, 4, 1] == pytest.approx(457526.55367, abs=0.01)
    assert y1.values3d[4, 4, 1] == pytest.approx(5935542.02467, abs=0.01)
    assert z1.values3d[4, 4, 1] == pytest.approx(1728.57898, abs=0.01)


def test_get_cell_corners():
    """Get X Y Z for one cell as tuple"""

    grid = Grid(testfile8a)
    clist = grid.get_xyz_cell_corners(ijk=(4, 4, 1))
    logger.debug(clist)

    tsetup.assert_almostequal(clist[0], 457168.358886, 0.001)


def test_get_xy_values_for_webportal():
    """Get lists on webportal format"""

    grid = Grid(testfile8a)
    prop = GridProperty(testfile9, grid=grid, name='PORO')

    start = xtg.timer()
    coord, valuelist = prop.get_xy_value_lists(grid=grid)
    elapsed = xtg.timer(start)
    logger.info('Elapsed {}'.format(elapsed))
    logger.info('Coords {}'.format(coord))

    grid = Grid(testfile10)
    prop = GridProperty(testfile11, grid=grid, name='PORO')

    coord, valuelist = prop.get_xy_value_lists(grid=grid, activeonly=False)

    logger.info('Cell 1 1 1 coords\n{}.'.format(coord[0][0]))
    assert coord[0][0][0] == (454.875, 318.5)
    assert valuelist[0][0] == -999.0


def test_get_xy_values_for_webportal_ecl():
    """Get lists on webportal format (Eclipse input)"""

    grid = Grid(testfile5)
    prop = GridProperty(testfile6, grid=grid, name='PORO')

    coord, _valuelist = prop.get_xy_value_lists(grid=grid)
    logger.info('First active cell coords\n{}.'.format(coord[0][0]))
    tsetup.assert_almostequal(coord[0][0][0][1], 5935688.22412, 0.001)


def test_get_values_by_ijk():
    """Test getting values for given input arrays for I J K"""
    logger.info('Name is {}'.format(__name__))

    x = GridProperty()
    logger.info("Import roff...")
    x.from_file(testfile1, fformat="roff", name='PORO')

    iset1 = np.array([np.nan, 23, 22])
    jset1 = np.array([np.nan, 23, 19])
    kset1 = np.array([np.nan, 13, 2])

    res1 = x.get_values_by_ijk(iset1, jset1, kset1)

    tsetup.assert_almostequal(res1[1], 0.08403542, 0.0001)
    assert np.isnan(res1[0])


def test_values_in_polygon():
    """Test replace values in polygons"""
    logger.info('Name is {}'.format(__name__))

    xprop = GridProperty()
    logger.info("Import roff...")
    grid = Grid(testfile5)
    xprop.from_file(testfile1, fformat="roff", name='PORO', grid=grid)
    poly = Polygons(polyfile)
    xprop.geometry = grid

    xprop.operation_polygons(poly, 99, inside=True)
    tsetup.assert_almostequal(xprop.values.mean(), 25.1788, 0.01)

    # geom = grid.get_geometrics(return_dict=True)

    # layslice = xtgeo.plot.Grid3DSlice()
    # layslice.canvas(title="Layer 1")
    # layslice.plot_gridslice(grid, xprop, window=(geom['xmin'], geom['xmax'],
    #                                              geom['ymin'], geom['ymax']))
    # layslice.show()


# def test_get_xy_values_for_webportal_bri():
#     """Get lists on webportal format, small BRILLIG case"""

#     # Upps, work with this case and UNDEf cells are non-existing
#     # in GRID input!

#     grid = Grid(testfile3)
#     prop = GridProperty(testfile4, grid=grid, name='PORO')

#     coord, _valuelist = prop.get_xy_value_lists(grid=grid, activeonly=False)

#     logger.info('First active cell coords\n{}.'.format(coord[0][0]))
#     # assert coord[0][0][0] == (454.875, 318.5)
#     # assert valuelist[0][0] == -999.0
