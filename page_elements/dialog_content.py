from database.database_control import getData_byId

def dialog_content(ft, id, ref_text):
    result = getData_byId(id)
    match result[6]:
        case "@LOW":
            exp_color = "red"
        case "@HIGH":
            exp_color = "green"
        case _:
            exp_color = None
    
    return ft.Column([
        ft.Text(f'{result[1]}', size=40, weight=ft.FontWeight.W_800, ref=ref_text, color=f"{exp_color}"),
        ft.Text(f"[{result[3]}] [{result[2]}]", color="pink", size=26),
        ft.Text(f"{result[4]}", color="purple", size=30, italic=True, weight=ft.FontWeight.W_400, text_align=ft.TextAlign.CENTER)
        ],
        spacing=5,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )