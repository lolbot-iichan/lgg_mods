init -1000 python in lb_codeline_widget_mod:
    from renpy.store import config
    from renpy.store import ui
    import os

    def editoverlay():
        fullfn, line = renpy.get_filename_line()
        ui.button(clicked=None, xpos=config.screen_width, xanchor=1.0, ypos=2, xpadding=6, xminimum=200)
        ui.text("%s:%d" % (os.path.basename(fullfn), line), style="button_text", size=14)
    config.overlay_functions.append(editoverlay)
