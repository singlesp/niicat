#!/usr/bin/env python

import os
import argparse
import time
import platform
import nibabel as nb
from niicat.plotter import plot, _is_nifti_file
from importlib.metadata import files, version
from importlib.resources import files as resource_files
import sys


def is_executable(name):
    """Check whether `name` is on PATH and marked as executable."""
    from shutil import which

    return which(name) is not None


def main():
    parser = argparse.ArgumentParser(
        description="Generate previews of nifti image and png/jpeg images "
        + "on the terminal.",
        epilog="Written by Jakob Wasserthal",
    )
    parser.add_argument("nifti_file")
    parser.add_argument(
        "-ls",
        action="store_true",
        help="Use libsixel-python instead of iTerm2's imgcat to plot the image.",
        default=False,
    )
    parser.add_argument(
        "-lb",
        action="store_true",
        help="Use libsixel-bin instead of iTerm2's imgcat to plot the image.",
        default=False,
    )
    parser.add_argument(
        "-d",
        "--dpi",
        metavar="N",
        type=int,
        help="resolution for plotting (default: 200).",
        default=200,
    )
    parser.add_argument(
        "-s",
        "--slice",
        metavar="N",
        type=int,
        help="slice number to show (0-indexed, default: middle slice)",
        default=None,
    )
    parser.add_argument(
        "-v",
        "--volume",
        metavar="N",
        type=int,
        help="volume number to show for 4D data (0-indexed, default: middle volume)",
        default=None,
    )
    parser.add_argument(
        "--movie",
        action="store_true",
        help="Display all volumes of a 4D image sequentially as a movie.",
        default=False,
    )
    parser.add_argument("--version", action="version", version=version("niicat"))
    args = parser.parse_args()

    niicat_files = resource_files("niicat.resources")
    clear_cmd = "cls" if platform.system() == "Windows" else "clear"

    if not _is_nifti_file(args.nifti_file):
        # Handle non-nifti files (no movie mode possible)
        if args.movie:
            print(
                "ERROR: --movie flag can only be used with NIfTI files.",
                file=sys.stderr,
            )
            sys.exit(1)
        if args.ls:  # Assuming libsixel works for non-nifti via plot directly
            plot(args.nifti_file, dpi=args.dpi)  # Slice/Volume not relevant
        else:  # Fallback to imgcat for non-nifti likely needs specific handling or fails
            print(
                "ERROR: Plotting non-NIfTI files without -ls is not fully supported.",
                file=sys.stderr,
            )  # Or attempt generic imgcat
            # Potentially add generic os.system call here if desired
            return  # Exit after plotting non-nifti

    # --- NIfTI File Handling ---
    if args.movie:
        try:
            img = nb.load(args.nifti_file)
            if img.header["dim"][0] != 4:
                print("ERROR: --movie flag requires a 4D NIfTI image.", file=sys.stderr)
                sys.exit(1)
            num_volumes = img.shape[3]
        except Exception as e:
            print(f"ERROR: Could not load NIfTI file header: {e}", file=sys.stderr)
            sys.exit(1)

        for vol_idx in range(num_volumes):
            os.system(clear_cmd)  # Clear screen before each frame
            print(f"Displaying Volume {vol_idx + 1}/{num_volumes}")  # Show progress
            if args.ls:
                plot(
                    args.nifti_file,
                    dpi=args.dpi,
                    slice_num=args.slice,
                    volume_num=vol_idx,
                )
            elif args.lb:
                niipre_path = str(niicat_files / "niipre_to_buffer.py")
                imgcat_path = "img2sixel"
                if is_executable(imgcat_path):
                    os.system(
                        "python "
                        + niipre_path
                        + " "
                        + args.nifti_file
                        + " "
                        + str(args.dpi)
                        + " "
                        + str(args.slice if args.slice is not None else "None")
                        + " "
                        + str(vol_idx)  # Use current loop volume index
                        + " | "
                        + imgcat_path
                    )
                else:
                    print(
                        "ERROR: the command 'img2sixel' is not available in your PATH. "
                        + "Install libsixel-bin to make it available.",
                        file=sys.stderr,
                    )
                    break  # Exit loop if command fails
            else:
                niipre_path = str(niicat_files / "niipre_to_buffer.py")
                imgcat_path = str(niicat_files / "imgcat.sh")
                os.system(
                    "python "
                    + niipre_path
                    + " "
                    + args.nifti_file
                    + " "
                    + str(args.dpi)
                    + " "
                    + str(args.slice if args.slice is not None else "None")
                    + " "
                    + str(vol_idx)  # Use current loop volume index
                    + " | "
                    + imgcat_path
                )
            time.sleep(0.1)  # Delay between frames (adjust as needed)
    else:
        # --- Original Single Frame Logic ---
        if args.ls:
            plot(
                args.nifti_file,
                dpi=args.dpi,
                slice_num=args.slice,
                volume_num=args.volume,
            )
        elif args.lb:
            niipre_path = str(niicat_files / "niipre_to_buffer.py")
            imgcat_path = "img2sixel"
            if is_executable(imgcat_path):
                os.system(
                    "python "
                    + niipre_path
                    + " "
                    + args.nifti_file
                    + " "
                    + str(args.dpi)
                    + " "
                    + str(args.slice if args.slice is not None else "None")
                    + " "
                    + str(args.volume if args.volume is not None else "None")
                    + " | "
                    + imgcat_path
                )
            else:
                print(
                    "ERROR: the command 'img2sixel' is not available in your PATH. "
                    + "Install libsixel-bin to make it available.",
                    file=sys.stderr,
                )
        else:
            niipre_path = str(niicat_files / "niipre_to_buffer.py")
            imgcat_path = str(niicat_files / "imgcat.sh")
            os.system(
                "python "
                + niipre_path
                + " "
                + args.nifti_file
                + " "
                + str(args.dpi)
                + " "
                + str(args.slice if args.slice is not None else "None")
                + " "
                + str(args.volume if args.volume is not None else "None")
                + " | "
                + imgcat_path
            )


if __name__ == "__main__":
    main()
