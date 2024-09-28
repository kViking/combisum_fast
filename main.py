import pyperclip
import flet as ft
from combisum import combisum
from flet_core.control_event import ControlEvent
from flet import (
    Row,
    Page,
    Text,
    Card,
    Column,
    Container,
    TextField,
    TextAlign,
    TextButton,
    IconButton,
    TextThemeStyle,
    ElevatedButton,
    MainAxisAlignment,
    CrossAxisAlignment,
)

splash_good = False
try:
    import pyi_splash as splash # type: ignore

    splash.update_text("Combisum GPU.0")
    splash_good = True
except ImportError:
    pass

# Create history item class
class HistoryItem(TextButton):
    def __init__(self, target: str, array: str, results, on_click_function) -> None:
        super().__init__()
        self.target = target
        self.array = array
        self.results = results
        self.on_click = on_click_function
        self.text = f"{self.target} | {self.array}"    
        self.tooltip = "Re-run this calculation"


def main(page: Page) -> None:
    if splash_good:
        splash.close()

    # Set page properties
    page.title = "Combisum GPU.0"
    page.vertical_alignment = MainAxisAlignment.START
    page.horizontal_alignment = CrossAxisAlignment.CENTER


    # Set up variables
    results = []
    history = []

    # Error display
    error = Text("")
    error_button = IconButton(
        icon=ft.icons.ERROR, 
        tooltip="Display error info", 
        on_click=lambda e: page.open(error_modal),
        style=ft.ButtonStyle(color=ft.colors.RED),
        visible=False
    )

    def close_error_modal(event: ControlEvent) -> None:
        page.close(error_modal)

    error_modal = ft.AlertDialog(
        title=Text("Error"),
        content=Column([
            error
        ]),
        actions=[TextButton("Close", on_click=close_error_modal)]
    )



    # Create result_text and info_modal variables to update later
    result_text = Column(expand=True, horizontal_alignment=CrossAxisAlignment.CENTER, alignment=MainAxisAlignment.CENTER)

    def close_info_modal(event: ControlEvent) -> None:
        page.close(info_modal)

    info_modal = ft.AlertDialog(
        title=Text("Info"),
        content=Column([]),
        actions=[TextButton("Close", on_click=close_info_modal)]
    )


    # Define buttons and button callbacks

    def toggle_dark_mode(event: ControlEvent) -> None:
        # Toggle dark mode
        page.theme_mode = ft.ThemeMode.DARK if page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
        page.update()

    dark_mode_button = ft.IconButton(icon=ft.icons.LIGHT_MODE, tooltip="Toggle dark mode", on_click=toggle_dark_mode)

    def copy_results(event: ControlEvent) -> None:
        # Copy results to clipboard as .tsv raw values
        tsv = "\n".join(["\t".join([str(y) for y in x]) for x in results[0]])
        pyperclip.copy(tsv)

    copy_button = IconButton(
        icon=ft.icons.CONTENT_COPY, 
        on_click=copy_results,
        tooltip="Copy all results to clipboard as .tsv raw values",
        visible=False)

    def load_history(event: ControlEvent) -> None:
        nonlocal target_text, array_text, results, history, error
        
        # Load selected history item into input fields
        target_text.value = event.control.text.split(" | ")[0]
        array_text.value = event.control.text.split(" | ")[1]
        results = []
        run(event)
        page.update()
    
    cpu_mode = ft.Checkbox("CPU only", value=False, tooltip="Restrict to CPU computation")
    
    def run(event: ControlEvent) -> None:
        nonlocal result_text, results, history, error

        # Get target value and array from input fields
        target = float(target_text.value)
        array = array_text.value.replace(",", "")
        array = [float(x) for x in array.split()]
        result_text.controls = [Text('beep boop', color=ft.colors.GREEN)]
        page.update()

        # Calculate combisum and format results
        results = combisum(target, array, cpu_mode.value)
        result_formatted = [[', '.join(str(y) for y in x)] for x in results[0][:5]]

        result_text.controls = [
                TextButton(text=x[0],
                    on_click=lambda e: pyperclip.copy("\t".join(x[0].split(", "))),
                    tooltip="Copy this combination to clipboard",
                    style=ft.ButtonStyle(color=ft.colors.ON_PRIMARY_CONTAINER)
                ) for x in result_formatted
            ] + [Text(f"...and {len(results[0]) - 5} more") if len(results[0]) > 5 else Text("")]
        
        error.value = results[1].get("error", "")
        error_button.visible = bool(error.value)
        copy_button.visible = bool(results[0])

        info_modal.content.controls = [Text(f"{x}: {results[1].get(x)}") for x in results[1]]

        history.append(
            {
            "target": target_text.value,
            "array": array_text.value,
            "results": results
            }
        )
        
        history_card.visible = True
        history_view.controls = [
            HistoryItem(target=x.get('target'), 
                        array=x.get('array'), 
                        results=x.get("results"), 
                        on_click_function=load_history
            ) for x in list(reversed(history))]

        for item in history_view.controls:
            if not item.results[0]:
                item.style = ft.ButtonStyle(color=ft.colors.RED)
            else:
                item.style = ft.ButtonStyle(color=ft.colors.ON_PRIMARY_CONTAINER)

        page.update()

    # Create input fields and buttons
    target_text = TextField(value="25.43", on_submit=run)
    array_text = TextField(value="12.85 3.14 5.43 4.56 12.58", on_submit=run)
    button = ElevatedButton("Run", on_click=run)
    history_view = Column(
        expand=True,
        scroll=ft.ScrollMode.ALWAYS,
        horizontal_alignment=CrossAxisAlignment.START,
        alignment=MainAxisAlignment.START,
        controls=[]
    )
    
    input_card = Card(
        content=Container(
            expand=True,
            padding=12,
            content=Column(
                expand=True,
                alignment=MainAxisAlignment.START,
                controls=[
                    Text('Input', 
                        expand=True, 
                        theme_style=TextThemeStyle.DISPLAY_SMALL, 
                        text_align=TextAlign.LEFT),
                    target_text,
                    array_text,
                    Row(
                        expand=True,
                        alignment=MainAxisAlignment.END,
                        controls=[
                            cpu_mode,
                            button
                        ]
                    )
                ]
            )
        )
    )

    history_card = Card(
        expand=True,
        visible=False,
        content=Container(
            expand=True,
            padding=12,
            content=Column(
                expand=True,
                alignment=MainAxisAlignment.START,
                controls=[
                    Text('History', 
                        theme_style=TextThemeStyle.DISPLAY_SMALL, 
                        text_align=TextAlign.LEFT, 
                        expand=True),
                    history_view
                ]
            )
        )
    )

    results_card = Card(
        content=Container(
            expand=True,
            padding=12,
            content=Column(
                expand=True,
                controls=[
                    Row(
                        expand=True,
                        controls=[
                            error_button,
                            Text('Results', 
                            theme_style=TextThemeStyle.DISPLAY_SMALL, 
                            text_align=TextAlign.LEFT,
                            expand=True),
                            copy_button
                        ]
                    ),
                    Row(
                        expand=True,
                        alignment=MainAxisAlignment.START,
                        vertical_alignment=CrossAxisAlignment.START,
                        controls=[
                            result_text,
                        ]
                    ),
                    Row(
                        expand=True,
                        alignment=MainAxisAlignment.END,
                        controls=[
                            IconButton(
                                icon=ft.icons.CODE, 
                                on_click=lambda e: page.open(info_modal),
                                tooltip="Get debug info"
                            )
                        ]
                    )
                ]
            )
        )
    )           

    page_layout = ft.SafeArea(
        Column(
            alignment=MainAxisAlignment.SPACE_AROUND,
            controls=[
                Row(
                    expand=True,
                    alignment=MainAxisAlignment.END,
                    controls=[
                        dark_mode_button
                    ]
                ),
                Row(
                    vertical_alignment=CrossAxisAlignment.START,
                    expand=True,
                    controls=[
                        Column(
                            expand=True,
                            controls=[
                                input_card,
                                Row(
                                    expand=True,
                                    alignment=MainAxisAlignment.START,
                                    vertical_alignment=CrossAxisAlignment.START,
                                    controls=[history_card]
                                )
                            ]
                        ),
                        Column(
                            expand=True,
                            alignment=MainAxisAlignment.START,
                            controls=[results_card]
                        )                        
                    ] 
                )
            ]
        )
    )

    page.add(page_layout)

if __name__ == "__main__":
    ft.app(main)
