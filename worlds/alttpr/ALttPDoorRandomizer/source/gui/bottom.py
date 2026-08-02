from tkinter import ttk, messagebox, StringVar, Button, Entry, Frame, Label, LEFT, RIGHT, X
from argparse import Namespace
import logging
import os
import random
import re
from ...CLI import parse_cli
from ...Fill import FillError
from ...Main import main, export_yaml, EnemizerError
from ...Utils import local_path, output_path, open_file, update_deprecated_args
from ..classes import constants as CONST
from .randomize.multiworld import multiworld_page
from . import widgets
from ..classes.Empty import Empty


def bottom_frame(self, parent, args=None):
    # Bottom Frame
    self = ttk.Frame(parent)

    # Bottom Frame options
    self.widgets = {}

    mw,_ = multiworld_page(self, parent.settings)
    mw.pack(fill=X, expand=True)
    self.widgets = mw.widgets

    # Seed input
    # widget ID
    widget = "seed"

    # Empty object
    self.widgets[widget] = Empty()
    # pieces
    self.widgets[widget].pieces = {}

    # frame
    self.widgets[widget].pieces["frame"] = Frame(self)
    # frame: label
    self.widgets[widget].pieces["frame"].label = Label(self.widgets[widget].pieces["frame"], text="Seed #")
    self.widgets[widget].pieces["frame"].label.pack(side=LEFT)
    # storagevar
    savedSeed = parent.settings["seed"]
    self.widgets[widget].storageVar = StringVar(value=savedSeed)
    # textbox
    self.widgets[widget].type = "textbox"
    self.widgets[widget].pieces["textbox"] = Entry(self.widgets[widget].pieces["frame"], width=15, textvariable=self.widgets[widget].storageVar)
    self.widgets[widget].pieces["textbox"].pack(side=LEFT)

    def saveSeed(caller,_,mode):
        savedSeed = self.widgets["seed"].storageVar.get()
        parent.settings["seed"] = int(savedSeed) if savedSeed.isdigit() else None
    self.widgets[widget].storageVar.trace_add("write",saveSeed)
    # frame: pack
    self.widgets[widget].pieces["frame"].pack(side=LEFT)

    ## Number of Generation attempts
    key = "generationcount"
    self.widgets[key] = widgets.make_widget(
      self,
      "spinbox",
      self,
      "Count",
      None,
      None,
      {"label": {"side": LEFT}, "spinbox": {"side": RIGHT}}
    )
    self.widgets[key].pack(side=LEFT)

    def generateRom():
        guiargs = create_guiargs(parent)
        argsDump = vars(guiargs)
        from Gui import save_settings
        if parent.randomSprite.get():
            argsDump['sprite'] = 'random'
        elif argsDump['sprite']:
            argsDump['sprite'] = argsDump['sprite'].name
        save_settings(parent, argsDump, "last.json")

        try:
            guiargs = create_guiargs(parent)
            # get default values for missing parameters
            cliargs = ['--multi', str(guiargs.multi)]
            if hasattr(guiargs, 'customizer'):
                cliargs.extend(['--customizer', str(guiargs.customizer)])

            for k,v in vars(parse_cli(cliargs)).items():
                if k not in vars(guiargs):
                    setattr(guiargs, k, v)
                elif type(v) is dict:  # use same settings for every player
                    players = guiargs.multi if len(v) == 0 else len(v)
                    setattr(guiargs, k, {player: getattr(guiargs, k) for player in range(1, players + 1)})
            if guiargs.multi == 1 and guiargs.names.endswith("=="):
                # allow settings code thru player names entry
                guiargs.code[1] = guiargs.names
                guiargs.names = ""
            argsDump = vars(guiargs)

            needEnemizer = False
            falsey = ["none", "default", False, 0]
            for enemizerOption in ["shuffleenemies", "enemy_damage", "shufflebosses", "enemy_health"]:
                if enemizerOption in argsDump:
                    if isinstance(argsDump[enemizerOption], dict):
                        for playerID,playerSetting in argsDump[enemizerOption].items():
                            if not playerSetting in falsey:
                                needEnemizer = True
                    elif not argsDump[enemizerOption] in falsey:
                        needEnemizer = True
            seeds = []

            if guiargs.count is not None and guiargs.seed:
                seed = guiargs.seed
                for _ in range(guiargs.count):
                    world = main(seed=seed, args=guiargs, fish=parent.fish)
                    seeds.append(world.seed)
                    seed = random.randint(0, 999999999)
            else:
                if not guiargs.seed:
                    random.seed(None)
                    guiargs.seed = random.randint(0, 999999999)
                world = main(seed=guiargs.seed, args=guiargs, fish=parent.fish)
                seeds.append(world.seed)
        except (FillError, EnemizerError, Exception, RuntimeError) as e:
            logging.exception(e)
            messagebox.showerror(title="Error while creating seed", message=str(e))
        else:
            YES = parent.fish.translate("cli","cli","yes")
            NO = parent.fish.translate("cli","cli","no")
            successMsg = ""
            made = {}
            for k in [ "rom", "playthrough", "spoiler" ]:
                made[k] = parent.fish.translate("cli","cli","made." + k)
            made["enemizer"] = parent.fish.translate("cli","cli","used.enemizer")
            for k in made:
                v = made[k]
                pattern = "([\w]+)(:)([\s]+)(.*)"
                m = re.search(pattern,made[k])
                made[k] = m.group(1) + m.group(2) + ' ' + m.group(4)
            successMsg += (made["rom"] % (YES if (guiargs.create_rom) else NO)) + "\n"
            successMsg += (made["playthrough"] % (YES if (guiargs.calc_playthrough) else NO)) + "\n"
            successMsg += (made["enemizer"] % (YES if needEnemizer else NO)) + "\n"
            # FIXME: English
            successMsg += ("Seed%s: %s" % ('s' if len(seeds) > 1 else "", ','.join(str(x) for x in seeds)))

            messagebox.showinfo(title="Success", message=successMsg)

    ## Generate Button
    # widget ID
    widget = "go"

    # Empty object
    self.widgets[widget] = Empty()
    # pieces
    self.widgets[widget].pieces = {}

    # button
    self.widgets[widget].type = "button"
    self.widgets[widget].pieces["button"] = Button(self, command=generateRom)
    # button: pack
    self.widgets[widget].pieces["button"].pack(side=LEFT)
    self.widgets[widget].pieces["button"].configure(bg="#CCCCCC")

    def exportYaml():
        guiargs = create_guiargs(parent)
        # get default values for missing parameters
        for k,v in vars(parse_cli(['--multi', str(guiargs.multi)])).items():
            if k not in vars(guiargs):
                setattr(guiargs, k, v)
            elif type(v) is dict: # use same settings for every player
                setattr(guiargs, k, {player: getattr(guiargs, k) for player in range(1, guiargs.multi + 1)})

        filename = None
        try:
            from tkinter import filedialog
            filename = filedialog.asksaveasfilename(initialdir=guiargs.outputpath, title="Save file", filetypes=(("Yaml Files", (".yaml", ".yml")), ("All Files", "*")))
            if filename is not None and filename != '':
                guiargs.outputpath = os.path.dirname(filename)
                guiargs.outputname = os.path.splitext(os.path.basename(filename))[0]
                export_yaml(args=guiargs, fish=parent.fish)
        except (FillError, EnemizerError, Exception, RuntimeError) as e:
            logging.exception(e)
            messagebox.showerror(title="Error while exporting yaml", message=str(e))
        else:
            if filename is not None and filename != '':
                successMsg = "File Exported"
                # FIXME: English
                messagebox.showinfo(title="Success", message=successMsg)

    ## Export Yaml Button
    widget = "exportyaml"
    self.widgets[widget] = Empty()
    self.widgets[widget].pieces = {}
    # button
    self.widgets[widget].type = "button"
    self.widgets[widget].pieces["button"] = Button(self, command=exportYaml)
    self.widgets[widget].pieces["button"].pack(side=LEFT)

    def open_output():
        if output_path.cached_path is None:
            if args and args.outputpath:
                output_path.cached_path = args.outputpath
            else:
                output_path.cached_path = parent.settings["outputpath"]

        open_file(output_path('.'))

    def select_output():
        from tkinter import filedialog
        folder_selected = filedialog.askdirectory()
        if folder_selected is not None and folder_selected != '':
            parent.settings["outputpath"] = folder_selected
            if args:
                args.outputpath = folder_selected

    ## Output Button
    widget = "outputdir"
    self.widgets[widget] = Empty()
    self.widgets[widget].pieces = {}

    # storagevar
    self.widgets[widget].storageVar = StringVar(value=parent.settings["outputpath"])

    # button
    self.widgets[widget].type = "button"
    self.widgets[widget].pieces["button"] = Button(self, command=select_output)
    self.widgets[widget].pieces["button"].pack(side=RIGHT)

    ## Save Settings Button
    widget = "savesettings"
    self.widgets[widget] = Empty()
    self.widgets[widget].pieces = {}
    # button
    self.widgets[widget].type = "button"
    self.widgets[widget].pieces["button"] = Button(self)
    self.widgets[widget].pieces["button"].pack(side=RIGHT)

    ## Documentation Button
    # widget ID
    widget = "docs"

    # Empty object
    self.widgets[widget] = Empty()
    # pieces
    self.widgets[widget].pieces = {}
    # button
    self.widgets[widget].type = "button"
    self.widgets[widget].selectbox = Empty()
    self.widgets[widget].selectbox.storageVar = Empty()
    if os.path.exists(local_path('README.html')):
        def open_readme():
            open_file(local_path('README.html'))
        self.widgets[widget].pieces["button"] = Button(self, text='Open Documentation', command=open_readme)
        # button: pack
        self.widgets[widget].pieces["button"].pack(side=RIGHT)

    return self


