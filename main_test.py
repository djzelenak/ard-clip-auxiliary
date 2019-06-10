import os
import subprocess
import argparse
from geo_utils import GetExtents

WKT = "ard_srs.wkt"

def get_files(arg_in, arg_name, arg_out):
    # TODO add function to replace repeated code
    """
    src_file = arg_in + os.sep + arg_name + ".tif"

    out_dest = arg_out + os.sep + "{}_tile".format(arg_name)

    if not os.path.exists(out_dest):

        os.makedirs(out_dest)

    out_file = out_dest + os.sep + "h{h}v{v}_".format(h=hv[0], v=hv[1]) + arg_name + ".tif"

    return src_file, out_file
    """
    pass


def run_subset(in_file, out_file, ext):

    # For reference:
    # GeoExtent = namedtuple('GeoExtent', ['x_min', 'y_max', 'x_max', 'y_min'])

    run_trans ="gdal_translate -projwin {ulx} {uly} {lrx} {lry} -a_srs {wkt} -co COMPRESS=DEFLATE -eco {src} {dst}".format(
        ulx=ext.x_min, uly=ext.y_max,
        lrx=ext.x_max, lry=ext.y_min,
        wkt=WKT,
        src=in_file,
        dst=out_file)

    subprocess.call(run_trans, shell=True)

    return None


def main():

    all_names = ["aspect", "slope", "posidex", "dem", "trends", "mpw"]

    # all_hv = [(str(h), str(v)) for h in range(33) for v in range(22)]

    all_hv = []

    for h in range(33):

        for v in range(22):

            if len(str(h)) == 1: h = "0" + str(h)

            else: h = str(h)

            if len(str(v)) == 1: v = "0" + str(v)

            else: v = str(v)

            all_hv.append((h, v))

    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input", type=str, required=True,
                      help="Full path to the directory containing the ancillary data products")

    parser.add_argument("-o", "--output", type=str, required=True,
                      help="Full path to the output location")

    parser.add_argument("-n", "--name", type=str, required=False, choices = all_names,
                      help="Specify the product to clip, if no product selected then all products will be clipped")

    parser.add_argument('-hv', nargs=2, type=str, required=False, metavar=('HH (0-32)', 'VV (0-21)'),
                        help='Horizontal and vertical ARD grid identifiers.  WARNING:  if no chip identifier is supplied all'
                             ' 726 chips will be processed!')

    args = parser.parse_args()

    if args.hv is None:

        # Loop through all available HV's here

        for hv in all_hv:

            print("\n\tWorking on tile ", hv)

            get_extent = GetExtents(int(hv[0]), int(hv[1]))

            out_dest = args.output + os.sep + "h{h}v{v}".format(h=hv[0], v=hv[1])

            if not os.path.exists(out_dest):

                os.makedirs(out_dest)

            if args.name is None:

            # Loop through all available file names for each tile

                for name in all_names:

                    src_file = args.input + os.sep + name + ".tif"

                    out_file = out_dest + os.sep + name + ".tif"

                    if not os.path.exists(out_file):

                        run_subset(src_file, out_file, get_extent.TILE_EXTENT)

            else:

                src_file = args.input + os.sep + args.name + ".tif"

                out_file = out_dest + os.sep + args.name + ".tif"

                if not os.path.exists(out_file):

                    run_subset(src_file, out_file, get_extent.TILE_EXTENT)

    else:

        get_extent = GetExtents(int(args.hv[0]), int(args.hv[1]))

        out_dest = args.output + os.sep + "h{h}v{v}".format(h=args.hv[0], v=args.hv[1])

        if not os.path.exists(out_dest):

            os.makedirs(out_dest)

        if args.name is None:

            # Loop through all available file names for each tile

            for name in all_names:

                src_file = args.input + os.sep + name + ".tif"

                out_file = out_dest + os.sep + name + ".tif"

                if not os.path.exists(out_file):

                    print("\nProcessing {}\n".format(name))

                    run_subset(src_file, out_file, get_extent.TILE_EXTENT)

        else:

            src_file = args.input + os.sep + args.name + ".tif"

            out_file = out_dest + os.sep + args.name + ".tif"

            if not os.path.exists(out_file):

                run_subset(src_file, out_file, get_extent.TILE_EXTENT)


if __name__ == '__main__':

    main()