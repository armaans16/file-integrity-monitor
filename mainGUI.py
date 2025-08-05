import flet as ft
from mainCLI import hash_file, compare_hashes, save_baseline, load_baseline, check_for_changes
import json

def main(page: ft.Page): 
    page.title = "File Integrity Monitor"
    page.window_width = 800
    page.window_height = 600
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 10

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
                result_display.color = ft.Colors.GREEN_600
                original_hash_display.value = f"Original Hash: {result['original_hash']}"
                current_hash_display.value = f"Current Hash: {result['current_hash']}"
            elif result["status"] == "modified":
                result_display.value = "Result: Modified"
                result_display.color = ft.Colors.RED_600
                original_hash_display.value = f"Original Hash: {result['original_hash']}"
                current_hash_display.value = f"Current Hash: {result['current_hash']}"
            elif result["status"] == "added_to_baseline":
                result_display.value = "Result: Added to Baseline"
                result_display.color = ft.Colors.BLUE_600
                current_hash_display.value = f"Current Hash: {result['current_hash']}"
                original_hash_display.value = "Original Hash: N/A"
                update_baseline_display()
        else:
            file_display.value = "No file selected"
            result_display.value = "Result: "
            result_display.color = ft.Colors.GREY_600
            original_hash_display.value = "Original Hash: "
            current_hash_display.value = "Current Hash: "
        page.update()

    # Function to clear all UI elements
    def clear_all():
        nonlocal selected_file_path
        selected_file_path = ""
        file_display.value = "No file selected"
        result_display.value = "Result: "
        result_display.color = ft.Colors.GREY_600
        original_hash_display.value = "Original Hash: "
        current_hash_display.value = "Current Hash: "
        page.update()
    
    def remove_from_baseline(e: ft.FilePickerResultEvent):
        nonlocal selected_file_path
        if e.files:
            selected_file_path = e.files[0].path
            baseline = load_baseline()
            if selected_file_path in baseline:
                del baseline[selected_file_path]
                with open('baseline.json', 'w') as file:
                    json.dump(baseline, file, indent=2)
        file_display.value = "File removed from baseline"
        result_display.value = "Result: Removed from Baseline"
        original_hash_display.value = "Original Hash: "
        current_hash_display.value = "Current Hash: "
        update_baseline_display()
        page.update()

    # Function to update baseline display
    def update_baseline_display():
        baseline = load_baseline()
        baseline_controls.clear()
        
        if not baseline:
            baseline_controls.append(
                ft.Text(
                    "No files in baseline",
                    size=14,
                    color=ft.Colors.GREY_500,
                    italic=True,
                )
            )
        else:
            for file_path, file_hash in baseline.items():
                # Create a container for each baseline entry
                entry_container = ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text(
                                f"File: {file_path}",
                                size=12,
                                weight=ft.FontWeight.W_500,
                                color=ft.Colors.BLACK87,
                            ),
                            ft.Text(
                                f"Hash: {file_hash}",
                                size=11,
                                color=ft.Colors.GREY_600,
                                font_family="monospace",
                            ),
                        ],
                        spacing=4,
                    ),
                    padding=ft.padding.all(8),
                    margin=ft.margin.only(bottom=8),
                    bgcolor=ft.Colors.GREY_50,
                    border=ft.border.all(1, ft.Colors.GREY_200),
                    border_radius=ft.border_radius.all(6),
                )
                baseline_controls.append(entry_container)
        
        baseline_column.controls = baseline_controls
        page.update()

    # Create baseline display components
    baseline_controls = []
    baseline_column = ft.Column(
        controls=[],
        spacing=8,
        scroll=ft.ScrollMode.AUTO,
    )

    # Create the file picker
    file_picker = ft.FilePicker(on_result=file_picker_result)
    page.overlay.append(file_picker)

    file_deleter = ft.FilePicker(on_result=remove_from_baseline)
    page.overlay.append(file_deleter)

    # Title container
    title = ft.Container(
        content=ft.Text(
            "File Integrity Monitor",
            size=32,
            weight=ft.FontWeight.BOLD,
            font_family="Inter",
            color=ft.Colors.BLACK,
            text_align=ft.TextAlign.CENTER,
        ),
        alignment=ft.alignment.center,
        margin=ft.margin.only(bottom=15),
    )

    # Browse button
    browse_button = ft.ElevatedButton(
        "Browse for File",
        icon=ft.Icons.FOLDER_OPEN,
        on_click=lambda _: file_picker.pick_files(),
        style=ft.ButtonStyle(
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.BLUE_600,
        )
    )

    # clear button
    clear_button = ft.ElevatedButton(
        "Clear current file",
        icon=ft.Icons.DELETE,
        on_click=lambda _: clear_all(),
        style=ft.ButtonStyle(
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.RED_600,
        )
    )

    remove_from_baseline_button = ft.ElevatedButton(
        "Remove file from Baseline",
        icon=ft.Icons.DELETE,
        on_click=lambda _: file_deleter.pick_files(),
        style=ft.ButtonStyle(
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.RED_600,
        )
    )

    # Main content container - this groups all the main functionality
    main_content = ft.Container(
        content=ft.Column(
            controls=[
                # File selection section
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text(
                                "Select File to Monitor",
                                size=18,
                                weight=ft.FontWeight.W_500,
                                color=ft.Colors.BLACK87,
                            ),
                            ft.Row(
                                controls=[
                                    browse_button,
                                    ft.Text(
                                        "New files will be added to baseline",
                                        size=11,
                                        color=ft.Colors.GREY_500,
                                        italic=True,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                spacing=10,
                            ),
                            clear_button,
                            remove_from_baseline_button,
                            file_display,
                        ],
                        spacing=10,
                    ),
                    padding=ft.padding.all(15),
                    margin=ft.margin.only(bottom=5),
                ),
                
                # Divider
                ft.Divider(color=ft.Colors.GREY_300, height=1),
                
                # Results section
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text(
                                "Integrity Check Results",
                                size=18,
                                weight=ft.FontWeight.W_500,
                                color=ft.Colors.BLACK87,
                            ),
                            result_display,
                            original_hash_display,
                            current_hash_display,
                        ],
                        spacing=8,
                    ),
                    padding=ft.padding.all(20),
                ),

                # Divider
                ft.Divider(color=ft.Colors.GREY_300, height=1),

                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text("Current Baseline", size=18, weight=ft.FontWeight.W_500, color=ft.Colors.BLACK87),
                            ft.Container(
                                content=baseline_column,
                                height=150,
                                padding=ft.padding.all(10),
                                bgcolor=ft.Colors.WHITE,
                                border=ft.border.all(1, ft.Colors.GREY_300),
                                border_radius=ft.border_radius.all(8),
                            ),
                        ],
                        spacing=10,
                    ),
                    padding=ft.padding.all(20),
                )
            ],
            spacing=0,
        ),
        # Container styling
        bgcolor=ft.Colors.WHITE,
        border=ft.border.all(1, ft.Colors.GREY_300),
        border_radius=ft.border_radius.all(12),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=8,
            color=ft.Colors.BLACK12,
            offset=ft.Offset(0, 2),
        ),
        padding=0,  # Padding is handled by inner containers
    )

# Structure of the main_content container for understanding the layout
#main_content (Container) - The "card"
#├── Column - Vertical layout
#    ├── File Section (Container) - "Box 1"
#    │   └── Column - Elements in box 1
#    ├── Divider - Visual separator
#    └── Results Section (Container) - "Box 2"
#        └── Column - Elements in box 2

    # Add all components to page
    page.add(
        ft.Column(
            controls=[
                title,
                main_content,
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )
    )
    
    # Initialize baseline display
    update_baseline_display()

ft.app(target=main)