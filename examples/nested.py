from __future__ import print_function
import tempfile
import random
import matplotlib.pyplot as plt

from benu.benu import Canvas

OUTER = 500

# ---------

cm = plt.get_cmap("jet")
outer = OUTER

tmp_fname = tempfile.mktemp(".png")
canv = Canvas(tmp_fname, OUTER, OUTER)

while outer > 10:
    device_rect = (0, 0, outer, outer)
    user_rect = (0, 0, outer, outer)
    with canv.set_user_coords(device_rect, user_rect):
        canv.poly(
            [0, 0, outer, outer, 0],
            [0, outer, outer, 0, 0],
            color_rgba=cm(random.randrange(0, cm.N)),
        )
    outer = outer // 2

canv.save()
print(tmp_fname)
