from __future__ import print_function
import tempfile
import scipy.misc
import numpy as np

from benu.benu import Canvas
from benu.utils import (
    set_foregroundcolor,
    set_backgroundcolor,
    negotiate_panel_size,
    get_panel_rects,
)

TARGET_OUT_W, TARGET_OUT_H = 1024, 768
MARGIN = 0

# full size lena
lena = scipy.misc.lena().astype(np.uint8)
# 160px lena
iw = 160
ih = 160
ilena = lena[200 : 200 + ih, 200 : 200 + iw]

# define the panels maximum size
panels = {}
panels["lena"] = dict(
    width=lena.shape[1],
    height=lena.shape[0],
    device_x0=MARGIN,
    device_x1=0.5 * TARGET_OUT_W - MARGIN // 2,
    device_y0=MARGIN,
    device_y1=TARGET_OUT_H - MARGIN,
)
panels["plot"] = dict(
    width=500,
    height=400,
    device_x0=0.5 * TARGET_OUT_W + MARGIN // 2,
    device_x1=1.0 * TARGET_OUT_W - MARGIN // 2,
    device_y0=MARGIN,
    device_y1=TARGET_OUT_H - MARGIN,
)
actual_out_w, actual_out_h = negotiate_panel_size(panels)

tmp_fname = tempfile.mktemp(".png")

canv = Canvas(tmp_fname, actual_out_w, actual_out_h)
canv.poly(
    [0, 0, actual_out_w, actual_out_w, 0],
    [0, actual_out_h, actual_out_h, 0, 0],
    color_rgba=(0, 0, 0, 1),
)

# big lena
p = panels["lena"]
device_rect, user_rect = get_panel_rects(p)
with canv.set_user_coords(device_rect, user_rect):
    canv.imshow(lena, 0, 0, filter="best")
    # in pixel coordinates!
    xpx = np.arange(50, 150)
    ypx = (np.sin(xpx) * 100) + 150
    canv.plot(xpx, ypx, color_rgba=(1, 0, 0, 1))

# draw 1/4 size lena in bottom left
device_rect = (0, actual_out_h - (ih // 4), iw // 4, ih // 4)
user_rect = (0, 0, ilena.shape[1], ilena.shape[0])
with canv.set_user_coords(device_rect, user_rect):
    canv.imshow(ilena, 0, 0, filter="best")
    # in pixel coordinates
    col = 20
    row = 80
    canv.scatter(
        [col], [row], color_rgba=(0.4, 0, 0.6, 0.8), radius=6, markeredgewidth=5
    )


# plot
p = panels["plot"]
device_rect, user_rect = get_panel_rects(p)
with canv.set_user_coords(device_rect, user_rect):
    with canv.get_figure(user_rect) as fig:
        ax = fig.add_subplot(111)
        ax.plot([5, 7, 10], [5, 7, 10], "r-")
        set_foregroundcolor(ax, "white")
        set_backgroundcolor(ax, "black")
        fig.patch.set_facecolor("none")

# inset lena on bottom right hand corner of plot
p = panels["plot"]
device_rect = (p["device_x0"] + p["dw"] - iw, p["device_y0"] + p["dh"] - ih, iw, ih)
user_rect = (0, 0, ilena.shape[1], ilena.shape[0])
with canv.set_user_coords(device_rect, user_rect):
    canv.imshow(ilena, 0, 0, filter="best")
    # in pixel coordinates
    col = 20
    row = 80
    canv.scatter(
        [col], [row], color_rgba=(0.4, 0, 0.6, 0.8), radius=6, markeredgewidth=5
    )

canv.save()
print(tmp_fname)
