import flet as ft
from mainCLI import hash_file, compare_hashes, save_baseline, load_baseline, check_for_changes


def main(page: ft.Page): 
    page.title = "File Integrity Monitor"
    page.window_width = 600
    page.window_height = 400
    page.theme_mode = ft.ThemeMode.LIGHT

    # Variable to store selected file path
    selected_file_path = ""

    # Text to display selected file
    file_display = ft.Text(
        "No file selected",
        size=14,
        color=ft.Colors.GREY_600,
    )

    result_display = ft.Text(
        "Result: ",
        size=14,
        color=ft.Colors.GREY_600,
    )

    original_hash_display = ft.Text(
        "Original Hash: ",
        size=14,
        color=ft.Colors.GREY_600,
    )

    current_hash_display = ft.Text(
        "Current Hash: ",
        size=14,
        color=ft.Colors.GREY_600,
    )

    # Callback function for when file is selected
    def file_picker_result(e: ft.FilePickerResultEvent):
        nonlocal selected_file_path
        if e.files:
            selected_file_path = e.files[0].path
            file_display.value = f"Selected: {selected_file_path}"
            result = check_for_changes(selected_file_path)
            if result["status"] == "unchanged":
                result_display.value = "Result: Unchanged"
                original_hash_display.value = f"Original Hash: {result['original_hash']}"
                current_hash_display.value = f"Current Hash: {result['current_hash']}"
            elif result["status"] == "modified":
                result_display.value = "Result: Modified"
                original_hash_display.value = f"Original Hash: {result['original_hash']}"
                current_hash_display.value = f"Current Hash: {result['current_hash']}"
            elif result["status"] == "added_to_baseline":
                result_display.value = "Result: Added to Baseline"
                current_hash_display.value = f"Current Hash: {result['current_hash']}"
        else:
            file_display.value = "No file selected"
            result_display.value = "Result: "
            original_hash_display.value = "Original Hash: "
            current_hash_display.value = "Current Hash: "
        page.update()

    # Create the file picker
    file_picker = ft.FilePicker(on_result=file_picker_result)
    page.overlay.append(file_picker)

    # Title container
    title = ft.Container(
        content=ft.Text(
            "File Integrity Monitor",
            size=30,
            weight=ft.FontWeight.BOLD,
            font_family="Inter",
            color=ft.Colors.BLACK,
            text_align=ft.TextAlign.CENTER,
        ),
        alignment=ft.alignment.center,
        width=None,
    )

    # Browse button
    browse_button = ft.ElevatedButton(
        "Browse for File",
        icon=ft.Icons.FOLDER_OPEN,
        on_click=lambda _: file_picker.pick_files()
    )

    # Add all components to page
    page.add(
        title,
        browse_button,
        file_display,
        result_display,
        original_hash_display,
        current_hash_display
    )

ft.app(target=main)