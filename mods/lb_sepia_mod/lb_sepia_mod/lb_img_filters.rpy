init 9999 python in lb_sepia_mod:
    import re
    from renpy.store import im
    from renpy.store import config
    from renpy.store import style
    from renpy.store import Style

    def lb__sepia_wrap(str):
        str = str.replace("4964a3","a0a0a0")
        if  not ".png" in str and not ".jpg" in str:
            return str
        if  "im.Sepia" in str:
            return str
        str = re.sub("('.*\.[jp][pn]g')","im.Sepia(\\1)",str)
        if  "im.Sepia" in str:
            return str
        return re.sub('(".*\.[jp][pn]g")',"im.Sepia(\\1)",str)

    def lb__recolor_scr(ch, im_op, wr):
        if  "positional" in dir(ch):
            ch.positional = [wr(v) for v in ch.positional]
        if  "keyword" in dir(ch):
            ch.keyword = [(k,wr(v)) for (k,v) in ch.keyword]

        if  "children" in dir(ch):
            for c in ch.children:
                lb__recolor_scr(c, im_op, wr)
        if  "entries" in dir(ch):
            for cnd,c in ch.entries:
                lb__recolor_scr(c, im_op, wr)

    def lb__recolor(im_op, wr):
        fail_list = []
        for id, img in renpy.display.image.images.iteritems():
            try:
                for i,(c,sub) in enumerate(img.child.args[0]):
                    img.child.args[0][i] = (c,im_op(sub))
            except:
                try:
                    renpy.display.image.images[id] = im_op(img)
                except:
                    try:
                        img.child = im_op(img.child)
                    except:
                        try:
                            for i,st in enumerate(img.atl.statements):
                                if  "expressions" in `dir(st)`:
                                    img.atl.statements[i].expressions = [tuple(wr(x) for x in v) for v in st.expressions]
                        except:
                            if  id[0] == "title":
                                raise
                            fail_list += [(`img`," ".join(id))]

        for id in renpy.style.styles:
            if  len(id) == 1 and "Frame" in `type(getattr(style,id[0]).background)`:
                try:
                    getattr(style,id[0]).background.image = im_op(getattr(style,id[0]).background.image)
                except:
                    fail_list += [(`getattr(style,id[0])`," ".join(id))]

        style.default.outlines = [(2, "#727272b3", 0, 0)]

        for id, scr in renpy.display.screen.screens.iteritems():
            for ch in scr.ast.children:
                lb__recolor_scr(ch, im_op, wr)

#        if  fail_list:
#            renpy.error("\n".join([`len(fail_list)`]+[`i` for i in fail_list]))        

    lb__recolor(im.Sepia, lb__sepia_wrap)

    config.overlay_functions.append(lambda:ui.image("lb_sepia_mod/sepia.png"))
    