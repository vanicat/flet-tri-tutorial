from collections.abc import Sequence
import flet as ft
import random

class IconGenerator:
    ICONS = (
        ft.icons.ABC,
        ft.icons.ACCESS_ALARM,
        ft.icons.ACCOUNT_BALANCE,
        ft.icons.ADD,
        ft.icons.AIRLINE_STOPS,
        ft.icons.DANGEROUS,
        ft.icons.WARNING,
        ft.icons.ERROR,
        ft.icons.JOIN_FULL,
        ft.icons.BACKPACK,
        ft.icons.CALCULATE,
        ft.icons.DELETE,
        ft.icons.DIAMOND,
        ft.icons.MOVING
    )

    def __init__(self, nb:int) -> None:
        self.order = random.sample(range(len(self.ICONS)), nb)

    def get_std(self, v: int) -> str:
        if v == -1:
            return ft.icons.DO_NOT_DISTURB
        return self.ICONS[self.order[v]]
    
    def get_outlined(self, v: int) -> str:
        if v == -1:
            return ft.icons.DO_NOT_DISTURB_OUTLINED
        return self.ICONS[self.order[v]] + "_outlined"

class MyConteneur:
    def __init__(self, numicon:int, app:"MyApp", draggable = True, permutable = True) -> None:
        self.inserable = False
        self.cont = ft.Container()
        self._app = app
        self.draggable = draggable
        self.permutable = permutable
        self.numicon = numicon
        self.selected = False

    @property
    def selected(self):
        return self._button.selected

    @selected.setter
    def selected(self, v:bool):
        self._button.selected = v
        self._app.page.update()

    @property
    def numicon(self):
        return self._numicon
    
    @numicon.setter
    def numicon(self, num:int) -> None:
        self._numicon = num
        self._button = ft.IconButton(
            icon = self._app.icons.get_std(num),
            selected=False,
            selected_icon=self._app.icons.get_outlined(num),
            on_click=self.on_click)
        if self.draggable:
            target_content = ft.Draggable(
                group="icone",
                content=self._button,
                data=self
            )
        else:
            target_content = self._button
        self.cont.content = ft.DragTarget(
            group="icone",
            on_accept=self.on_accept_drag,
            content = target_content
        )
        
        self._app.page.update()
        
    def on_click(self, ev):
        self.selected = not self.selected

    def on_accept_drag(self, ev:ft.DragTargetAcceptEvent):
        ctrl = self._app.page.get_control(ev.src_id)
        assert ctrl is not None, "event on non existing control"
        src = ctrl.data
        if self.permutable:
            src.numicon, self.numicon = self.numicon, src.numicon
        else:
            self.numicon = src.numicon

class NoApp:
    def update(self):
        pass

    def get_control(self, id):
        assert False, "Intialisation of page not done yet"

class MyApp:
    def __init__(self, nb:int) -> None:
        self.page = NoApp()
        self.icons = IconGenerator(nb)
        self.position = random.sample(range(nb), nb)
        self.contents = tuple((
            MyConteneur(i, self) for i in self.position
        ))

    def setup(self, page: ft.Page) -> None:
        self.page = page
        page.add(ft.SafeArea(ft.Text("Trouver un algorithme de tri")))
        buttons_row = ft.Row([
            ft.TextButton("aide", on_click=self.help),
            ft.TextButton("cmp", on_click=self.cmp)
        ])
        page.add(buttons_row)
        self._message = ft.Text()
        page.add(ft.SafeArea(self._message))
        page.add(ft.Row([
            ic.cont for ic in self.contents
        ]))
        
    @property
    def message(self):
        return self._message.value
    
    @message.setter
    def message(self, newvalue:str):
        self._message.value = newvalue
        self.page.update()
        

    def help(self, ev):
        print("will do help here")

    @property
    def selected(self):
        return [
            ic for ic in self.contents if ic.selected
        ]

    def cmp(self, ev):
        selected = self.selected
        if len(selected) != 2:
            self.message = "selectionne deux icônes pour les comparer"
            return
        
        a, b = selected
        if a.numicon < b.numicon:
            self.message = "le premier est plus petit que le deuxième"
        else:
            self.message = "le deuxième est plus petit que le premier"
    
ft.app(MyApp(10).setup)
