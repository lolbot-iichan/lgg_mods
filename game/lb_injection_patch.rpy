# turns usual RenPy 6.99.12 into mod-selecting RenPy 6.99.12
# looking for file ".lgg_mods.lst" in user's home holder

python early:
    def lb_searchpath_patch_injection():
        if  renpy.version_tuple[:3] != (6,99,12):
            renpy.error("Wrong RenPy version: "+renpy.version_string+". Please, use RenPy 6.99.12.x.")
        
        mainpy = renpy.config.renpy_base+"/renpy/main.py"
        place_line  = None
        continue_line = None
        patch_begin = "#LB_LGG_SEARCHPATH_PATCH_v2\n"
        patch_end   = "#LB_LGG_SEARCHPATH_PATCH_end\n"


        patch       = """#LB_LGG_SEARCHPATH_PATCH_v2
    lb_allowed_mod_names_file = os.path.expanduser("~/.lgg_mods.lst")
    try:
        with open(lb_allowed_mod_names_file,"r") as f:
            lb_allowed_mod_names = [l.strip() for l in f]
    except:
        try:
            open(lb_allowed_mod_names_file,"w").close()
        except:
            pass
        lb_allowed_mod_names = []
    for lb_mods_location in [renpy.config.gamedir+"/../mods/"]:
        if  os.path.exists(lb_mods_location):
            for lb_mod_name in sorted(os.listdir(lb_mods_location)):
                if  not lb_mod_name in lb_allowed_mod_names:
                    continue
                lb_mod_location = os.path.join(lb_mods_location,lb_mod_name)
                lb_mod_descr = os.path.join(lb_mod_location,"descript.ion")
                if  os.path.isdir(lb_mod_location) and os.path.exists(lb_mod_descr):
                    renpy.config.searchpath.append(lb_mod_location)
#LB_LGG_SEARCHPATH_PATCH_end
"""


        with open(mainpy,"r") as f:
            lines = f.readlines()
            for i,line in enumerate(lines):
                if  line == "    renpy.config.searchpath = [ renpy.config.gamedir ]\n":
                    place_line = i
                if  line == patch_end:
                    continue_line = i+1
            if  place_line is None:
                renpy.error("Couldn't find patch line at " + mainpy)
            if  continue_line is None:
                continue_line = place_line+1
    
        if  lines[place_line+1] != patch_begin:
            with open(mainpy,"w") as f:
                for line in lines[:place_line+1]:
                    f.write(line)
                f.write(patch)
                for line in lines[continue_line:]:
                    f.write(line)
            renpy.quit(relaunch=True)

    lb_searchpath_patch_injection()