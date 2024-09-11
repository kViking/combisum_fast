import pyperclip
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
    IconButton,
    MainAxisAlignment,
    CrossAxisAlignment,
)

def main(page: Page) -> None:
    page.title = "Combisum GPU.0"
    page.vertical_alignment = MainAxisAlignment.START
    page.horizontal_alignment = CrossAxisAlignment.CENTER

    result_text = Column(expand=1, horizontal_alignment=CrossAxisAlignment.CENTER, alignment=MainAxisAlignment.CENTER)

    results = []
    error = Text("", color=ft.colors.RED)

    def copy_results(event: ControlEvent) -> None:
        pyperclip.copy("\n".join(["\t".join([str(y) for y in x]) for x in results[0][:15]]))
        print(results[0])

    copy_button = IconButton(
        icon=ft.icons.CONTENT_COPY, 
        on_click=copy_results,
        tooltip="Copy all results to clipboard as .tsv raw values",
        visible=False)
    
    def run(event: ControlEvent) -> None:
        nonlocal result_text, results
        target = float(target_text.value)
        array = array_text.value.replace(",", "")
        array = [float(x) for x in array.split()]
        result_text.controls = [Text('beep boop', color=ft.colors.GREEN)]
        page.update()

        results = combisum(target, array)
        result_formatted = [[', '.join(str(y) for y in x)] for x in results[0][:15]]
        print(result_formatted)
        result_text.controls = [
            Text(x[0], 
                theme_style=TextThemeStyle.BODY_MEDIUM,
                text_align=ft.TextAlign.CENTER, 
                expand=True) for x in result_formatted
            ]
        error.value = results[1].get("error", "")
        copy_button.visible = True  
        page.update()

    target_text = TextField(value="25.43", on_submit=run)
    array_text = TextField(value="12.85 3.14 5.43 4.56 12.58", on_submit=run)
    button = ElevatedButton("run", on_click=run)
    
    page_layout = Column(
        [
            Row(
                [
                    Text('Input', expand=1, theme_style=TextThemeStyle.DISPLAY_SMALL),
                ],
            ),
            Row(
                [
                    Column(
                        [
                            target_text,
                            array_text,
                            button
                        ], expand=1,
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                        alignment=MainAxisAlignment.START
                    ),
                    Column(
                        [
                            Row(
                                [
                                    error,
                                ], expand=1,
                                alignment=MainAxisAlignment.CENTER
                            ),
                            Row(
                                [
                                    result_text,
                                ], expand=1,
                                alignment=MainAxisAlignment.CENTER
                            ),
                            Row(
                                [
                                    copy_button
                                ], expand=1,
                                alignment=MainAxisAlignment.END
                            )
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
