#provides interface for mod list editing
# looking for file ".lgg_mods.lst" in user's home holder

init python in lb_mods_util:
    lb__mods_allow_list = []

    def lb__mods_toggle(id):
        global lb__mods_allow_list
        if  id in lb__mods_allow_list:
            lb__mods_allow_list.remove(id)
        else:
            lb__mods_allow_list.append(id)
        
    import os, codecs

    def lb__mods_load_allowed():
        global lb__mods_allow_list
        try:
            with codecs.open(os.path.expanduser("~/.lgg_mods.lst"),"r","utf-8") as f:
                lb__mods_allow_list = [l.strip() for l in f]
        except:
            lb__mods_allow_list = []

    def lb__mods_dump_allowed():
        global lb__mods_allow_list
        try:
            with codecs.open(os.path.expanduser("~/.lgg_mods.lst"),"w","utf-8") as f:
                for it in lb__mods_allow_list:
                    f.write(it+"\n")
        except:
            pass
        renpy.quit(relaunch=True)            

    def lb__mods_parse_descr(path):
        try:
            fname = os.path.join(path,"descript.ion")
            with codecs.open(fname,"r","utf-8") as f:
                result = {}
                cur_section = None
                for line in f.readlines():
                    line = line.strip()
                    if  line and line[0]=="[" and line[-1]=="]":
                        cur_section = line[1:-1]
                    if  "=" in line:
                        k,v = line[:line.find("=")], line[line.find("=")+1:].replace("\\n","\n")
                        if  cur_section is None or cur_section == "ru":
                            result[k]=v
                return result
        except:
            return {}

    def lb__mods_get_info():
        result = []
        for lb_mods_location_x in ["../mods/","../../../workshop/content/542260"]:
            lb_mods_location = renpy.config.gamedir + "/" + lb_mods_location_x
            if  os.path.exists(lb_mods_location):
                for id in sorted(os.listdir(lb_mods_location)):
                    path = os.path.join(lb_mods_location,id)
                    descr = lb__mods_parse_descr(path)
                    title = id
                    if  "title" in descr:
                        title = descr["title"]
                    if  "credits" in descr:
                        title = "[" + descr["credits"] + "] " + title
                    result.append((id,descr,title.replace("[","[[").replace("{","{{")))
        return result
