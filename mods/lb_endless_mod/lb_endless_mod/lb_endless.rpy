init python in lb_registration:
    lb_mods["lb_endless_mod_start"] = u"Бесконечный сценарий"
    
init 9999 python in lb_endless_mod:
    lgg_character_list =  ["al","an","kr","st","ya","yu"]
    from renpy.store import al,  an,  kr,  st,  ya,  yu,  rm

init python in lb_endless_mod:
    from renpy.store import ImageReference
    import codecs

    __DEPTH__ = 2
    __MINLEN__ = 2    
    __SENTANCES__ = 2

    Empty = ""
    KeySeparator = "#"

    def start_key():
        if  __DEPTH__ == 1:
            return Empty
        return Empty + (KeySeparator+Empty)*(__DEPTH__-1)

    def next_key(key,word):
        if  __DEPTH__ == 1:
            return word
        if  word == Empty:
            return start_key()
        
        parted = key.partition(KeySeparator)
        return parted[2] + KeySeparator + word

    def generate_condition(txt_len,word):
        if  word == Empty:
            if  txt_len < __MINLEN__:
                return False
        return True

    class WordsMap():
        def __init__(self):
            self.words_map = {}
            self.text_stat = {}
            self.text_stat["cur_sent_len"] = 0
            self.text_stat["max_sent_len"] = 0
    
        def insert(self,key,word,separator):
            if  word == Empty and key == start_key():
                return
            if  not key in self.words_map:
                self.words_map[key] = [ ]
            if  not (word,separator) in self.words_map[key]:
                self.words_map[key] += [(word,separator)]

        def feed_line(self,line):
            key = start_key()
            separator = ""
            splitline = [x.lower() for x in rstrip_line(explode_line(line)).split(" ") if x!=""]
            if  len(splitline) == 0:
                return key,separator
            i = 0
            while i < len(splitline):
                separator,i,word = lookup_word(splitline,i,separator)
                if  i != -1:
                    if  word == Empty:
                        if  self.text_stat["max_sent_len"] < self.text_stat["cur_sent_len"]:
                            self.text_stat["max_sent_len"] = self.text_stat["cur_sent_len"]
                        self.text_stat["cur_sent_len"] = 0
                    else:
                        self.text_stat["cur_sent_len"]+= 1
                    self.insert( key , word , separator )
                    key = next_key( key , word )
                    separator = ''
                else:
                    return key, separator
            return key, ''

        def clear_before_generate(self):
            self.txt_len = 0
            self.undo_len = 1
            self.word = Empty + "dummy" #just to start while
            self.text = []
            self.keystack = []
            self.key = start_key()
    
        def generate_text(self):
            global txt_len, undo_len, word, text, keystack, key
            self.clear_before_generate()
            while self.word != Empty:
                (self.word,sep) = renpy.random.choice(self.words_map[self.key])
                if  generate_condition(self.txt_len,self.word):
                    self.text += [sep,up_starting(self.word,self.txt_len)]
                    self.keystack += [self.key]
                    self.key = next_key(self.key,self.word)
                    self.txt_len  += 1
                else:
                    if  self.undo_len >= self.txt_len:
                        self.clear_before_generate()
                        continue
                    self.key = self.keystack[-self.undo_len]
                    if  not self.key in self.words_map:
                        renpy.error((self.word,self.key,self.keystack,self.undo_len,self.txt_len,self.text))
                    self.keystack = self.keystack[0:-self.undo_len]
                    self.txt_len -= self.undo_len
                    self.text = self.text[0:-2*self.undo_len]
                    self.word = self.text[-1].lower()
                    self.undo_len += 1
            return "".join(self.text)

    CharsAtEOL  = [ "\n" , "\r" , "\t" , " " ]
    SentanceEnd = [ "." , "!" , "?" , ";", u"вЂ¦" ]
    SentanceSep = [ "," , ":" ]
    SpaceDepSep = [ "-" ]
    

    def up_starting(word,txt_len):
        if  txt_len > 0:
            return word
        if  len(word) > 1:
            return word[0].upper() + word[1:]
        elif  len(word) == 1:
            return word.upper()
        else:
            renpy.error("Empty word")

    def rstrip_line(line):
        while len(line)>0 and line[-1] in CharsAtEOL:
            line = line[0:-1]
        return line

    def explode_line(line):
        for i in SentanceEnd:
            line = line.replace(i," "+i+" ")
        for i in SentanceSep:
            line = line.replace(i," "+i+" ")
        for i in SpaceDepSep:
            line = line.replace(i+" "," "+i+" ")
            line = line.replace(" "+i," "+i+" ")
        return line

    def lookup_word(splitline,i,separator):
        if  i <0 or i >= len(splitline):
            return None,None,None
        while i < len(splitline):
            if  splitline[i] in SentanceSep:
                separator += splitline[i]
                i += 1
                continue
            if  splitline[i] in SentanceEnd:
                separator += splitline[i] + " "
                return separator, i+1, Empty
            return separator+" ", i+1, splitline[i]
        return separator, -1, Empty

    def start():
        global sayers
        global bgs
        global sprites
        global bg
        global sayer

        import re

        sayers = {}
        for key,item in renpy.game.script.namemap.iteritems():
            if  isinstance(item,renpy.ast.Say):
                if  not item.who in sayers:
                    sayers[item.who] = WordsMap()
                sayers[item.who].feed_line(re.sub(r'{[^}]*}', '', item.what+"."))

        bgs = list()
        sprites = {}
        for i in renpy.display.image.images.keys():
            if  i[0] == "roma_guestroom" and not i[0] in bgs:
                bgs.append(i)
            if  i[0] in lgg_character_list:
                if  not i[0] in sprites:
                    sprites[i[0]] = set()
                sprites[i[0]].add(i)
        for k in sprites.keys():
            sprites[k] = list(sprites[k])

        bg = None
        sayer = None    

    def random_bg():
        while True:
            x = renpy.random.choice(bgs)
            if  hasattr(renpy.display.image.images[x],"predict_files"):
                if  [f for f in renpy.display.image.images[x].predict_files() if not renpy.loadable(f)]:
                    continue
            return x

    def random_sprite(sayer):
        while True:
            x = renpy.random.choice(sprites[sayer])
            if  hasattr(renpy.display.image.images[x],"predict_files"):
                if  [f for f in renpy.display.image.images[x].predict_files() if not renpy.loadable(f)]:
                    continue
            return x
        
    def next():
        global bg
        global sayer

        if  renpy.random.random() < 0.05 or not bg:
            renpy.scene('master')
            renpy.show(random_bg())
            sayer = None
        if  renpy.random.random() < 0.05:
            if  sayer is not None:
                renpy.hide(sayer)
            sayer = renpy.random.choice(sprites.keys()+[None])
            if  sayer is not None:
                renpy.show(random_sprite(sayer))

        if  renpy.random.random() < 0.3:
            if  sayer is not None:
                renpy.show(random_sprite(sayer))

        if  sayer == None:
            who = renpy.random.choice([None])
        else:
            who = renpy.random.choice(["rm",sayer,None])

        text = ""
        while True:
            try:
                for i in range(__SENTANCES__):
                    text += sayers[who].generate_text()
                break
            except:
                raise
                continue
            
        if  who == None:
            renpy.exports.say(who, text)
        else:
            renpy.exports.say(globals()[who], text)
            
            
label lb_endless_mod_start:
    $ renpy.music.stop()
    $ renpy.block_rollback()
    scene black
    $ renpy.exports.say(None, u"Processing game. Please, wait...{fast}", interact=None)
    pause 0.01
    $ lb_endless_mod.start()
    jump lb__endless_regenerate

label lb__endless_regenerate:
    $ lb_endless_mod.next()
    jump lb__endless_regenerate
