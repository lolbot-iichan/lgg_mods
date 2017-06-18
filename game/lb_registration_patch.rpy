#provides a map for mod registration

init -99999 python in lb_registration:
    lb_mods = {}

    rgsn = renpy.game.script.namemap
    rgsn["lb__start_original"],rgsn["start"] = rgsn["start"],rgsn["lb__start_original"]

label lb__start_original:
    if  not lb_registration.lb_mods:
        jump lb__start_original
    menu:
        "Начать обычную игру":
            jump lb__start_original
        "Играть в модификацию":
            jump lb__start_mod

label lb__start_mod:
    jump expression renpy.display_menu([(v,k) for k,v in lb_registration.lb_mods.items()])   
                      