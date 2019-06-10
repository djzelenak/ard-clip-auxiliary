
import os
import subprocess
import argparse
import datetime as dt
import tarfile
from geo_utils import GetExtents

now = dt.datetime.now()

WKT = "ard_srs.wkt"

all_aux = ["aspect", "slope", "posidex", "dem", "trends", "mpw"]

name_pattern = "AUX_CU_HHHVVV_20000731_CURRENT-DATE_V01_AUX-NAME.tif"

all_hv = []

for h in range(33):

    for v in range(22):

        if len(str(h)) == 1: h = "0" + str(h)

        else: h = str(h)

        if len(str(v)) == 1: v = "0" + str(v)

        else: v = str(v)

        all_hv.append((h, v))


def make_filename(hv, aux, out_dir):
    """

    :param aux:
    :param hv:
    :param out_file:
    :return:
    """
    replace = {"HHHVVV": f"0{hv[0]}0{hv[1]}",
               "CURRENT-DATE": now.strftime("%Y%m%d"),
               "AUX-NAME": aux.upper()}

    out_file = name_pattern

    for key in replace.keys():
        out_file = out_file.replace(key, replace[key])

    return f"{out_dir}{os.sep}{out_file}"


def run_subset(in_file, out_file, ext):

    # For reference:
    # GeoExtent = namedtuple('GeoExtent', ['x_min', 'y_max', 'x_max', 'y_min'])

    run_trans ="gdal_translate -projwin {ulx} {uly} {lrx} {lry} -a_srs {wkt} -co COMPRESS=DEFLATE {src} {dst}".format(
        ulx=ext.x_min, uly=ext.y_max,
        lrx=ext.x_max, lry=ext.y_min,
        wkt=WKT,
        src=in_file,
        dst=out_file)

    subprocess.call(run_trans, shell=True)

    return None


def main_work(indir, outdir, aux=None, hv=None):
    """

    :param indir:
    :param outdir:
    :param aux:
    :param hv:
    :return:
    """
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    if hv is None:
        hv_ = all_hv
    else:
        hv_ = [hv]

    if aux is None:
        aux_ = all_aux
    else:
        aux_ = [aux]

    for tile in hv_:
        get_extent = GetExtents(int(tile[0]), int(tile[1]))

        out_file = None

        tarlist = []

        for prod in aux_:
            print(f"\nWorking on TILE: {tile}\n\t\tAUX: {prod}")

            out_file = make_filename(tile, prod, outdir)

            src_file = f"{indir}{os.sep}{prod}.tif"

            if not os.path.exists(out_file):
                run_subset(src_file, out_file, get_extent.TILE_EXTENT)

                tarlist.append(out_file)

        archive = outdir + os.sep + os.path.basename(out_file)[:35] + ".tar"

        with tarfile.open(archive, "w") as tar:
            for f in tarlist:
                tar.add(f, os.path.basename(f))
                
                os.remove(f)

    return None


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input", dest="indir", type=str, required=True,
                      help="Full path to the directory containing the CONUS ancillary data products")

    parser.add_argument("-o", "--output", dest="outdir", type=str, required=True,
                      help="Full path to the output location")

    parser.add_argument("-aux", dest="aux", type=str, required=False, choices = all_aux,
                        metavar=all_aux,
                        help="Specify the product to clip, if no product is selected then all products will be clipped")

    parser.add_argument('-hv', dest="hv", nargs=2, type=str, required=False,
                        metavar=('HH 0-32', 'VV 0-21'),
                        help='Horizontal and vertical ARD grid identifiers.  ' \
                             'WARNING:  if no chip identifier is supplied all'
                             ' 726 chips will be processed!')

    args = parser.parse_args()

    main_work(**vars(args))


if __name__ == '__main__':

    main()