import pyperclip
import matplotlib as mpl
import flet as ft
from combimath import combisum
from flet_core.control_event import ControlEvent
from flet import (
    Page,
    Row,
    Column,
    Text,
    TextField,
    TextButton,
    TextThemeStyle,
    ElevatedButton,
    IconButton,
    MainAxisAlignment,
    CrossAxisAlignment,
)

def main(page: Page) -> None:
    # Set page properties
    page.title = "Combisum GPU.0"
    page.vertical_alignment = MainAxisAlignment.START
    page.horizontal_alignment = CrossAxisAlignment.CENTER

    mpl.use("svg")

    # Create result_text column to display results
    result_text = Column(expand=True, horizontal_alignment=CrossAxisAlignment.CENTER, alignment=MainAxisAlignment.CENTER)

    results = []
    history = []
    error = Text("", color=ft.colors.RED)

    def copy_results(event: ControlEvent) -> None:
        # Copy results to clipboard as .tsv raw values
        tsv = "\n".join(["\t".join([str(y) for y in x]) for x in results[0]])
        pyperclip.copy(tsv)
        print(tsv)

    def load_history(event: ControlEvent) -> None:
        nonlocal target_text, array_text, results, history, error
        
        # Load selected history item into input fields
        target_text.value = event.control.text.split(" | ")[0]
        array_text.value = event.control.text.split(" | ")[1]
        results = []
        page.update()

    copy_button = IconButton(
        icon=ft.icons.CONTENT_COPY, 
        on_click=copy_results,
        tooltip="Copy all results to clipboard as .tsv raw values",
        visible=False)
    
    def run(event: ControlEvent) -> None:
        nonlocal result_text, results, history, error

        # Get target value and array from input fields
        target = float(target_text.value)
        array = array_text.value.replace(",", "")
        array = [float(x) for x in array.split()]
        result_text.controls = [Text('beep boop', color=ft.colors.GREEN)]
        page.update()

        # Calculate combisum and format results
        results = combisum(target, array)
        result_formatted = [[', '.join(str(y) for y in x)] for x in results[0][:5]]
        print(result_formatted)
        result_text.controls = [
            Text(x[0], 
                theme_style=TextThemeStyle.BODY_MEDIUM,
                text_align=ft.TextAlign.CENTER, 
                expand=True) for x in result_formatted
            ] + [Text(f"...and {len(results[0]) - 5} more") if len(results[0]) > 5 else Text("")]
        error.value = results[1].get("error", "")
        copy_button.visible = True  
        history.insert(
            0, {
            "target": target_text.value,
            "array": array_text.value,
            "results": results
            }
        )
        history_view.controls = [TextButton(text=f'{x["target"]} | {x["array"]}', on_click=load_history) for x in history]
        page.update()

    # Create input fields and buttons
    target_text = TextField(value="25.43", on_submit=run)
    array_text = TextField(value="12.85 3.14 5.43 4.56 12.58", on_submit=run)
    button = ElevatedButton("run", on_click=run)
    history_view = Column(
        [],
        expand=True,
        scroll=ft.ScrollMode.ALWAYS,
        horizontal_alignment=CrossAxisAlignment.CENTER,
        alignment=MainAxisAlignment.START
    )
    
    # Create page layout
    page_layout = Column(
        [
            Row(
                [
                    Text('Input', expand=True, theme_style=TextThemeStyle.DISPLAY_SMALL),
                ], expand=True
            ),
            Row(
                [
                    Column(
                        [
                            target_text,
                            array_text,
                            button,
                            history_view
                        ], expand=True,
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                        alignment=MainAxisAlignment.START
                    ),
                    Column(
                        [
                            Row(
                                [
                                    error,
                                ], expand=True,
                                alignment=MainAxisAlignment.CENTER
                            ),
                            Row(
                                [
                                    result_text,
                                ], expand=True,
                                alignment=MainAxisAlignment.CENTER
                            ),
                            Row(
                                [
                                    copy_button
                                ], expand=True,
                                alignment=MainAxisAlignment.END
                            )
                        ], expand=True,
                        scroll=ft.ScrollMode.ALWAYS,
                        horizontal_alignment=CrossAxisAlignment.CENTER
                    )
                    
                ], expand=True,
                tight=True,
            )
        ]
    )

    page.add(page_layout)

if __name__ == "__main__":
    ft.app(main)
