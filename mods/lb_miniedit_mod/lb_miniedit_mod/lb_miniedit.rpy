init python in lb_registration:
    lb_mods["lb_miniedit_mod_start"] = u"Мини-редактор"

#TEMPORARY UNCOMMENT TO FIX BROKEN SAVE
#init python:
#    persistent.lb__miniedit_slots = None

label lb_miniedit_mod_start:
    python:
        if  persistent.lb__miniedit_slots is None:
            persistent.lb__miniedit_slots = [
                    {
                        "time": "night",
                        "scene": "roma_room night2",
                        "who": "rm",
                        "what": "Ляляля, жужужу, я - фигура Лиссажу.",
                        "show": [
                            {"tag":"kr","sprite":['undress2', 'kind', 'far'],"at":"left"},
                            {"tag":"an","sprite":['sleep', 'panic', 'far'],"at":"right"},
                            {"tag":"st","sprite":['swimtowel', 'genki', 'far'],"at":"center"},
                        ],
                    },
                    {
                        "time": "day",
                        "scene": "sport_indoor day",
                        "who": "oh",
                        "what": "Ты не пройдёшь!",
                        "show": [
                            {"tag":"oh","sprite":['laugh', 'far'],"at":"right"},
                        ],
                    },
                ]
        if  persistent.lb__miniedit_slot is None or persistent.lb__miniedit_slot not in range(len(persistent.lb__miniedit_slots)):
            persistent.lb__miniedit_slot = 0

        lb__miniedit_mode = "edit"
        
        lb__miniedit_idx = 0
        lb__miniedit_upd_time()

        lb__miniedit_time_menu = [("День","day"),("Вечер","evening"),("Ночь","night")]
        
        lb__miniedit_who_menu = [
                (u'Алекса','al'),
                (u'Аня','an'),
                (u'Палпалыч','fi'),
                (u'Кристина','kr'),
                (u'Человек в черном','mib1'),
                (u'Охранник','oh'),
                (u'Садовник','sad'),
                (u'Стася','st'),
                (u'Виктория Сергеевна','vs'),
                (u'Яна','ya'),
                (u'Юра','yu'),
            ]
        
        lb__miniedit_say_menu = [
                (u"Рассказчик","narrator"),
                
                (u'Алекса','al'),
                (u'Аня','an'),
                (u'Палпалыч','fi'),
                (u'Кристина','kr'),
                (u'Человек в черном','mib1'),
                (u'Охранник','oh'),
                (u'Садовник','sad'),
                (u'Стася','st'),
                (u'Виктория Сергеевна','vs'),
                (u'Яна','ya'),
                (u'Юра','yu'),
                (u'Рома','rm'),
                (u'«Кристина»','ky'),
                (u'Голос','vo'),
                (u'Женщина','wo'),
                (u'Девушка','gi'),
                (u'Робот','ro'),
                (u'Отец','ot'),
                (u'Голос 1','vo1'),
                (u'Голос 2','vo2'),
                (u'Голос 3','vo3'),
            ]
        
        lb__miniedit_pos = ["left","center","right"]

    jump lb_miniedit_mod_loop

