from convert_to_iso import convert_file
from totalsegmentator.python_api import totalsegmentator, class_map
from niigz_to_obj import convert_nii_to_obj
import argparse
import os
licensenum = 'aca_JY39RTTVQPDJ4G'


# pipeline is segment, split masks, convert to iso, iso to obj
def nii2obj(indir, outdir, task="total"):
    print(indir)
    for filename in os.listdir(indir):
        print(filename)
        infile = os.path.join(indir, filename)
        if infile.endswith(".nii.gz") or infile.endswith(".nii"):
            totalsegmentator(infile, outdir, task=task, license_number=licensenum)

    for filename in os.listdir(outdir):
        print(filename)
        infile = os.path.join(outdir, filename)
        base_name = os.path.splitext(os.path.basename(infile))[0]
        base_name = os.path.splitext(os.path.basename(base_name))[0]

        print(base_name)
        base_name = os.path.join(outdir, base_name)
        print(base_name)
        iso_name = base_name + "_iso.nii.gz"
        convert_file(infile, iso_name)
        if os.path.exists(iso_name):
            convert_nii_to_obj(iso_name, base_name + ".obj")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="convert a nifti file to isometric",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("infile", help="nii.gz file")
    parser.add_argument("outfile", help="output.nii.gz")
    parser.add_argument("task", help="task to segment")
    args = parser.parse_args()
    print(args.infile, args.outfile)
    nii2obj(args.infile, args.outfile, args.task)
