import numpy as np

def set_foregroundcolor(ax, color):
    """
    For the specified axes, sets the color of the frame, major ticks,                                                             
    tick labels, axis labels, title and legend                                                                                   
    """
    for tl in ax.get_xticklines() + ax.get_yticklines() + ax.get_xticklabels() + ax.get_yticklabels():
        tl.set_color(color)
    try:
        for tl in ax.get_zticklines() + ax.get_zticklabels():
            tl.set_color(color)
    except AttributeError:
        pass

    for spine in ax.spines:
        ax.spines[spine].set_edgecolor(color)

    for tick in ax.xaxis.get_major_ticks():
        tick.label1.set_color(color)
    for tick in ax.yaxis.get_major_ticks():
        tick.label1.set_color(color)
    try:
        for tick in ax.zaxis.get_major_ticks():
            tick.label1.set_color(color)
    except AttributeError:
        pass

    ax.axes.xaxis.label.set_color(color)
    ax.axes.xaxis.get_offset_text().set_color(color)
    ax.axes.yaxis.label.set_color(color)
    ax.axes.yaxis.get_offset_text().set_color(color)
    try:
        ax.axes.zaxis.label.set_color(color)
        ax.axes.zaxis.get_offset_text().set_color(color)
    except AttributeError:
        pass

    ax.axes.title.set_color(color)
    lh = ax.get_legend()
    if lh != None:
        lh.get_title().set_color(color)
        lh.legendPatch.set_edgecolor('none')
        labels = lh.get_texts()
        for lab in labels:
            lab.set_color(color)

def set_backgroundcolor(ax, color):
    """
    Sets the background color of the current axes (and legend).                                                                   
    Use 'None' (with quotes) for transparent. To get transparent                                                                 
    background on saved figures, use:                                                                                            
    pp.savefig("fig1.svg", transparent=True)                                                                                     
    """
    ax.patch.set_facecolor(color)
    lh = ax.get_legend()
    if lh != None:
        lh.legendPatch.set_facecolor(color)

def scale(w, h, x, y, maximum=True):
    # see http://code.activestate.com/recipes/577575-scale-rectangle-while-keeping-aspect-ratio/
    nw = y * w // h
    nh = x * h // w
    if maximum ^ (nw >= x):
        return nw or 1, y
    return x, nh or 1

def negotiate_panel_size(panels, max_height, margin):
    #calculate sizes of the panels that fit
    for name in panels:
        m = panels[name]
        m['dw'], m['dh'] = scale(
                            m['width'], m['height'],
                            m['device_x1']-m['device_x0'], max_height
        )

    #recalculate the actual sized output
    actual_out_h = np.max([panels[name]['dh'] for name in panels]) + 2*margin
    actual_out_w = np.sum([panels[name]['dw'] for name in panels]) + 2*margin

    return actual_out_w, actual_out_h
