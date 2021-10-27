import sys
import tkinter as tk
import tkinter.ttk as ttk

class App(ttk.Frame):
    def __init__(self, parent, title=None):
        super().__init__(parent)
        parent.wm_geometry("600x400")
        parent.wm_title(title)
        self.top = tk.Frame(self, height=100, background="green4")
        self.middle = tk.Frame(self, background="red4")
        self.lower = tk.Frame(self, height=100, background="blue4")

        self.textframe = ttk.Frame(self.middle)
        self.text = tk.Text(self.textframe)
        self.vs = ttk.Scrollbar(self.textframe,
                                command=self.text.yview)
        self.sg = ttk.Sizegrip(self.textframe)
        self.text.configure(yscrollcommand=self.vs.set)
        self.text.grid(row=0, column=0, sticky="news")
        self.vs.grid(row=0, column=1, sticky="news")
        self.sg.grid(row=1, column=1, sticky="sew")
        self.textframe.grid_rowconfigure(0, weight=1)
        self.textframe.grid_columnconfigure(0, weight=1)
        self.middle.bind('<Map>', self.Place)

        self.sg.bindtags((self.sg, '.','all'))
        self.sg.bind('<Button-1>', self.Press)
        self.sg.bind('<B1-Motion>', self.Drag)
        self.sg.bind('<ButtonRelease-1>', self.Release)

        self.top.grid(row=0, column=0, sticky="news")
        self.middle.grid(row=1, column=0, sticky="news")
        self.lower.grid(row=2, column=0, sticky="news")
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid(row=0,column=0, sticky="news")
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

    def Press(self, ev):
        self.dragging=True
        self.dragpos = (ev.x_root, ev.y_root)

    def Drag(self, ev):
        if self.dragging:
            dx = ev.x_root - self.dragpos[0]
            dy = ev.y_root - self.dragpos[1]
            sgx = self.sg.winfo_x() + dx
            sgy = self.sg.winfo_y() + dy
            sgw = self.sg.winfo_reqwidth()
            sgh = self.sg.winfo_reqheight()
            max_w = self.middle.winfo_width() - sgw
            max_h = self.middle.winfo_height() - sgh
            if sgx < 0 or sgx > max_w or sgy < 0 or sgy > max_h:
                return
            self.textframe.place(x=0, y=0,
                            width=sgx+sgw, height=sgy+sgh)
            self.dragpos = (ev.x_root, ev.y_root)

    def Release(self, ev):
        self.dragging=False

    def Place(self, ev):
        """Place the text widget controls once the rest of the
        application has been mapped so we actually have a size
        to work from.
        Reset the Map event to avoid re-calling this code."""
        self.textframe.bind('<Map>', None)
        self.textframe.place(x=0, y=0,
                             width=self.middle.winfo_width(),
                             height=self.middle.winfo_height())

def main(args=None):
    root = tk.Tk()
    app = App(root, "Sizegrip demo")
    root.mainloop()
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))