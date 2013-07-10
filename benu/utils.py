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

def sorted_left_to_right(panels):
    return [k for k,v in sorted(panels.items(), key=lambda x: x[1]['device_x0'])]

def _check_panels(panels):
    REQUIRED = ("width","height","device_x0","device_x1",
                "device_y0","device_y1")
    for n,p in panels.items():
        for k in REQUIRED:
            if k not in p:
                raise ValueError("Panel %s missing value %s" % (n,k))

def get_panel_rects(p):
    device_rect = (p["device_x0"], p["device_y0"], p["dw"], p["dh"])
    user_rect = (0,0,p["width"],p["height"])

    return device_rect, user_rect

def negotiate_panel_size(panels, max_height=None, margin=0):
    _check_panels(panels)

    if max_height is None:
        max_height = np.max([panels[name]['device_y1'] for name in panels])

    #calculate sizes of the panels that fit
    for name in panels:
        m = panels[name]
        nw, nh = scale(
                    m['width'], m['height'],
                    m['device_x1']-m['device_x0'], max_height
        )
        m['dw'], m['dh'] = nw, nh

    #recalculate the actual sized output
    actual_out_h = np.max([panels[name]['dh'] for name in panels]) + 2*margin
    actual_out_w = np.sum([panels[name]['dw'] for name in panels]) + 2*margin

    return actual_out_w, actual_out_h

def negotiate_panel_size_same_height(panels, max_width, margin):
    _check_panels(panels)

    #increase the size of all individual boxes until the total width does not
    #exceed max_width
    ch = 0
    while (not ch) or (tw < max_width):
        widths = []
        for name in panels:
            m = panels[name]
            widths.append( scale(m['width'], m['height'],1e9,ch)[0] )
        ch += 1
        tw = np.sum(widths)

    #calculate sizes of the panels that fit
    for name in panels:
        m = panels[name]
        nw, nh = scale(
                    m['width'], m['height'],
                    1e9, ch-1
        )
        m['dw'], m['dh'] = nw, nh

    #adjust starting x
    x = None
    for name in sorted_left_to_right(panels):
        m = panels[name]
        if x is None:
            x = m['device_x0']
            x += m['dw']
            continue

        m['device_x0'] = x
        x += m['dw']

    #recalculate the actual sized output
    actual_out_h = np.max([panels[name]['dh'] for name in panels])
    actual_out_w = np.sum([panels[name]['dw'] for name in panels])

    return actual_out_w, actual_out_h

if __name__ == "__main__":
    from pprint import pprint

    TARGET_OUT_W, TARGET_OUT_H = 1024, 768
    MARGIN = 0

    target_out_w = TARGET_OUT_W
    target_out_h = TARGET_OUT_H
    device_y0 = MARGIN
    device_y1 = target_out_h-MARGIN
    max_height = device_y1-device_y0
    max_width = TARGET_OUT_W

    for fmf,dsc in [((659,494),(1024,768)),((1920,1080),(1024,768))]:
        fmfwidth,fmfheight = fmf
        dscwidth,dscheight = dsc

        panels = {}
        panels["mov"] = dict(
            width = fmfwidth,
            height = fmfheight,
            device_x0 = MARGIN,
            device_x1 = target_out_w//2 - MARGIN//2,
            device_y0 = MARGIN,
            device_y1 = target_out_h-MARGIN
        )
        panels["dsc"] = dict(
            width = dscwidth,
            height = dscheight,
            device_x0 = target_out_w//2 + MARGIN//2,
            device_x1 = target_out_w - MARGIN//2,
            device_y0 = MARGIN,
            device_y1 = target_out_h-MARGIN
        )

        hpanels = panels.copy()
        wpanels = panels.copy()

        actual_out_w, actual_out_h = negotiate_panel_size_same_height(panels, max_width, MARGIN)
        print "SAME HEIGHT MOVIE SIZE", actual_out_w, actual_out_h
        pprint(hpanels)

        actual_out_w, actual_out_h = negotiate_panel_size(wpanels, max_height, MARGIN)
        print "MAX WIDTH MOVIE SIZE", actual_out_w, actual_out_h
        pprint(wpanels)


