import sys
import matplotlib.pyplot as plt
from niicat.plotter import plot

print(f"DEBUG: Received sys.argv: {sys.argv}", file=sys.stderr)

iFile = sys.argv[1]
dpi = int(sys.argv[2])
slice_num = int(sys.argv[3]) if len(sys.argv) > 3 and sys.argv[3] else None
volume_num = int(sys.argv[4]) if len(sys.argv) > 4 and sys.argv[4] else None

print(f"DEBUG: Parsed slice_num: {slice_num}", file=sys.stderr)
print(f"DEBUG: Parsed volume_num: {volume_num}", file=sys.stderr)

fig = plot(iFile, return_fig=True, dpi=dpi, slice_num=slice_num, volume_num=volume_num)
plt.savefig(sys.stdout.buffer, dpi=dpi)