init python:
    lb__miniedit_change = lambda mode: lambda: [globals().__setitem__("lb__miniedit_mode", mode),True][-1]
    lb__miniedit_change_idx = lambda mode,idx: lambda: [globals().__setitem__("lb__miniedit_mode", mode),globals().__setitem__("lb__miniedit_idx", idx),True][-1]
    lb__miniedit_change_idx_jdx = lambda mode,idx,jdx: lambda: [globals().__setitem__("lb__miniedit_mode", mode),globals().__setitem__("lb__miniedit_idx", idx),globals().__setitem__("lb__miniedit_jdx", jdx),True][-1]

    def lb__miniedit_get(p):
        return persistent.lb__miniedit_slots[persistent.lb__miniedit_slot][p]
    def lb__miniedit_set(p,v):
        persistent.lb__miniedit_slots[persistent.lb__miniedit_slot][p] = v

    def lb__miniedit_upd_time():
        global time
        time = lb__miniedit_get("time")

    def lb__miniedit_button(text=None, clicked=None, width=75, bgcolor=None):
        if  text is not None:
            ui.button(clicked=clicked, xpos=0, xanchor=0.0, ypos=0, xpadding=6, ypadding=-10, xminimum=width, yminimum=30, background=Frame(im.FactorScale("resources/GUI/option_12.png",0.5,0.5),12,12), hover_background=Frame(im.FactorScale("resources/GUI/option_14.png",0.5,0.5),12,12))
            ui.text(text, style="button_text", size=14)
        else:        
            ui.null(width=width)

    def lb__miniedit_export():
        text =  "    $ time = '%s'\n" % lb__miniedit_get("time")
        text += "    scene %s\n" % lb__miniedit_get("scene")
        for id,i in enumerate(lb__miniedit_get("show")):
            n_same = len([x for x in lb__miniedit_get("show")[:id+1] if x["tag"] == i["tag"] ])
            if  n_same == 1:
                text += "    show %s %s at %s\n" % (i["tag"],lb__miniedit_sprite_join(i["sprite"]),i["at"])
            else:
                text += "    show %s %s at %s as %s%d\n" % (i["tag"],lb__miniedit_sprite_join(i["sprite"]),i["at"],i["tag"],n_same)
        if  lb__miniedit_get("who") == "narrator":
            text += "    \"%s\"\n" % (lb__miniedit_get("what"))
        else:
            text += "    %s \"%s\"\n" % (lb__miniedit_get("who"),lb__miniedit_get("what"))
        text += "\n"
        return text

    def lb__miniedit_inner_export():
        text =  " "*20 + "{\n"
        for x in ["time","scene","who","what"]:
            text +=  " "*24 + '"%s": "%s",\n'%(x,lb__miniedit_get(x))
        text +=  " "*24 + '"show": [\n'
        for x in lb__miniedit_get("show"):
            text +=  " "*28 + '{"tag":"%s","sprite":%s,"at":"%s"},\n'%(x["tag"],`x["sprite"]`,x["at"])
        text +=  " "*24 + '],\n' +  " "*20 + '},\n'
        return text

    def lb__miniedit_check_place(s):
        if  s[0] in dict(lb__miniedit_who_menu).values():
            return False
        if  not lb__miniedit_get("time") in `s`:
            return False
        if  "cg_" in s[0]:
            return False
        return True

    def lb__miniedit_check_alive(img):
        if  isinstance(img, renpy.display.im.Image):
            try:
                return all([renpy.loadable(f) for f in img.predict_files()])
            except:
                return False
        if  isinstance(img, renpy.display.im.MatrixColor):
            return lb__miniedit_check_alive(img.image)
        return True
        
    def lb__miniedit_check_sprite(s, tag, conditions):
        if  s[0] != tag:
            return False
        ss = s[1:]
        if len(ss) < len(conditions):
            return False
        for i,c in enumerate(conditions):
            if  ss[i] != c:
                return False        
        return True        

    def lb__miniedit_sprite_join(s):
        return " ".join([i for i in s if i != ""])            
        
