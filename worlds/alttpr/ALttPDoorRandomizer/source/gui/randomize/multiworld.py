from tkinter import ttk, StringVar, Entry, Frame, Label, N, E, W, X, LEFT
from ..widgets import *
import json
import os
from ...classes.Empty import Empty

def multiworld_page(parent,settings):
    # Multiworld
    self = ttk.Frame(parent)

    # Multiworld options
    self.widgets = {}

    # Multiworld option sections
    self.frames = {}
    self.frames["widgets"] = Frame(self)
    self.frames["widgets"].pack(anchor=W, fill=X)

    # Load Multiworld option widgets as defined by JSON file
    # Defns include frame name, widget type, widget options, widget placement attributes
    with open(os.path.join("resources","app","gui","randomize","multiworld","widgets.json")) as multiworldItems:
        myDict = json.load(multiworldItems)
        myDict = myDict["widgets"]
        dictWidgets = widgets.make_widgets_from_dict(self, myDict, self.frames["widgets"])
        for key in dictWidgets:
            self.widgets[key] = dictWidgets[key]
            self.widgets[key].pack(side=LEFT, anchor=N)

    ## List of Player Names
    # This one's more-complicated, build it and stuff it
    # widget ID
    widget = "names"

    # Empty object
    self.widgets[widget] = Empty()
    # pieces
    self.widgets[widget].pieces = {}

    # frame
    self.widgets[widget].pieces["frame"] = Frame(self.frames["widgets"])
    # frame: label
    self.widgets[widget].pieces["frame"].label = Label(self.widgets[widget].pieces["frame"], text='Player names')
    # storage var
    self.widgets[widget].storageVar = StringVar(value=settings["names"])

    # FIXME: Got some strange behavior here; both Entry-like objects react to mousewheel on Spinbox
    def saveMultiNames(caller,_,mode):
        settings["names"] = self.widgets["names"].storageVar.get()
    self.widgets[widget].storageVar.trace_add("write",saveMultiNames)
    # textbox
    self.widgets[widget].pieces["textbox"] = Entry(self.widgets[widget].pieces["frame"], textvariable=self.widgets[widget].storageVar)

    # frame label: pack
    self.widgets[widget].pieces["frame"].label.pack(side=LEFT, anchor=N)
    # textbox: pack
    self.widgets[widget].pieces["textbox"].pack(side=LEFT, anchor=N, fill=X, expand=True)
    # frame: pack
    self.widgets[widget].pieces["frame"].pack(side=LEFT, anchor=N, fill=X, expand=True)

    return self,settings
