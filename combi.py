import flet as ft
from combimath import combisum

import logging

#Set up logging with logfile and stdout
formatting = logging.Formatter('%(process)d %(asctime)s %(levelname)s %(funcName)s[%(lineno)s]: %(message)s')
logging.basicConfig(level=logging.INFO, filename='combi.log', filemode='w')
file_handler = logging.FileHandler('combi.log')
file_handler.setFormatter(formatting)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatting)
logger = logging.getLogger(__name__)
logger.addHandler(stream_handler)
logger.addHandler(file_handler)


class CombisumApp(ft.Column):
    def __init__(self):
        super().__init__()
        self.target = '0'
        self.numbers = '0'
        self.results = []
        self.flag = {
            "cuda": None,
            "max_length": None,
            "combo_length": None,
            "target": None,
            "numbers": None,
            "error": None
        }
        self.error = ft.Text(f"Error occurred", theme_style=ft.TextThemeStyle.DISPLAY_SMALL, visible=False)
        self.input_panel = ft.Column(
            [
                ft.Text("Input _", theme_style=ft.TextThemeStyle.DISPLAY_SMALL),
                ft.TextField(
                    label="Target",
                    on_change=self.target_changed,
                    on_submit=self.combisum
                ),
                ft.TextField(
                    label="Numbers",
                    on_change=self.numbers_changed
                ),
                ft.ElevatedButton(
                    "Run",
                    on_click=self.combisum
                )
            ], expand=1
        )

        self.output_panel = ft.Column(
            [
                ft.Text("Results", theme_style=ft.TextThemeStyle.DISPLAY_SMALL),
                self.error,
                ft.Text("Flag")
            ], expand=1
        )

        self.controls = [
            ft.Row([ft.Text("CombiSum", theme_style=ft.TextThemeStyle.DISPLAY_LARGE)]),
            ft.Divider(),
            ft.Row([self.input_panel, self.output_panel], vertical_alignment=ft.CrossAxisAlignment.START)
        ]

    def target_changed(self, e):
        self.target = e.control.value
        self.update()
    
    def numbers_changed(self, e):
        self.numbers = e.control.value
        self.update()

    def combisum(self, e):
        t_target = float(self.target)
        t_numbers = [float(x) for x in self.numbers.split(' ')]

        self.results, self.flag = combisum(t_target, t_numbers)

        if self.flag['error']:
            self.error.visible = True
            self.error.value = f"Error occurred: {self.flag['error']}"
        
        self.update()


#Define base page
def main(page: ft.Page):
    page.title = "CombiSum App"
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.vertical_alignment = ft.CrossAxisAlignment.START
    page.update()

    app = CombisumApp()
    
    page.add(app)


#Run the app
ft.app(target=main)