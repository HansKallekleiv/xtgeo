/*
 ******************************************************************************
 *
 * NAME:
 *    cube_export_rmsregular.c
 *
 * AUTHOR(S):
 *    Jan C. Rivenaes
 *
 * DESCRIPTION:
 *     Exports a cube to RMS regular format
 *
 * ARGUMENTS:
 *    nx...nz        i     cube dimensions
 *    xori...zinc    i     cube origin + increment in xyz
 *    rotation       i     Cube rotation (degrees)
 *    yflip          i     Cube YFLIP index (needed?)
 *    p_val_v        i     1D Array of cube values of ncx*ncy*ncz size
 *    nval           i     Number of elements in array
 *    file           i     File to export to
 *    option         i     For future use
 *    debug          i     Debug level
 *
 * RETURNS:
 *    Function: 0: upon success. If problems <> 0:
 *
 * TODO/ISSUES/BUGS:
 *    - yflip handling correctly dealt with?
 *
 * LICENCE:
 *    cf. XTGeo LICENSE
 ******************************************************************************
 */

#include "libxtg.h"
#include "libxtg_.h"


int cube_export_rmsregular (
                            int   nx,
                            int   ny,
                            int   nz,
                            double xori,
                            double yori,
                            double zori,
                            double xinc,
                            double yinc,
                            double zinc,
                            double rotation,
                            int yflip,
                            float *p_val_v,
                            long nval,
                            char  *file,
                            int   debug
                            )
{

    /* locals */
    char sub[24]="cube_export_rmsregular";
    FILE *fc;
    int swap, i, j, k;
    long ic;
    double xmax,ymax,zmax;
    float value;

    xtgverbose(debug);

    xtg_speak(sub, 4, "Setting VERBOSE....");

    /* if (yflip == -1) { */
    /*     xtg_speak(sub, 2, "Swap axes..."); */
    /*     cube_swapaxes(&nx, &ny, nz, &yflip, xori, &xinc, yori, &yinc, */
    /*                   &rotation, p_val_v, 0, debug); */
    /*     xtg_speak(sub, 2, "Swap axes...done"); */
    /* } */

    swap = x_swap_check();

    /* The Python/Perl class should do a check if file exist! */
    xtg_speak(sub, 2, "Opening file %s", file);
    fc = fopen(file, "wb");
    xtg_speak(sub, 2, "Exporting cube file %s", file);

    /* header is ASCII. NB remember the \n !... */
    xtg_speak(sub, 2, "Writing header ...");

    /* not sure if this xmax/ymax is the one that RMS wants...*/
    xmax = xori + xinc * (nx - 1);
    ymax = yori + yinc * (ny - 1);
    zmax = zori + zinc * (nz - 1);


    fprintf(fc, "Xmin/Xmax/Xinc: %11.3lf %11.3lf %le\n", xori, xmax, xinc);
    fprintf(fc, "Ymin/Ymax/Yinc: %11.3lf %11.3lf %le\n", yori, ymax, yinc);
    fprintf(fc, "Zmin/Zmax/Zinc: %11.3lf %11.3lf %le\n", zori, zmax, zinc);
    fprintf(fc, "Rotation: %9.5f\n", rotation);
    fprintf(fc, "Nx/Ny/Nz: %d %d %d\n", nx, ny, nz);


    xtg_speak(sub, 2, "Writing data ...");

    /* Data are written in Fortran order (columns fastest) */
    /* But input is C order. Hence x_ijk2ic */

    for (k = 1; k <= nz; k++) {
        for (j = 1; j <= ny; j++) {
            for (i = 1; i <= nx; i++) {

                ic = x_ijk2ic(i, j, k, nx, ny, nz, 0);

                value = p_val_v[ic];
                if (value > UNDEF_LIMIT) {
                    value=UNDEF_CUBE_RMS;
                }

                /* byte swapping if needed */
                if (swap == 1) SWAP_FLOAT(value);

                if (fwrite(&value, 4, 1, fc) !=1 ) {
                    xtg_error(sub, "Write failed in routine %s", sub);
                    return -1;
                }
            }
        }
    }

    fclose(fc);

    return EXIT_SUCCESS;
}
