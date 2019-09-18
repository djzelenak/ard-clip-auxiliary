"""
Description: Take CONUS NLCD layers and clip them to the extent of a given reference layer.
Based on script "RasterMask_reproject_resample_GDAL.py" by Devendra Dahal written on 5/12/2015
Last Updated: 1/10/2017, 2/2/2017, 9/18/2017 by Dan Zelenak
"""

import datetime
import os
import datetime as dt
import subprocess
import sys
import argparse
from collections import namedtuple

print(sys.version)

WKT = "ard_srs.wkt"

GeoExtent = namedtuple('GeoExtent', ['x_min', 'y_max', 'x_max', 'y_min'])

CONUS_EXTENT = GeoExtent(x_min=-2565585,
                         y_min=14805,
                         x_max=2384415,
                         y_max=3314805)


now = dt.datetime.now()

t1 = datetime.datetime.now()
print(t1.strftime("%Y-%m-%d %H:%M:%S"))


def make_filename(hv, aux, out_dir):
    """

    :param aux:
    :param hv:
    :param out_file:
    :return:
    """
    name_pattern = "AUX_CU_HHHVVV_20010101_CURRENT-DATE_V01_AUX-NAME.tif"

    replace = {"HHHVVV": f"0{hv[0]}0{hv[1]}",
               "CURRENT-DATE": now.strftime("%Y%m%d"),
               "AUX-NAME": aux.upper()}

    out_file = name_pattern

    for key in replace.keys():
        out_file = out_file.replace(key, replace[key])

    return os.path.join(out_dir, out_file)


def geospatial_hv(h, v, loc=CONUS_EXTENT):
    """
    Geospatial extent and 30m affine for a given ARD grid location.

    :param h:
    :param v:
    :param loc:
    :return:
    """

    xmin = loc.x_min + h * 5000 * 30
    xmax = loc.x_min + h * 5000 * 30 + 5000 * 30
    ymax = loc.y_max - v * 5000 * 30
    ymin = loc.y_max - v * 5000 * 30 - 5000 * 30

    return GeoExtent(x_min=xmin, x_max=xmax, y_max=ymax, y_min=ymin)


def get_hv_list(h_list=(0, 32), v_list=(0, 21)):
    h_range = range(h_list[0], h_list[1] + 1)
    v_range = range(v_list[0], v_list[1] + 1)

    out_hv = list()

    for h in h_range:
        for v in v_range:
            if len(str(h)) == 1:
                h = "0" + str(h)
            else:
                h = str(h)
            if len(str(v)) == 1:
                v = "0" + str(v)
            else:
                v = str(v)

            out_hv.append((h, v))

    return out_hv


def cli():
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input", type=str, required=True, metavar='FILE_PATH',
                        help="Full path to the input dataset")

    parser.add_argument("-o", "--output", type=str, required=True, metavar='DIR_PATH',
                        help="Full path to the output directory")

    parser.add_argument("--name", type=str, metavar="DATASET_NAME", choices=('NLCD', 'NLCDTRN'),
                        help="Specify the source dataset name (NLCD or NLCDTRN)")

    parser.add_argument('--hv', nargs=2, type=int, required=False,
                        metavar=('HH (0-32)', 'VV (0-21)'), default=None,
                        help='Specify a single tile to process')

    parser.add_argument('--hh', nargs=2, type=int, required=False,
                        metavar=('HH (0-32)'), default=(0, 32),
                        help='Horizontal grid range to process - must use 2 values - if a single col '
                             'then use the same value twice')

    parser.add_argument('--vv', nargs=2, type=int, required=False,
                        metavar=('VV (0-21)'), default=(0, 21),
                        help='Vertical grid range to process - must use 2 values - if a single row '
                             'then use the same value twice')

    args = parser.parse_args()

    main(**vars(args))

    return None


def main(input, output, name, hv=None, vv=None, hh=None):

    if (hv and hh) or (hv and vv):
        print("Invalid args: a single HV tile was specified along with a row and/or column range")
        sys.exit(0)

    if not (hv):
        # Specific row/column range(s)
        tiles = get_hv_list(h_list=hh, v_list=vv)
    else:
        # A single tile
        tiles = get_hv_list(h_list=(hv[0], hv[0]), v_list=(hv[1], hv[1]))

    print('\tWorking on {}'.format(os.path.basename(input)))

    if not os.path.exists(output):
        os.makedirs(output)

    for tile in tiles:
        clip_extent = geospatial_hv(h=int(tile[0]), v=int(tile[1]))

        print('\n------------------------')

        print('Extent of the out layer:\n\t\t\t', clip_extent.y_max,
              '\n\n\t', clip_extent.x_min, '\t\t\t', clip_extent.x_max, '\n\n\t\t\t', clip_extent.y_min)

        print('------------------------\n')

        in_file = os.path.basename(input)
        out_file = make_filename(hv=tile, aux=name, out_dir=output)

        print('\tProducing output {}'.format(out_file))

        run_trans = "gdal_translate -projwin {ulx} {uly} {lrx} {lry} -a_srs {wkt} {src} {dst}".format(
            ulx=clip_extent.x_min, uly=clip_extent.y_max,
            lrx=clip_extent.x_max, lry=clip_extent.y_min,
            wkt=WKT,
            src=input,
            dst=out_file)

        subprocess.call(run_trans, shell=True)

    print("\nAll done")


if __name__ == '__main__':
    cli()

t2 = datetime.datetime.now()

print(t2.strftime("%Y-%m-%d %H:%M:%S"))

tt = t2 - t1

print("\nProcessing time: " + str(tt))
