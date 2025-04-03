import sys
import matplotlib.pyplot as plt
from niicat.plotter import plot

print(f"DEBUG: Received sys.argv: {sys.argv}", file=sys.stderr)

iFile = sys.argv[1]
dpi = int(sys.argv[2])
slice_arg = sys.argv[3] if len(sys.argv) > 3 else None
volume_arg = sys.argv[4] if len(sys.argv) > 4 else None

slice_num = int(slice_arg) if slice_arg and slice_arg != "None" else None
volume_num = int(volume_arg) if volume_arg and volume_arg != "None" else None

print(f"DEBUG: Parsed slice_num: {slice_num}", file=sys.stderr)
print(f"DEBUG: Parsed volume_num: {volume_num}", file=sys.stderr)

fig = plot(iFile, return_fig=True, dpi=dpi, slice_num=slice_num, volume_num=volume_num)
plt.savefig(sys.stdout.buffer, dpi=dpi)
