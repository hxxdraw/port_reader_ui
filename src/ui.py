from config import *
import tkinter as tk
from tkinter import ttk
from src import port_mngr
from threading import Thread
from tkinter.colorchooser import askcolor


class Application(tk.Tk):
    def __init__(self):
        super(Application, self).__init__()
        self.title(WINDOW_TITLE)
        self.wm_attributes(ATTR_FULLSCREEN, WINDOW_FULLSCREEN)
        self.wm_attributes(ATTR_TOPMOST, WINDOW_TOPMOST)
        self.resizable(*WINDOW_RESIZABLE)
        self.overrideredirect(WINDOW_BORDERLESS)
        self.geometry("{}x{}+{}+{}".format(*WINDOW_SIZE, *self.__window_center_align()))
        self.__use_theme()
        Screen(self).pack(fill=tk.BOTH, expand=True)

    def __window_center_align(self):
        x, y = self.winfo_screenwidth() - WINDOW_SIZE[0], self.winfo_screenheight() - WINDOW_SIZE[1]
        return x // 2, y // 2

    def __use_theme(self):
        self.tk.call("source", r"themes/Sun-Valley-ttk-theme/sun-valley.tcl")
        self.tk.call("set_theme", "dark")


class Screen(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super(Screen, self).__init__(*args, **kwargs)
        # Screen parts
        self.console = ConsoleNotebook(self)
        self.settings = SettingsNotebook(self)

        # Grid config
        self.grid_rowconfigure(0, weight=2)
        self.grid_columnconfigure(0, weight=2)
        self.console.grid(row=0, column=0, sticky=tk.NSEW, pady=10, rowspan=2)
        self.settings.grid(row=0, column=1, sticky=tk.NSEW, pady=10, padx=20, rowspan=2)


class SettingsNotebook(ttk.Notebook):
    def __init__(self, *args, **kwargs):
        super(SettingsNotebook, self).__init__(*args, **kwargs)
        self.screen = args[0]
        self.settings_container = SettingsContainer(self)

        # Adding frames
        self.add(self.settings_container, text=TEXT_SETTINGS)


class ConsoleNotebook(ttk.Notebook):
    def __init__(self, *args, **kwargs):
        super(ConsoleNotebook, self).__init__(*args, **kwargs)
        self.console_container = ConsoleContainer(self)
        self.devices_container = DevicesContainer(self)
        # Adding frames
        self.add(self.devices_container, text=TEXT_DEVICES)
        self.add(self.console_container, text=TEXT_CONSOLE)


class SettingsContainer(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super(SettingsContainer, self).__init__(*args, **kwargs)
        self.parent = args[0]
        # Labels
        self.decoding_var = tk.BooleanVar()
        self.buttons_container = ttk.Frame(
            self
        )
        self.console_editor_container = ttk.Frame(
            self
        )
        self.switches_container = ttk.Frame(
            self
        )
        self.output_color_lbl = ttk.Label(
            self.console_editor_container,
            text=TEXT_TEXT_COLOR
        )
        self.field_bg_lbl = ttk.Label(
            self.console_editor_container,
            text=TEXT_CONSOLE_COLOR
        )
        self.output_color_ent = ttk.Entry(
            self.console_editor_container,
            **WConfig.select_color_entry
        )
        self.field_bg_ent = ttk.Entry(
            self.console_editor_container,
            **WConfig.select_color_entry
        )
        self.decoding_switch = ttk.Checkbutton(
            self.switches_container,
            text=TEXT_DECODING,
            style=Styles.switch_checkbutton,
            variable=self.decoding_var,
            command=lambda: self.__switch_decoding()
        )
        self.output_string_ent = ttk.Entry(
            self
        )
        self.separator1 = ttk.Separator(
            self
        )
        self.separator2 = ttk.Separator(
            self
        )
        self.apply_btn = ttk.Button(
            self.buttons_container,
            text=TEXT_APPLY,
            **WConfig.default_button
        )
        self.reset_btn = ttk.Button(
            self.buttons_container,
            text=TEXT_RESET,
            **WConfig.default_button
        )

        # Binds
        self.output_color_ent.bind(Events.LEFT_CLICK, self.__open_color_selector)
        self.field_bg_ent.bind(Events.LEFT_CLICK, self.__open_color_selector)
        self.apply_btn.bind(Events.LEFT_CLICK, lambda e: self.__apply_changes())
        self.reset_btn.bind(Events.LEFT_CLICK, lambda e: self.__set_default())

        # Grid
        self.buttons_container.grid_columnconfigure(0, weight=2)
        self.buttons_container.grid_columnconfigure(1, weight=2)
        self.console_editor_container.grid_columnconfigure(0, weight=2)
        self.console_editor_container.grid_columnconfigure(1, weight=2)

        self.console_editor_container.grid(row=0, column=0, sticky=tk.NSEW, padx=5, pady=10)
        self.separator1.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW, pady=10)
        self.switches_container.grid(row=2, column=0, sticky=tk.NSEW, columnspan=2, padx=5)
        self.separator2.grid(row=3, column=0, columnspan=2, sticky=tk.NSEW, pady=10)
        self.buttons_container.grid(row=4, column=0, columnspan=2, sticky=tk.NSEW)

        self.output_color_lbl.grid(row=1, column=0, sticky=tk.NSEW, padx=5)
        self.output_color_ent.grid(row=1, column=1, sticky=tk.NSEW, padx=5)
        self.field_bg_lbl.grid(row=2, column=0, sticky=tk.NSEW, padx=5, pady=10)
        self.field_bg_ent.grid(row=2, column=1, sticky=tk.NSEW, padx=5, pady=10)
        self.decoding_switch.grid(row=0, column=0, sticky=tk.NSEW)
        self.apply_btn.grid(row=0, column=0, sticky=tk.NSEW, padx=5, pady=5)
        self.reset_btn.grid(row=0, column=1, sticky=tk.NSEW, padx=5, pady=5)

        self.__set_default()

    @staticmethod
    def __open_color_selector(event):
        event.widget.delete(0, tk.END)
        event.widget.insert(0, askcolor()[1])

    def __apply_changes(self):
        self.parent.screen.console.console_container.configure_console(bg=self.field_bg_ent.get(), fg=self.output_color_ent.get())

    def __set_default(self):
        self.output_color_ent.delete(0, tk.END)
        self.field_bg_ent.delete(0, tk.END)
        self.output_color_ent.insert(0, Default.FG)
        self.field_bg_ent.insert(0, Default.BG)
        self.__apply_changes()

    def __switch_decoding(self):
        port_mngr.DECODING = self.decoding_var.get()


class ConsoleContainer(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super(ConsoleContainer, self).__init__(*args, **kwargs)
        # Grid config
        self.grid_rowconfigure(0, weight=2)
        self.grid_columnconfigure(0, weight=2)
        self.console_box = ttk.Frame(
            self
        )
        self.console_textarea = tk.Listbox(
            self.console_box,
            **WConfig.console
        )
        self.console_x_scroll = ttk.Scrollbar(
            self.console_box,
            command=self.console_textarea.xview,
            orient=tk.HORIZONTAL
        )
        self.console_y_scroll = ttk.Scrollbar(
            self.console_box,
            command=self.console_textarea.yview,
            orient=tk.VERTICAL
        )
        self.clear_btn = ttk.Button(
            self,
            text=TEXT_CLEAR_FIELD,
            style=Styles.accent_button,
            **WConfig.default_button
        )
        self.console_textarea.configure(
            yscrollcommand=self.console_y_scroll.set,
            xscrollcommand=self.console_x_scroll.set
        )

        self.clear_btn.bind(Events.LEFT_CLICK, lambda e: self.__clear_console())

        # Grid
        self.clear_btn.grid(row=2, column=0, columnspan=2, sticky=tk.NSEW, pady=10, padx=5, ipady=3)
        self.console_box.grid(row=0, column=0, sticky=tk.NSEW, padx=5, pady=10, rowspan=2)
        self.console_y_scroll.pack(fill=tk.Y, side=tk.RIGHT)
        self.console_x_scroll.pack(fill=tk.X, side=tk.BOTTOM)
        self.console_textarea.pack(fill=tk.BOTH, expand=True)

    def configure_console(self, **kwargs):
        self.console_textarea.configure(**kwargs)
        self.console_textarea.update()

    def __clear_console(self):
        self.console_textarea.delete(0, tk.END)


class DevicesContainer(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super(DevicesContainer, self).__init__(*args, **kwargs)
        self.grid_rowconfigure(0, weight=2)
        self.grid_columnconfigure(0, weight=2)
        self.parent = args[0]
        self.devices = []

        self.listbox_container = ttk.Frame(
            self
        )
        self.buttons_container = ttk.Frame(
            self,
        )
        self.devices_listbox = tk.Listbox(
            self.listbox_container,
            **WConfig.devices
        )
        self.devices_listbox_x_scroll = ttk.Scrollbar(
            self.listbox_container,
            command=self.devices_listbox.xview,
            orient=tk.HORIZONTAL
        )
        self.devices_listbox_y_scroll = ttk.Scrollbar(
            self.listbox_container,
            command=self.devices_listbox.yview,
            orient=tk.VERTICAL
        )
        self.devices_listbox.configure(
            xscrollcommand=self.devices_listbox_x_scroll.set,
            yscrollcommand=self.devices_listbox_y_scroll.set
        )
        self.connect_btn = ttk.Button(
            self.buttons_container,
            text=TEXT_CONNECT,
            **WConfig.default_button
        )
        self.update_btn = ttk.Button(
            self.buttons_container,
            text=TEXT_UPDATE,
            style=Styles.accent_button,
            **WConfig.default_button
        )
        self.disconnect_btn = ttk.Button(
            self.buttons_container,
            text=TEXT_DISCONNECT,
            **WConfig.default_button
        )

        # Pack
        self.devices_listbox_x_scroll.pack(fill=tk.X, side=tk.BOTTOM)
        self.devices_listbox_y_scroll.pack(fill=tk.Y, side=tk.RIGHT)
        self.devices_listbox.pack(fill=tk.BOTH, expand=True)

        self.update_btn.bind(Events.LEFT_CLICK, lambda e: self.__scan())
        self.connect_btn.bind(Events.LEFT_CLICK, lambda e: self.__connect())
        self.disconnect_btn.bind(Events.LEFT_CLICK, lambda e: self.__disconnect())
        # Grid
        self.buttons_container.grid_columnconfigure(0, weight=2)
        self.buttons_container.grid_columnconfigure(1, weight=2)
        self.listbox_container.grid(row=0, column=0, sticky=tk.NSEW, padx=5, pady=10)
        self.buttons_container.grid(row=1, column=0, sticky=tk.NSEW, padx=5, pady=5)
        self.connect_btn.grid(row=0, column=0, sticky=tk.NSEW, ipady=3, padx=10)
        self.disconnect_btn.grid(row=0, column=1, sticky=tk.NSEW, ipady=3, padx=10)
        self.update_btn.grid(row=1, column=0, sticky=tk.NSEW, columnspan=4, padx=10, pady=10, ipady=3)
        self.__scan()

    def __scan(self):
        self.devices.clear()
        self.devices_listbox.delete(0, tk.END)

        for port, device, hwid in port_mngr.get_ports():
            self.devices.append((port, device))
            self.devices_listbox.insert(tk.END, f"{port}: {device}")

    def __connect(self):
        port_mngr.IS_RUNNING = True
        Thread(target=port_mngr.read_port, args=(self.devices[self.devices_listbox.curselection()[0]][0], self.parent.console_container.console_textarea)).start()

    @staticmethod
    def __disconnect():
        port_mngr.IS_RUNNING = False
