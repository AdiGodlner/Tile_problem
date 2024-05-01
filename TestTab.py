import tkinter as tk


class TestTab(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent,width=200, height=150)
        self.myFrame = tk.Frame(self, width=200, height=150, bg="lightblue")
        parent.bind("<Configure>", self.update_frame_width)
        self.myFrame.pack()

        self.btnX = 0.1
        self.btnY = 0.1
        self.btn1 = None
        self.btn2 = None
        self.flag = True

        self.btn1 = tk.Button(self.myFrame, text="my btn", command=self.move_btn)
        self.btn1.pack()
        # self.create_widgets()

    def update_frame_width(self, event):
        print(f"update_frame_width | {event.size}")
        self.myFrame.configure(width=event.size)

    def create_widgets(self):
        self.btn1 = tk.Button(self, text="my btn", command=self.move_btn)
        self.btn1.place(relx=self.btnX,
                        rely=self.btnY,
                        relheight=self.btnX,
                        anchor="center")
        self.btn2 = tk.Button(self, text="my btn", command=self.move_btn)
        self.btn2.place(relx=self.btnX + 0.1,
                        rely=self.btnY,
                        relheight=self.btnX,
                        anchor="center")
        pass

    def move_btn(self):
        if self.flag:
            self.btnX += 0.01
            self.flag = self.btnX < 1
        else:
            self.btnX -= 0.01
            self.flag = self.btnX < 0

        self.btn1.place(relx=self.btnX,
                       rely=self.btnY,
                       relheight=0.5,
                       anchor="center")
        self.after(10, self.move_btn)

    def on_view(self):
        pass
