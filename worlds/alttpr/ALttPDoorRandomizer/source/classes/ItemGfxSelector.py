from tkinter import Button, Canvas, Label, LabelFrame, Frame, PhotoImage, Scrollbar, Toplevel, LEFT, BOTTOM, X, RIGHT, TOP
import os
from GuiUtils import ToolTips, set_icon
from Utils import local_path


class ItemGfxSelector(object):
    def __init__(self, parent, callback, valid_items=None, adjuster=False):
        self.parent = parent
        self.window = Toplevel(parent)
        self.window.geometry("800x650")
        self.callback = callback
        self.valid_items = valid_items if valid_items else []
        self.adjuster = adjuster

        self.window.wm_title("Select Triforce Piece Graphics")
        self.window['padx'] = 5
        self.window['pady'] = 5

        def open_itemgfx_dir(_evt):
            from Utils import open_file
            itemgfx_dir = local_path(os.path.join("data", "itemgfx"))
            if not os.path.isdir(itemgfx_dir):
                os.makedirs(itemgfx_dir)
            open_file(itemgfx_dir)

        frametitle = Frame(self.window)
        title_text = Label(frametitle, text="Item Graphics")
        title_text.pack(side=LEFT)
        local_title_link = Label(frametitle, text="(open folder)", fg="blue", cursor="hand2")
        local_title_link.pack(side=LEFT)
        local_title_link.bind("<Button-1>", open_itemgfx_dir)

        self.icon_section(frametitle)

        frame = Frame(self.window)
        frame.pack(side=BOTTOM, fill=X, pady=5)

        button = Button(frame, text="Default (Triforce)", command=self.use_default)
        button.pack(side=LEFT, padx=(0, 5))

        if adjuster:
            button = Button(frame, text="Current triforce from rom", command=self.use_default_unchanged)
            button.pack(side=LEFT, padx=(0, 5))

        set_icon(self.window)
        self.window.focus()

    def icon_section(self, frame_label):
        frame = LabelFrame(self.window, labelwidget=frame_label, padx=5, pady=5)
        canvas = Canvas(frame, borderwidth=0, width=780)
        y_scrollbar = Scrollbar(frame, orient="vertical", command=canvas.yview)
        y_scrollbar.pack(side="right", fill="y")
        content_frame = Frame(canvas)
        canvas.pack(side="left", fill="both", expand=True)
        canvas.create_window((4, 4), window=content_frame, anchor="nw")
        canvas.configure(yscrollcommand=y_scrollbar.set)

        def onFrameConfigure(canvas):
            """Reset the scroll region to encompass the inner frame"""
            canvas.configure(scrollregion=canvas.bbox("all"))

        content_frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))
        frame.pack(side=TOP, fill="both", expand=True)

        itemgfx_dir = local_path(os.path.join("data", "itemgfx"))
        
        if not os.path.exists(itemgfx_dir):
            label = Label(content_frame, text='No item graphics found in data/itemgfx folder.')
            label.pack()
            return

        # Get all GIF files (converted from PNG)
        gif_files = []
        for file in os.listdir(itemgfx_dir):
            if file.lower().endswith('.gif'):
                item_name = os.path.splitext(file)[0]
                # Only include if it's in the valid_items list
                if item_name in self.valid_items:
                    gif_files.append((file, item_name))

        # Sort by name
        gif_files.sort(key=lambda x: str.lower(x[1]))

        if len(gif_files) == 0:
            label = Label(content_frame, text='No valid item graphics found. Items must match names from Tables.py.')
            label.pack()
            return

        # Calculate how many columns can fit (assuming ~40px per icon with padding)
        max_columns = 18
        
        i = 0
        for filename, item_name in gif_files:
            filepath = os.path.join(itemgfx_dir, filename)
            image = self.get_image_for_item(filepath)
            if image is None:
                continue
            
            button = Button(content_frame, image=image, command=lambda name=item_name: self.select_item(name))
            ToolTips.register(button, item_name)
            button.image = image
            button.grid(row=i // max_columns, column=i % max_columns, padx=2, pady=2)
            i += 1

        if i == 0:
            label = Label(content_frame, text='No valid item graphics could be loaded.')
            label.pack()

    def get_image_for_item(self, filepath):
        """Load and prepare an item graphic for display"""
        try:
            # Load GIF with native Tkinter PhotoImage (no PIL required)
            photo = PhotoImage(file=filepath)
            return photo
        except Exception as e:
            print(f"Error loading image {filepath}: {e}")
            return None

    def use_default(self):
        self.callback("Triforce")
        self.window.destroy()

    def use_default_unchanged(self):
        self.callback(None)
        self.window.destroy()

    def select_item(self, item_name):
        self.callback(item_name)
        self.window.destroy()
