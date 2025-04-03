import sys
import matplotlib.pyplot as plt
from niicat.plotter import plot

iFile = sys.argv[1]
dpi = int(sys.argv[2])
slice_num = int(sys.argv[3]) if len(sys.argv) > 3 and sys.argv[3] else None
volume_num = int(sys.argv[4]) if len(sys.argv) > 4 and sys.argv[4] else None
fig = plot(iFile, return_fig=True, dpi=dpi, slice_num=slice_num, volume_num=volume_num)
plt.savefig(sys.stdout.buffer, dpi=dpi)
