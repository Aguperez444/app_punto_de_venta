import ttkbootstrap as ttk
import project_functions
from Views.base_window_toplevel import BaseProjectWindowToplevel

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Controllers.register_sale_controller import RegisterSaleController


class VentanaVenta(BaseProjectWindowToplevel):

    def __init__(self, parent, controller: 'RegisterSaleController', product_data: dict): #TODO CHECK THIS
        super().__init__(parent)
        self.controller = controller

        # ----------------------------------------- ventana ---------------------------------------------
        self.tecla_presionada = False
            # TODO hasta donde entiendo, de esto se debería encargar la clase padre

        self.focus_set()
        self.grab_set()
        # -------------------------------------obtención de datos ----------------------------------------

        # datos del producto
        self.producto = product_data
        self.product_name = self.producto['producto']

        # -----------------------------------------ttk_variables------------------------------------------------
        self.cantidad_vendida = ttk.StringVar()
        self.cantidad_vendida.set('1')
        self.title = f'¿Desea registrar una venta de: {self.product_name}?'
        # -----------------------------------------bootstrap widgets------------------------------------------------
        self.label_titulo = ttk.Label(master=self, text=f'{self.title}', font='Calibri 20 bold')
        self.label_subtitulo = ttk.Label(master=self, text='Info del producto:', font='Calibri 16 bold')

        self.sub_frame = ttk.Frame(master=self, width=1000, height=12)
        self.entry_frame = ttk.Frame(master=self, width=120, height=40)

        self.label_entry = ttk.Label(master=self.entry_frame, text='Cantidad:', font='Calibri 14 bold')
        self.entry_cantidad_vendida = ttk.Entry(master=self.entry_frame, textvariable=self.cantidad_vendida, width=3)

        # -----------------------------Buttons------------------------------
        #self.confirm_button = ttk.Button(master=self, text='Confirmar venta', style='success',
        #                            command=lambda: self.venta_confirm(product_id, self.cantidad_vendida.get())) #TODO CHECK THIS

        self.confirm_button = ttk.Button(master=self, text='Confirmar venta', style='success',
                                    command=self.venta_confirm) #TODO CHECK THIS

        self.cancel_button = ttk.Button(master=self, text='Cancelar venta', style='danger',
                                   command=self.venta_cancel)


        self.adjust_view_for_resolution()

        # -----------------------------------------------gestion de eventos----------------------------------------

        self.bind("<Configure>", self.on_resize)
        self.bind("<KeyPress>", self.iniciar_actualizacion)
        self.bind("<KeyRelease>", self.detener_actualizacion)



    # --------------------------------- Métodos de esta ventana ----------------------------------
    # region Funciones para manejo de UX
    def iniciar_actualizacion(self, event):
        # Marcar la tecla como presionada
        self.tecla_presionada = True
        # Llamar a la función de actualización
        self.actualizar_cantidad(event)

    def detener_actualizacion(self, _event):
        # Marcar la tecla como liberada
        self.tecla_presionada = False

    def actualizar_cantidad(self, event):
        if self.tecla_presionada:
            if self.cantidad_vendida.get() != '' and project_functions.no_contiene_letras(self.cantidad_vendida.get()):
                if event.keysym == 'Up':
                    nueva_cantidad = int(self.cantidad_vendida.get()) + 1
                elif event.keysym == 'Down':
                    nueva_cantidad = int(self.cantidad_vendida.get()) - 1
                else:
                    nueva_cantidad = int(self.cantidad_vendida.get())

                if nueva_cantidad <= 0:
                    nueva_cantidad = 1

                self.cantidad_vendida.set(str(nueva_cantidad))

                # Llamar a la función de actualización nuevamente después de un breve retraso
                #self.after(100, lambda: self.actualizar_cantidad(event))
                self.after(100, self.actualizar_cantidad, event)

    # endregion

    #region Funciones Para manejo de UI

    def render_view(self):
        # ---------------------------------------------- placing widgets -----------------------------------------------
        self.pasar_unico_al_cuadro(self.producto)

        self.label_titulo.pack()
        self.label_subtitulo.pack()
        self.cuadro.pack_configure(fill='both', expand=True)
        self.sub_frame.place(relx=0.5, rely=0.5, relwidth=0.9, height=70, anchor='center')
        self.confirm_button.place(relx=0.8, rely=0.8, anchor='center')
        self.confirm_button.place_configure(width=160, height=60)
        self.cancel_button.place(relx=0.2, rely=0.8, anchor='center')
        self.cancel_button.place_configure(width=160, height=60)
        self.entry_frame.place(relx=0.5, rely=0.3, anchor='center')
        self.label_entry.place(relx=0, rely=0, anchor='nw')
        self.entry_cantidad_vendida.place(relx=1, rely=0, anchor='ne')

    def adjust_view_for_resolution(self):
        if self.resolution[0] == '615x461':
            if len(self.title) > 50:
                self.label_titulo.configure(font='Calibri 15 bold')
                self.label_subtitulo.configure(font='Calibri 13 bold')
            self.label_entry.configure(font='Calibri 12 bold')

    # endregion

    def venta_confirm(self):
        amount_in = self.cantidad_vendida.get()
        self.controller.register_new_sale(self.producto, amount_in)

    def sale_registered(self):
        self.parent.realizar_busqueda()
        self.destroy()

    def venta_cancel(self):
        self.destroy()

