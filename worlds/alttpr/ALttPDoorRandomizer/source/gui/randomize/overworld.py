from tkinter import ttk, Frame, Label, W, E, NW, LEFT, RIGHT, X, Y, TOP
from . import widgets
import json
import os

def overworld_page(parent):
    # Overworld Shuffle
    self = ttk.Frame(parent)

    # Overworld Shuffle options
    self.widgets = {}

    # Overworld Shuffle option sections
    self.frames = {}

    # Load Overworld Shuffle option widgets as defined by JSON file
    # Defns include frame name, widget type, widget options, widget placement attributes
    self.frames["leftOverworldFrame"] = Frame(self)
    self.frames["rightOverworldFrame"] = Frame(self)

    self.frames["leftOverworldFrame"].pack(side=LEFT, anchor=NW, fill=Y)
    self.frames["rightOverworldFrame"].pack(anchor=NW, fill=Y)
    
    with open(os.path.join("resources","app","gui","randomize","overworld","widgets.json")) as overworldWidgets:
        myDict = json.load(overworldWidgets)
        for framename,theseWidgets in myDict.items():
            if not theseWidgets:
                continue
            dictWidgets = widgets.make_widgets_from_dict(self, theseWidgets, self.frames[framename])
            for key in dictWidgets:
                self.widgets[key] = dictWidgets[key]
                packAttrs = {"anchor":W}
                if self.widgets[key].type != "checkbox":
                    packAttrs["anchor"] = E
                packAttrs = widgets.add_padding_from_config(packAttrs, theseWidgets[key])
                self.widgets[key].pack(packAttrs)

    return self