label lb_miniedit_mod_loop:
    $ renpy.block_rollback()
    if  lb__miniedit_mode == "edit":
        scene expression (lb__miniedit_get("scene"))
        python:
            for id,i in enumerate(lb__miniedit_get("show")):
                renpy.show(" ".join([i["tag"],lb__miniedit_sprite_join(i["sprite"])]), at_list=[globals()[i["at"]]], tag="tag%d"%id)

        python:
            ui.vbox()
            ui.hbox()
            lb__miniedit_button()
            lb__miniedit_button("time@day")
            lb__miniedit_button(lb__miniedit_get("time"),lb__miniedit_change("time_edit"))
            ui.close()
            ui.hbox()
            lb__miniedit_button()
            lb__miniedit_button("scene")
            lb__miniedit_button(lb__miniedit_get("scene"),lb__miniedit_change("bg_edit"))
            ui.close()
            for i,item in enumerate(lb__miniedit_get("show")):
                ui.hbox()
                lb__miniedit_button("^",lb__miniedit_change_idx("show_up",i) if i!=0 else None,25)
                lb__miniedit_button("X",lb__miniedit_change_idx("show_delete",i),25)
                lb__miniedit_button("v",lb__miniedit_change_idx("show_down",i) if i+1!=len(lb__miniedit_get("show")) else None,25)
                lb__miniedit_button("show")
                lb__miniedit_button(item["tag"])
                for j,s in enumerate(item["sprite"]):
                    lb__miniedit_button(s, lb__miniedit_change_idx_jdx("show_sprite",i,j))
                lb__miniedit_button(width=25)
                lb__miniedit_button("at",width=25)
                lb__miniedit_button("<",lb__miniedit_change_idx("show_at_minus",i) if item["at"] != lb__miniedit_pos[0] else None,25)
                lb__miniedit_button(item["at"])
                lb__miniedit_button(">",lb__miniedit_change_idx("show_at_plus",i) if item["at"] != lb__miniedit_pos[-1] else None,25)
                ui.close()
            ui.hbox()
            lb__miniedit_button()
            lb__miniedit_button("+ show",lb__miniedit_change("show_add"))
            ui.close()
            ui.hbox()
            lb__miniedit_button()
            lb__miniedit_button(lb__miniedit_get("who"),lb__miniedit_change("say_who_edit"))
            lb__miniedit_button(lb__miniedit_get("what"),lb__miniedit_change("say_what_edit"))
            ui.close()
            ui.null(height=20)
            ui.hbox()
            lb__miniedit_button("{b}КОПИЯ{/b}",lb__miniedit_change("clone_slot"))
            for i in range(len(persistent.lb__miniedit_slots)):
                lb__miniedit_button("%d"%i,lb__miniedit_change_idx("load_slot",i) if i != persistent.lb__miniedit_slot else None,29)
            lb__miniedit_button("{b}УДАЛЕНИЕ{/b}",lb__miniedit_change("del_slot") if len(persistent.lb__miniedit_slots)>1 else None)
            ui.close()
            ui.hbox()
            lb__miniedit_button("{b}ЗАПУСК{/b}",lb__miniedit_change("run"))
            lb__miniedit_button("{b}ЭКСПОРТ{/b}",lb__miniedit_change("export"))
            ui.close()
            ui.close()
        $ ui.interact()

    
    else:
        if lb__miniedit_mode == "load_slot":
            $ persistent.lb__miniedit_slot = lb__miniedit_idx
            $ lb__miniedit_upd_time()

        elif lb__miniedit_mode == "clone_slot":
            python:
                import copy
                persistent.lb__miniedit_slots.insert(persistent.lb__miniedit_slot+1, copy.deepcopy(persistent.lb__miniedit_slots[persistent.lb__miniedit_slot]))
                persistent.lb__miniedit_slot += 1
    
        elif lb__miniedit_mode == "del_slot":
            if renpy.display_menu([("Delete current slot?!",None),("Yes",True),("No",False)]):
                python:
                    del persistent.lb__miniedit_slots[persistent.lb__miniedit_slot]
                    if  persistent.lb__miniedit_slot > 0:
                        persistent.lb__miniedit_slot -= 1
                    lb__miniedit_upd_time()
    
        elif lb__miniedit_mode == "run":
            scene expression (lb__miniedit_get("scene"))
            python:
                for id,i in enumerate(lb__miniedit_get("show")):
                    renpy.show(" ".join([i["tag"],lb__miniedit_sprite_join(i["sprite"])]), at_list=[globals()[i["at"]]], tag="tag%d"%id)
                who = globals()[lb__miniedit_get("who")]
                what = lb__miniedit_get("what")
            who "%(what)s"

