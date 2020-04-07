from __future__ import print_function
import tempfile

from benu.benu import Canvas
from benu.utils import set_foregroundcolor, set_backgroundcolor

import tempfile

tmp_fname = tempfile.mktemp(".png")
canv = Canvas(tmp_fname, 500, 500)
device_rect = (100, 100, 300, 300)
ux0 = 0
uy0 = 0
uw = 50
uh = 50
ux1 = ux0 + uw
uy1 = uy0 + uh
user_rect = (ux0, uy0, uw, uh)

# transform = 'rot 10'
transform = "rot -45"
# transform = 'orig'
pts = [
    (0, 0),
    (5, 5),
    (30, 30),
    (45, 45),
    (1, 3),
    (6, 2),
]

# test the with statement using as
with canv.set_user_coords(device_rect, user_rect, transform=transform) as canv2:
    for pt in pts:
        canv2.scatter([pt[0]], [pt[1]])

    # draw red boundary in user coords
    canv2.plot(
        [ux0, ux0, ux1, ux1, ux0], [uy0, uy1, uy1, uy0, uy0], color_rgba=(1, 0, 0, 1)
    )

# test the with statement (not using as)
with canv.set_user_coords(device_rect, user_rect, transform=transform):
    for pt in pts:
        canv.scatter([pt[0]], [pt[1]], radius=0.5, color_rgba=(0.2, 0.2, 0.6, 0.5))

if 1:
    # draw boundary of above coord system
    canv.plot(
        [
            device_rect[0],
            device_rect[0],
            device_rect[0] + device_rect[2],
            device_rect[0] + device_rect[2],
            device_rect[0],
        ],
        [
            device_rect[1],
            device_rect[1] + device_rect[3],
            device_rect[1] + device_rect[3],
            device_rect[1],
            device_rect[1],
        ],
        color_rgba=(0, 0.5, 0, 1),
    )  # dark green

# draw blue star
canv.poly(
    [0, 50, 100, 0, 100, 0],
    [100, 0, 100, 50, 50, 100],
    color_rgba=(0, 0, 1, 1),
    edgewidth=5,
)


for pt in pts:
    x, y = canv.get_transformed_point(
        pt[0], pt[1], device_rect, user_rect, transform=transform
    )
    canv.text("%s, %s" % (pt[0], pt[1]), x, y)
canv.save()

# this test is broken...
## with c.set_user_coords(1,2):
##     pass

print(tmp_fname)
