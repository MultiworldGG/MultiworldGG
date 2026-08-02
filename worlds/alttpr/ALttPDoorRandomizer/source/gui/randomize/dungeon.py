from tkinter import ttk, Frame, Label, E, W, LEFT, RIGHT, TOP
from ..widgets import *
import json
import os

def dungeon_page(parent):
    # Dungeon Shuffle
    self = ttk.Frame(parent)

    # Dungeon Shuffle options
    self.widgets = {}

    # Dungeon Shuffle option sections
    self.frames = {}
    self.frames["keysanity"] = Frame(self)
    self.frames["keysanity"].pack(anchor=W)
    self.frames["keysanity2"] = Frame(self)
    self.frames["keysanity2"].pack(anchor=W)

    ## Dungeon Item Shuffle
    mscbLabel = Label(self.frames["keysanity"], text="Dungeon Items: ")
    mscbLabel.pack(side=TOP, anchor=W)

    # Load Dungeon Shuffle option widgets as defined by JSON file
    # Defns include frame name, widget type, widget options, widget placement attributes
    # This first set goes in the Keysanity frame
    with open(os.path.join("resources","app","gui","randomize","dungeon","keysanity.json")) as keysanityItems:
        myDictFile = json.load(keysanityItems)
        myDict = myDictFile["keysanity"]
        myDict1, myDict2 = dict(), dict()
        count = 2
        for key in myDict.keys():
            (myDict1 if count > 0 else myDict2)[key] = myDict[key]
            count -= 1
        dictWidgets = {**widgets.make_widgets_from_dict(self, myDict1, self.frames["keysanity"]), \
                      **widgets.make_widgets_from_dict(self, myDict2, self.frames["keysanity2"])}
        for key in dictWidgets:
            self.widgets[key] = dictWidgets[key]
            packAttrs = {"side":LEFT}
            packAttrs = widgets.add_padding_from_config(packAttrs, myDict[key])
            self.widgets[key].pack(packAttrs)

    # These get split left & right
    self.frames["widgets"] = Frame(self)
    self.frames["widgets"].pack(anchor=W)
    with open(os.path.join("resources","app","gui","randomize","dungeon","widgets.json")) as dungeonWidgets:
        myDict = json.load(dungeonWidgets)
        myDict = myDict["widgets"]
        dictWidgets = widgets.make_widgets_from_dict(self, myDict, self.frames["widgets"])
        for key in dictWidgets:
            self.widgets[key] = dictWidgets[key]
            packAttrs = {"anchor":W}
            packAttrs = widgets.add_padding_from_config(packAttrs, myDict[key])
            self.widgets[key].pack(packAttrs)

    return self
