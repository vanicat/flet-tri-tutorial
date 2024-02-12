import flet as ft

class MyApp:
    def __init__(self) -> None:
        pass

    def setup(self, page: ft.Page) -> None:
        page.add(ft.SafeArea(ft.Text("Trouver un algorithme de tri")))
        buttons_row = ft.Row([
            ft.TextButton("aide", on_click=self.help),
            ft.TextButton("cmp", on_click=self.cmp)
        ])
        page.add(buttons_row)

        

    def help(self, ev):
        print("will do help here")

    def cmp(self, ev):
        pass
    
ft.app(MyApp().setup)
