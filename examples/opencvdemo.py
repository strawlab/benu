import cv2
import numpy as np

from benu.benu import NumpyArrayCanvas

canv = NumpyArrayCanvas(640, 480)
with canv.get_fullsize_figure() as fig:
    ax = fig.add_subplot(111)
    ax.plot([5, 7, 10], [5, 7, 10], "g-", label="green")
    ax.plot(range(10), range(10), "b*", label="blue")
    ax.plot(range(10, 0, -1), range(10), "r^", label="red")
    ax.set_xlabel("Xlabel")
    ax.set_ylabel("Ylabel")
    ax.legend()

raw = canv.as_cv2()
cv2.imshow("test", raw)
cv2.waitKey(0)
