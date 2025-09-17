import ttkbootstrap as ttk
from Views.base_window_toplevel import BaseProjectWindowToplevel, BaseProjectWindow


class AlertWindow(ttk.Toplevel):

    def __init__(self, parent_window: BaseProjectWindowToplevel | BaseProjectWindow, success: bool, error_msg: str='Error Desconocido'):
        super().__init__()
        if success:
            self.title('alerta - Producto agregado exitosamente')
        else:
            self.title('alerta - Error')

        self.parent_window = parent_window
        self.ancho = int(parent_window.winfo_width() / 4)
        self.alto = int(parent_window.winfo_height() / 6)
        self.x = (parent_window.winfo_screenwidth() - self.ancho) // 2
        self.y = (parent_window.winfo_screenheight() - self.alto) // 2
        self.geometry(f'{self.ancho}x{self.alto}+{self.x}+{self.y}')


        # ventana

        # alert_window.iconbitmap(parent_window.parent.icon_path)
        # self.iconbitmap(parent.icon_path) funciona en windows no en linux
        self.wm_iconphoto(False, parent_window.parent.icon)

        # label

        self.label_alerta = ttk.Label(master=self, text='')
        self.label_alerta.configure(text="Algo malio sal :(")
        if success:
            self.label_alerta.configure(text='producto agregado exitosamente')
        self.label_alerta.configure(font='Arial 20 bold')
        self.msg = ttk.StringVar()
        self.msg.set(error_msg)
        self.label_msg = ttk.Label(master=self, textvariable=self.msg, font='Arial 12 bold', wraplength=250)

        self.focus_set()
        self.grab_set()

        self.button_confirm = ttk.Button(master=self, text='Aceptar', style='success')
        self.button_confirm.configure(width=15, command=self.aceptar)

        self.label_alerta.pack()
        self.button_confirm.place(relx=0.5, rely=0.8, anchor='center', width=100, height=40)
        if not success:
            self.label_msg.pack()

        # mainloop

        self.mainloop()

        # gestion de eventos

        self.bind('<Return>', lambda *args: self.aceptar())


    def aceptar(self):
        self.parent_window.cerrar_ventana_alerta()

