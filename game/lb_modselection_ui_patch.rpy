#provides GUI for mod list editing

init python in lb_mods_util:
    from copy import deepcopy
    opts = renpy.display.screen.screens[("preferences",None)].ast.children
    opts += [deepcopy(opts[1])]
    opts[-1].positional = ['_(u"Модификации")']
    opts[-1].keyword = [(u'action', u'[Function(lb_mods_util.lb__mods_load_allowed),Show("lb__mods_selection_screen")]'), (u'xalign', u'.05'), (u'yalign', u'.93')]

init python:
    style.lb__negabutton = Style(style.button)
    style.lb__negabutton.background = Frame(im.Grayscale("resources/GUI/option_15.png"), 10, 10)
    style.lb__negabutton.hover_background = Frame(im.Grayscale("resources/GUI/option_12.png"), 10, 10)
    style.lb__negabutton.selected_background = Frame(im.Grayscale("resources/GUI/option_14.png"),10,10) 
    style.lb__negabutton_text = Style(style.button_text)

screen lb__mods_selection_screen:
    modal True
    tag menu
    add 'resources/GUI/option_00.png'
    $ adj = NewAdj(step = 300)
    textbutton _("Отмена"):
        action Return()
        xalign .05
        yalign .93
    textbutton _("Применить"):
        action Function(lb_mods_util.lb__mods_dump_allowed)
        xalign .95
        yalign .93
    viewport:
        mousewheel True
        draggable True
        yinitial 1.0
        yadjustment adj
        xfill False
        xalign 0.5
        ypos 0.1
        vbox:
            null:
                height 10
            for id,descr,title in lb_mods_util.lb__mods_get_info():
                textbutton title:
                    if  not id in lb_mods_util.lb__mods_allow_list:
                        style "lb__negabutton"
                    action Function(lb_mods_util.lb__mods_toggle,id)
                null:
                    height 10   
                      