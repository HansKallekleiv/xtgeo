/*
 *******************************************************************************
 *
 * Import ECL EGRID (version 2)
 *
 *******************************************************************************
 */

#include "libxtg.h"
#include "libxtg_.h"

/*
 *******************************************************************************
 *
 * NAME:
 *    grd3d_imp_ecl_egrid.c
 *
 * AUTHOR(S):
 *    Jan C. Rivenaes
 *
 * DESCRIPTION:
 *    Import a grid on eclipse EGRID format. This routine requires that an
 *    earlier scanning of the file is done, so that grid dimensions and
 *    the byte positions of the relevant records are known. These records are:
 *    MAPAXES, COORD, ZCORN, ACTNUM. Only binary format is supported.
 *
 * ARGUMENTS:
 *    points_v       i     a [9] matrix with X Y Z of 3 points
 *    nvector        o     a [4] vector with A B C D
 *    option         i     Options flag for later usage
 *    debug          i     Debug level
 *
 * RETURNS:
 *    Function: 0: upon success. If problems:
 *              1: some input points are overlapping
 *              2: the input points forms a line
 *    Result nvector is updated
 *
 * TODO/ISSUES/BUGS:
 *
 * LICENCE:
 *    CF XTGeo's LICENSE
 *******************************************************************************
 */



int grd3d_imp_ecl_egrid (
                         FILE *fc,
                         int nx,
                         int ny,
                         int nz,
                         long bpos_mapaxes,
                         long bpos_coord,
                         long bpos_zcorn,
                         long bpos_actnum,
                         double *p_coord_v,
                         double *p_zcorn_v,
                         int *p_actnum_v,
                         int debug
                         )
{

    /* locals */
    int *idum = NULL;
    float *fdum = NULL;
    double *ddum = NULL;

    double xma1, yma1, xma2, yma2, xma3, yma3, cx, cy, cz;

    float *tmp_mapaxes, *tmp_coord, *tmp_zcorn;
    int nxyz, nmapaxes, ncoord, nzcorn;
    int *tmp_actnum;
    int ib = 0;

    char sbn[24] = "grd3d_imp_ecl_egrid";

    /*
     * ========================================================================
     * INITIAL TASKS
     * ========================================================================
     */
    xtgverbose(debug);

    nxyz = nx * ny * nz;
    nmapaxes = 6;
    ncoord = (nx + 1) * (ny + 1) * 2 * 3;
    nzcorn = nx * ny *nz * 8;

    tmp_mapaxes = calloc(nmapaxes, sizeof(float));
    tmp_coord = calloc(ncoord, sizeof(float));
    tmp_zcorn = calloc(nzcorn, sizeof(float));
    tmp_actnum = calloc(nxyz, sizeof(int));

    /*=========================================================================
     * Read MAPAXES, which is present if bpos_mapaxes > 0
     * MAPAXES format is 6 numbers:
     * xcoord_endof_yaxis ycoord_endof_yaxis xcoord_origin ycoord_origin
     * xcoord_endof_xaxis ycoord_endof_xaxis
     * MAPAXES is a donkey ear growth fertilizer :-)
     */

    xma1 = 0; yma1 = 0; xma2 = 0; yma2 = 0; xma3 = 0; yma3 = 0;
    if (bpos_mapaxes >= 0) {
        grd3d_read_eclrecord(fc, bpos_mapaxes, 2, idum, 0, tmp_mapaxes,
                             nmapaxes, ddum, 0, debug);
        xma1 = tmp_mapaxes[0];
        yma1 = tmp_mapaxes[1];
        xma2 = tmp_mapaxes[2];
        yma2 = tmp_mapaxes[3];
        xma3 = tmp_mapaxes[4];
        yma3 = tmp_mapaxes[5];
        xtg_speak(sbn, 2, "Mapaxes 0: %f", tmp_mapaxes[0]);
    }

    /*=========================================================================
     * Read COORD
     */
    grd3d_read_eclrecord(fc, bpos_coord, 2, idum, 0, tmp_coord, ncoord, ddum,
                         0, debug);

    /* convert from MAPAXES, if present */
    xtg_speak(sbn, 2, "Conversion of COORD...");

    for (ib = 0; ib < ncoord; ib = ib + 3) {
        cx = tmp_coord[ib];
        cy = tmp_coord[ib+1];
        cz = tmp_coord[ib+2];
        if (bpos_mapaxes >= 0) {
            if (ib == 0) xtg_speak(sbn, 2, "Mapaxes transform is present... "
                                   "xma1=%f, xma2=%f, xma3=%f, "
                                   "yma1=%f, yma2=%f, yma3=%f, ",
                                   xma1, xma2, xma3, yma1, yma2, yma3);

            x_mapaxes(bpos_mapaxes, &cx, &cy, xma1, yma1, xma2, yma2,
                      xma3, yma3, 0, debug);
        }
        p_coord_v[ib] = cx;
        p_coord_v[ib+1] = cy;
        p_coord_v[ib+2] = cz;
    }
    xtg_speak(sbn, 2, "Conversion... DONE");

    /*=========================================================================
     * Read ZCORN
     */
    xtg_speak(sbn, 2, "Read ZCORN...");
    grd3d_read_eclrecord(fc, bpos_zcorn, 2, idum, 0, tmp_zcorn, nzcorn, ddum,
                         0, debug);

    xtg_speak(sbn, 2, "Read ZCORN... DONE");
    /*
     * ZCORN: Eclipse has 8 corners pr cell, while XTGeo format
     * use 4 corners (top of cell) except for last layer where also base is
     * used, i.e. for NZ+1 cell. This may cause problems if GAPS in GRDECL
     * format (like BRILLD test case); however rare...
     */

    xtg_speak(sbn, 2, "Transform ZCORN...");

    grd3d_zcorn_convert(nx, ny, nz, tmp_zcorn, p_zcorn_v, 0, debug);

    xtg_speak(sbn, 2, "Transform ZCORN... DONE");


    /*=========================================================================
     * Read ACTNUM directly
     */
    grd3d_read_eclrecord(fc, bpos_actnum, 1, p_actnum_v, nxyz, fdum, 0, ddum,
                         0, debug);

    int nact = 0;
    for (ib = 0; ib < nxyz; ib++) {
        if (p_actnum_v[ib] == 1) nact ++;
    }

    free(tmp_mapaxes);
    free(tmp_coord);
    free(tmp_zcorn);
    free(tmp_actnum);


    return nact;  // shall be number of active cells
}
