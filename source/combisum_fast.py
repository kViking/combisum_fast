import pyperclip
import flet as ft
from combimath import combisum
from flet_core.control_event import ControlEvent
from flet import (
    Page,
    Row,
    Text,
    Card,
    Column,
    TextField,
    TextButton,
    TextThemeStyle,
    ElevatedButton,
    IconButton,
    MainAxisAlignment,
    CrossAxisAlignment,
)

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
    # Set page properties
    page.title = "Combisum GPU.0"
    page.vertical_alignment = MainAxisAlignment.START
    page.horizontal_alignment = CrossAxisAlignment.CENTER

    # Create result_text column to display results
    result_text = Column(expand=True, horizontal_alignment=CrossAxisAlignment.CENTER, alignment=MainAxisAlignment.CENTER)

    results = []
    history = []
    error = Text("", color=ft.colors.RED)
    info_modal = ft.AlertDialog(
        title=Text("Info"),
        content=Column([]),
        actions=[TextButton("Close", on_click=lambda e: page.close(info_modal))],
    )

    def toggle_dark_mode(event: ControlEvent) -> None:
        # Toggle dark mode
        page.theme_mode = ft.ThemeMode.DARK if page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
        page.update()

    dark_mode_button = ft.IconButton(icon=ft.icons.LIGHT_MODE, tooltip="Toggle dark mode", on_click=toggle_dark_mode)

    def copy_results(event: ControlEvent) -> None:
        # Copy results to clipboard as .tsv raw values
        tsv = "\n".join(["\t".join([str(y) for y in x]) for x in results[0]])
        pyperclip.copy(tsv)

    def load_history(event: ControlEvent) -> None:
        nonlocal target_text, array_text, results, history, error
        
        # Load selected history item into input fields
        target_text.value = event.control.text.split(" | ")[0]
        array_text.value = event.control.text.split(" | ")[1]
        results = []
        run(event)
        page.update()

    copy_button = IconButton(
        icon=ft.icons.CONTENT_COPY, 
        on_click=copy_results,
        tooltip="Copy all results to clipboard as .tsv raw values",
        visible=False)
    
    cpu_mode = ft.Checkbox("CPU mode", value=False, tooltip="Run on CPU instead of GPU")
    
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
            Text(x[0], 
                theme_style=TextThemeStyle.BODY_MEDIUM,
                text_align=ft.TextAlign.CENTER, 
                expand=True) for x in result_formatted
            ] + [Text(f"...and {len(results[0]) - 5} more") if len(results[0]) > 5 else Text("")]
        error.value = results[1].get("error", "")
        copy_button.visible = True

        info_modal.content.controls = [Text(f"{x}: {results[1].get(x)}") for x in results[1]]

        history.append(
            {
            "target": target_text.value,
            "array": array_text.value,
            "results": results
            }
        )
        history_view.controls = [HistoryItem(target=x.get('target'), array=x.get('array'), results=x.get("results"), on_click_function=load_history) for x in list(reversed(history))]
        for item in history_view.controls:
            if not item.results[0]:
                item.style = ft.ButtonStyle(color=ft.colors.RED)
            else:
                item.style = ft.ButtonStyle(color=ft.colors.ON_PRIMARY_CONTAINER)

        page.update()

    # Create input fields and buttons
    target_text = TextField(value="25.43", on_submit=run)
    array_text = TextField(value="12.85 3.14 5.43 4.56 12.58", on_submit=run)
    button = ElevatedButton("run", on_click=run)
    history_view = Column(
        [],
        expand=True,
        scroll=ft.ScrollMode.ALWAYS,
        horizontal_alignment=CrossAxisAlignment.START,
        alignment=MainAxisAlignment.START
    )
    
    # Create page layout
    page_layout = Column(
        [
            Row(
                [
                    dark_mode_button
                ], expand=True,
                alignment=MainAxisAlignment.END
            ),
            Row(
                [
                    Column(
                        [
                            Card(
                                content=Column(
                                    [
                                        Text('Input', 
                                             expand=True, 
                                             theme_style=TextThemeStyle.DISPLAY_SMALL, 
                                             text_align=ft.TextAlign.LEFT),
                                        target_text,
                                        array_text,
                                        Row(
                                            [
                                                cpu_mode,
                                                button
                                            ], expand=True,
                                            alignment=MainAxisAlignment.END
                                        ),
                                    ], expand=True,
                                    alignment=MainAxisAlignment.START,
                                ), expand=True,
                            ),
                            Row(
                                [Card(
                                    content=Column(
                                        [
                                            Text('History', 
                                                theme_style=TextThemeStyle.DISPLAY_SMALL, 
                                                text_align=ft.TextAlign.LEFT, 
                                                expand=True),
                                            history_view
                                        ], expand=True,
                                        alignment=MainAxisAlignment.START,
                                    ), expand=True,
                                )],
                                expand=True,
                                alignment=MainAxisAlignment.START,
                                vertical_alignment=CrossAxisAlignment.START
                            )
                        ], expand=True,
                    ),
                    Column(
                        [Card(
                            content=Column(
                                [
                                    Text('Results', 
                                         theme_style=TextThemeStyle.DISPLAY_SMALL, 
                                         text_align=ft.TextAlign.LEFT),
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
                                            copy_button,
                                            IconButton(
                                                icon=ft.icons.INFO, 
                                                on_click=lambda e: page.open(info_modal),
                                                tooltip="View error details"
                                            )
                                        ], expand=True,
                                        alignment=MainAxisAlignment.END
                                    )
                                ], expand=True,
                                alignment=MainAxisAlignment.START
                            )
                        )], expand=True,
                        alignment=MainAxisAlignment.START
                    )
                    
                ], expand=True,
                vertical_alignment=CrossAxisAlignment.START
            )
        ],
        alignment=MainAxisAlignment.SPACE_AROUND
    )

    page.add(page_layout)

if __name__ == "__main__":
    ft.app(main)