# not implemented in LGG's renpy
#        elif lb__miniedit_mode == "copy":
#            python:
#                import pygame
#                import pygame.scrap
#                pygame.scrap.init()
#                # TODO экспорт через encode("utf-8") не работает
#                # При pygame.scrap информации в Сети почти нет, в RenPy идёт уже скомпилированная версия
#                # Крайне странный workaround случайно найден тут: http://habrahabr.ru/sandbox/64061
#                pygame.scrap.put("text/plain;charset=utf-8",lb__miniedit_export().encode("utf-16")) 
    
        elif lb__miniedit_mode == "export":
            python:
                import os
                import codecs
                if  not renpy.exists("../mods/scenario_test/scenario_test/test_export.rpy"):
                    try:
                        os.makedirs("mods/scenario_test/scenario_test/")
                    except:
                        pass
                    with codecs.open("mods/scenario_test/descript.ion","w","utf-8") as f:
                        f.write('id=test__export\nversion=1.0\n\n[ru]\ntitle=Тестовый мод\ndescription=Тест тест тест.\ncredits=???\n')
                    with codecs.open("mods/scenario_test/scenario_test/test_export.rpy","w","utf-8") as f:
                        f.write('init python in lb_registration:\n    lb_mods["test__export"] = "test game"\n\nlabel test__export:\n')
                with codecs.open("mods/scenario_test/scenario_test/test_export.rpy","a","utf-8") as f:
                    f.write(lb__miniedit_export()+"\n")
                renpy.exports.say(None, u"Успешно экспортировано в файл: '%s'" % "mods/scenario_test/scenario_test/test_export.rpy")

        elif lb__miniedit_mode == "export_inner":
            python:
                with open("export.txt","a") as f:
                    f.write(lb__miniedit_inner_export().encode("utf-8")+"\n")
                renpy.exports.say(None, u"Успешно экспортировано в файл: '%s'" % "export.txt")
    
        elif lb__miniedit_mode == "time_edit":
            python:
                lb__miniedit_set("time", renpy.display_menu(lb__miniedit_time_menu))
                lb__miniedit_upd_time()
    
        elif lb__miniedit_mode == "bg_edit":
            python:
                renpy.block_rollback()
                keys = [" ".join(i) for i,img in renpy.display.image.images.iteritems() if lb__miniedit_check_place(i) and lb__miniedit_check_alive(img)]

                import math
                n = int(math.ceil(math.sqrt(float(len(keys)))))
                ui.grid(n,n)
                for b in sorted(keys):
                    try:
                        i = im.FactorScale(im.Crop(ImageReference(b),0,0,config.screen_width,config.screen_height),1.0/n)
                        ui.imagebutton(im.MatrixColor(i,im.matrix.saturation(0.3)*im.matrix.contrast(0.3)),i,clicked=ui.returns(b))
                    except:
                        ui.button(clicked=ui.returns(b))
                        ui.text(b)
                for b in range(n*n-len(keys)):
                    ui.null()
                ui.close()
                res = ui.interact()

                lb__miniedit_set("scene", res)
    
        elif lb__miniedit_mode == "show_up":
            $ tmp = lb__miniedit_get("show")[lb__miniedit_idx-1]
            $ lb__miniedit_get("show")[lb__miniedit_idx-1] = lb__miniedit_get("show")[lb__miniedit_idx]
            $ lb__miniedit_get("show")[lb__miniedit_idx] = tmp
    
        elif lb__miniedit_mode == "show_delete":
            $ del lb__miniedit_get("show")[lb__miniedit_idx]
    
        elif lb__miniedit_mode == "show_down":
            $ tmp = lb__miniedit_get("show")[lb__miniedit_idx+1]
            $ lb__miniedit_get("show")[lb__miniedit_idx+1] = lb__miniedit_get("show")[lb__miniedit_idx]
            $ lb__miniedit_get("show")[lb__miniedit_idx] = tmp
    
        elif lb__miniedit_mode == "show_sprite":
            $ tmp = lb__miniedit_get("show")[lb__miniedit_idx]
            $ avaliable = [[] if len(i)==1 else i[1:] for i in renpy.display.image.images if lb__miniedit_check_sprite(i,tmp["tag"],tmp["sprite"][:lb__miniedit_jdx])]
            $ next_words = sorted(list(set([ "" if len(x)<=lb__miniedit_jdx else x[lb__miniedit_jdx] for x in avaliable ])))
            if  len(next_words) > 1 or (len(next_words) == 1 and next_words[0] != ""):
                if  len(next_words) > 1:
                    $ q = "show " + lb__miniedit_get("show")[lb__miniedit_idx]["tag"] + lb__miniedit_sprite_join(tmp["sprite"][:lb__miniedit_jdx]+["..."])
                    $ lb__miniedit_get("show")[lb__miniedit_idx]["sprite"] = tmp["sprite"][:lb__miniedit_jdx] + [renpy.display_menu([(q,None)]+[('+ "'+w+'"',w) for w in next_words])]
                else:
                    $ lb__miniedit_get("show")[lb__miniedit_idx]["sprite"] = tmp["sprite"][:lb__miniedit_jdx] + [next_words[0]]               
                $ lb__miniedit_jdx += 1
                $ lb__miniedit_mode = "show_sprite"
                jump lb_miniedit_mod_loop
            else:
                $ lb__miniedit_get("show")[lb__miniedit_idx]["sprite"][:lb__miniedit_jdx]
    
        elif lb__miniedit_mode == "show_at_minus":
            $ lb__miniedit_get("show")[lb__miniedit_idx]["at"] = lb__miniedit_pos[lb__miniedit_pos.index(lb__miniedit_get("show")[lb__miniedit_idx]["at"])-1]
    
        elif lb__miniedit_mode == "show_at_plus":
            $ lb__miniedit_get("show")[lb__miniedit_idx]["at"] = lb__miniedit_pos[lb__miniedit_pos.index(lb__miniedit_get("show")[lb__miniedit_idx]["at"])+1]
    
        elif lb__miniedit_mode == "show_add":
            python:
                lb__miniedit_idx = len(lb__miniedit_get("show"))
                tmp = {}
                tmp["tag"] = renpy.display_menu(lb__miniedit_who_menu)
                renpy.block_rollback()
                tmp["sprite"] = []
                tmp["at"] = "center"
                lb__miniedit_set("show", lb__miniedit_get("show")+[tmp])
                lb__miniedit_jdx = 0 
                lb__miniedit_mode = "show_sprite"
            jump lb_miniedit_mod_loop                
    
        elif lb__miniedit_mode == "say_who_edit":
            python:
                ui.hbox(xalign=0.5, yalign=0.5)
                for r,x in [
                        (range(0, (len(lb__miniedit_say_menu)+1)/3), 0.25), 
                        (range((len(lb__miniedit_say_menu)+1)/3, 2*(len(lb__miniedit_say_menu)+1)/3), 0.5), 
                        (range(2*(len(lb__miniedit_say_menu)+1)/3, len(lb__miniedit_say_menu)), 0.75)
                    ]:
                    ui.vbox()
                    for idx,i in enumerate(r):
                        img = Fixed(Text(lb__miniedit_say_menu[i][0], xalign=0.5, yalign=0.5, color=(0,0,0,255)), xmaximum=260)
                        imga = Fixed(Text(lb__miniedit_say_menu[i][0], xalign=0.5, yalign=0.5, color=(0,0,0,110)), xmaximum=260)
                        bgim = Fixed(Frame("resources/GUI/option_14.png",100,17), xmaximum=260, ymaximum=35)
                        bgima = Fixed(Frame("resources/GUI/option_12.png",100,17), xmaximum=260, ymaximum=35)
                        bg = Fixed(bgim, xmaximum=286)
                        bga = Fixed(bgima, xmaximum=286)
                        this_idle = LiveComposite((286,35),
                                                      (13,0), bga,
                                                      (13,0), imga
                                                      )
                        this_hover = LiveComposite((286,35),
                                                      (13,0), bg,
                                                      (13,0), img
                                                      )
                        ui.fixed(xpos=0.5, ymaximum=35, xmaximum=266)
                        ui.imagebutton(this_idle, this_hover, clicked=ui.returns(lb__miniedit_say_menu[i][1]), style="default", xanchor=0.5, yanchor=0.5)
                        ui.close()
                    ui.close()
                ui.close()
                lb__miniedit_set("who", ui.interact())
    
        elif lb__miniedit_mode == "say_what_edit":
            $ lb__miniedit_set("what", renpy.input("What to say:",lb__miniedit_get("what")))
    
        else:
            $ renpy.error(("Unknown mode",lb__miniedit_mode))

        $ lb__miniedit_mode = "edit"

    jump lb_miniedit_mod_loop
