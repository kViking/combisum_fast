import flet as ft
from combimath import combisum
from flet_core.control_event import ControlEvent
from flet import (
    Page,
    Row,
    Column,
    Text,
    TextField,
    TextThemeStyle,
    ElevatedButton,
    Divider,
    IconButton,
    MainAxisAlignment,
    CrossAxisAlignment,
)
import pyperclip

def main(page: Page) -> None:
    page.title = "FFFFFFFFFFFF"
    page.vertical_alignment = MainAxisAlignment.START
    page.horizontal_alignment = CrossAxisAlignment.CENTER

    target_text = TextField(value="25.43")
    array_text = TextField(value="12.85 3.14 5.43 4.56 12.58")
    result_text = Column(expand=1)

    results = []
    error = Text("", color=ft.colors.RED)

    def copy_results(event: ControlEvent) -> None:
        pyperclip.copy("\n".join(["\t".join([str(y) for y in x]) for x in results[0]]))
        print(results[0])

    copy_button = IconButton(
        icon=ft.icons.CONTENT_COPY, 
        on_click=copy_results,
        tooltip="Copy results to clipboard",
        visible=False)
    
    def run(event: ControlEvent) -> None:
        nonlocal result_text, results
        target = float(target_text.value)
        array = array_text.value.replace(",", "")
        array = [float(x) for x in array.split()]
        result_text.value = "beep boop"
        page.update()

        results = combisum(target, array)
        result_text.controls = [Text(x, theme_style=TextThemeStyle.BODY_SMALL) for x in results[0]]
        error.value = results[1].get("error", "")
        copy_button.visible = True  
        page.update()

    button = ElevatedButton("run", on_click=run)
    
    page_layout = Column(
        [
            Row([Text("Title", theme_style=TextThemeStyle.DISPLAY_LARGE)],alignment=MainAxisAlignment.START),
            Divider(),
            Row(
                [
                    Text('input _', expand=1),
                    copy_button
                ]
            ),
            Row(
                [
                    Column(
                        [
                            target_text,
                            array_text,
                            button
                        ], expand=1,
                        horizontal_alignment=CrossAxisAlignment.CENTER
                    ),
                    Column(
                        [
                            error,
                            result_text
                        ], expand=1,
                        horizontal_alignment=CrossAxisAlignment.CENTER
                    )
                ], expand=1
            )
        ]
    )

    page.add(page_layout)

if __name__ == "__main__":
    ft.app(main)