def create_guiargs(parent):
    guiargs = Namespace()

    # set up settings to gather
    # Page::Subpage::GUI-id::param-id
    options = CONST.SETTINGSTOPROCESS

    # Cycle through each page
    for mainpage in options:
        subpage = None
        _, v = next(iter(options[mainpage].items()))
        if isinstance(v, str):
            subpage = ""
        # Cycle through each subpage (in case of Item Randomizer)
        for subpage in (options[mainpage] if subpage is None else [subpage]):
            # Cycle through each widget
            for widget in (options[mainpage][subpage] if subpage != "" else options[mainpage]):
                # Get the value and set it
                arg = options[mainpage][subpage][widget] if subpage != "" else options[mainpage][widget]
                page = parent.pages[mainpage].pages[subpage] if subpage != "" else parent.pages[mainpage]
                pagewidgets = page.content.customWidgets if mainpage == "custom" else page.content.startingWidgets if mainpage == "startinventory" else page.widgets
                if widget in pagewidgets and hasattr(pagewidgets[widget], 'storageVar'):
                    setattr(guiargs, arg, pagewidgets[widget].storageVar.get())

    # Get Multiworld Worlds count
    guiargs.multi = int(parent.pages["bottom"].pages["content"].widgets["worlds"].storageVar.get())

    # Get baserom path
    guiargs.rom = parent.pages["randomizer"].pages["generation"].widgets["rom"].storageVar.get()

    # Get customizer path
    customizer_value = parent.pages["randomizer"].pages["generation"].widgets["customizer"].storageVar.get()
    if customizer_value and customizer_value != 'None':
        guiargs.customizer = customizer_value

    # Get if we're using the Custom Item Pool
    guiargs.custom = bool(parent.pages["custom"].content.customWidgets["usecustompool"].storageVar.get())

    # Get Seed ID
    guiargs.seed = None
    if parent.pages["bottom"].pages["content"].widgets["seed"].storageVar.get():
        guiargs.seed = parent.pages["bottom"].pages["content"].widgets["seed"].storageVar.get()

    # Get number of generations to run
    guiargs.count = 1
    if parent.pages["bottom"].pages["content"].widgets["generationcount"].storageVar.get():
        guiargs.count = int(parent.pages["bottom"].pages["content"].widgets["generationcount"].storageVar.get())

    # Get Adjust settings
    adjustargs = {
      "nobgm": "disablemusic",
      "quickswap": "quickswap",
      "heartcolor": "heartcolor",
      "heartbeep": "heartbeep",
      "menuspeed": "fastmenu",
      "owpalettes": "ow_palettes",
      "uwpalettes": "uw_palettes",
      "reduce_flashing": "reduce_flashing",
      "shuffle_sfx": "shuffle_sfx",
      "shuffle_sfxinstruments": "shuffle_sfxinstruments",
      "shuffle_songinstruments": "shuffle_songinstruments"
    }
    for adjustarg in adjustargs:
      internal = adjustargs[adjustarg]
      setattr(guiargs,"adjust." + internal, parent.pages["adjust"].content.widgets[adjustarg].storageVar.get())

    # Get Custom Items and Starting Inventory Items
    customitems = CONST.CUSTOMITEMS
    guiargs.startinventory = []
    guiargs.customitemarray = {}
    guiargs.startinventoryarray = {}
    for customitem in customitems:
        if customitem not in CONST.CANTSTARTWITH:
            # Starting Inventory is a CSV
            amount = int(parent.pages["startinventory"].content.startingWidgets[customitem].storageVar.get())
            guiargs.startinventoryarray[customitem] = amount
            for _ in range(0, amount):
                label = CONST.CUSTOMITEMLABELS[customitems.index(customitem)]
                guiargs.startinventory.append(label)
        # Custom Item Pool is a dict of ints
        guiargs.customitemarray[customitem] = int(parent.pages["custom"].content.customWidgets[customitem].storageVar.get())

    # Starting Inventory is a CSV
    guiargs.startinventory = ','.join(guiargs.startinventory)

    # Get Sprite Selection (set or random)
    guiargs.sprite = parent.pages["randomizer"].pages["gameoptions"].widgets["sprite"]["spriteObject"]
    guiargs.randomSprite = parent.randomSprite.get()

    # Get Triforce Piece GFX Selection
    guiargs.triforce_gfx = parent.pages["randomizer"].pages["gameoptions"].widgets["triforce_gfx"]["selectedItem"]

    # Get output path
    guiargs.outputpath = parent.settings["outputpath"]

    guiargs = update_deprecated_args(guiargs)

    return guiargs
