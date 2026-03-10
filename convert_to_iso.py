"""
This script converts a NIfTI file to isometric voxels. It uses the nibabel library
to read and write NIfTI files, and scipy.ndimage for resampling the image data.

Functions:
- convert_file: Converts the input NIfTI file to isometric voxels and saves the output file.

Usage:
Run this script from the command line, providing the input NIfTI file and the output file name.

Example:
python convert_to_iso.py input.nii.gz output.nii.gz
"""

import numpy as np
import nibabel as nib
import argparse
import scipy.ndimage as ndimage


def convert_file(inname, outname):
    """
    Convert a NIfTI file to isometric voxels and save the result.

    Parameters:
    inname (str): Path to the input NIfTI file.
    outname (str): Path to the output NIfTI file.
    """
    img = nib.load(inname)
    header = img.header
    img_data = img.get_fdata()
    
    # Check for empty files
    if not np.all(img_data == 0):
        iso_voxels = np.min(header.get_zooms())
        zoom_ratio = np.array(header.get_zooms()) / iso_voxels

        print(f"Zoom ratio: {zoom_ratio}")
        print(f"Original shape: {np.shape(img_data)}")

        data = ndimage.zoom(img_data, zoom=zoom_ratio, order=1)

        print(f"Resampled shape: {np.shape(data)}")

        new_affine = img.affine.copy()
        new_affine[:3, :3] = img.affine[:3, :3] @ np.diag(1.0 / zoom_ratio)
        iso_img = nib.Nifti1Image(data, new_affine, header=img.header)

        nib.save(iso_img, outname)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert a NIfTI file to isometric voxels",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("infile", help="Path to the input NIfTI file (input.nii.gz)")
    parser.add_argument("outfile", help="Path to the output NIfTI file (output.nii.gz)")
    args = parser.parse_args()
    print(f"Input file: {args.infile}")
    print(f"Output file: {args.outfile}")
    convert_file(args.infile, args.outfile)
