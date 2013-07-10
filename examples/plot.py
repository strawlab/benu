import tempfile

from benu.benu import Canvas
from benu.utils import set_foregroundcolor, set_backgroundcolor
 
tmp_fname = tempfile.mktemp('.png')
canv = Canvas(tmp_fname,500,500)
with canv.get_figure(500,500) as fig:
    ax = fig.add_subplot(111)
    ax.plot( [5,7,10], [5,7,10], 'r-' )
    ax.set_xlabel('Xlabel')
    ax.set_ylabel('Ylabel')
    fig.patch.set_facecolor('none')

canv.save()
print tmp_fname

