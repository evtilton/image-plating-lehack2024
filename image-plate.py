import argparse
import time
from PIL import Image
import matplotlib.pyplot as plt
from scipy import optimize
import numpy as np
from tqdm import trange
from math import sqrt
from datetime import datetime
from numba import jit
from numba.core.types.scalars import Boolean

parser = argparse.ArgumentParser(description="morph one image into another")
parser.add_argument("filler_img", help="use this image as the filler image")
parser.add_argument("skeleton_img",
                    help="use this image as the skeleton image")
parser.add_argument("-p",
                    "--precision",
                    default=5000,
                    help="specify level of pixelation in output",
                    type=int)
parser.add_argument("-v",
  "--vivid",
  default=False,
  help="vivid?",
  type=Boolean)
args = parser.parse_args()

print("initializing..")

skel_img = Image.open("input/" + args.skeleton_img)
fill_img = Image.open("input/" + args.filler_img)
dims = skel_img.size
xres, yres = skel_img.info['dpi']
fill_img = fill_img.resize(dims)
skel_arr = np.asarray(skel_img)
fill_arr = np.asarray(fill_img)
rows, cols, _ = skel_arr.shape

## bipartite matching problem 

precision = args.precision
total_pixels = skel_arr.size

O = int(sqrt(total_pixels / precision))
r = rows // O
c = cols // O

tic = time.time()
cost_matrix = np.empty((r, c, r, c))

print("finding optimal matching.. MEAN")

for i in trange(r):
  for j in trange(c, leave=False):
    avg_skel = np.average(skel_arr[i * O:i * O + O, j * O:j * O + O],
                          axis=(0, 1))
    for i2 in range(r):
      for j2 in range(c):
        avg_fill = np.average(fill_arr[i2 * O:i2 * O + O, j2 * O:j2 * O + O],
                              axis=(0, 1))
        cost_matrix[i, j, i2, j2] = np.linalg.norm(avg_fill - avg_skel)

toc = time.time()
print(toc - tic, "EXEC")

# body of loop ended
# post loop

temp = cost_matrix.reshape(r, c,
                           r * c).transpose(2, 0,
                                            1).reshape(r * c,
                                                       r * c).transpose(1, 0)
_, col_ind = optimize.linear_sum_assignment(temp)
coords = col_ind.reshape(r, c)

# had to manually change third from 3 to 4 to match shape of final arr
print(rows, cols)

@jit(nopython=True)
def body():
  final_arr = np.full((rows, cols, 4), 255, dtype=int)
  
  for i in range(r):
    for j in range(c):
      temp = coords[i, j]
      i2 = temp // c
      j2 = temp % c
  
      #rand = random.random()*100
      final_arr[i * O:i * O + O,
      j * O:j * O + O] = fill_arr[i2 * O:i2 * O + O,
                                  j2 * O:j2 * O + O].copy()
  return final_arr


## If user only wants the final frame, save it to disk and exit program. ##
final_arr = np.full((rows, cols, 4), 255, dtype=int)
if args.vivid:
  final_arr = body()
else:
  for i in range(r):
    for j in range(c):
      temp = coords[i, j]
      i2 = temp // c
      j2 = temp % c

      final_arr[i * O:i * O + O,
      j * O:j * O + O] = fill_arr[i2 * O:i2 * O + O,
                                  j2 * O:j2 * O + O].copy()

plt.figure(figsize=(rows / yres, cols / xres))
plt.imshow(final_arr)
datetime_obj = datetime.now()
timestamp = datetime_obj.strftime("%Y-%m-%d_%H-%M-%S")
output_filename = "pixel-shuffle_" + timestamp + ".png"

plt.gca().set_axis_off()
plt.subplots_adjust(top=1, bottom=0, right=1, left=0)
plt.savefig(output_filename,
            transparent=True,
            bbox_inches='tight',
            pad_inches=0)

print("done")
