init python in lb_registration:
    lb_mods["lb_helloworld_mod_start"] = u"Тестовый сценарий"

label lb_helloworld_mod_start:
    $ time = 'day'
    scene roma_kitchen day
    show an school kind normal 
    with emc
    an "Тест!"
    $ time = 'night'
    scene roma_kitchen day
    show an school kind normal 
    with emc
    an "Тест!"
    ".:GOOD END:."