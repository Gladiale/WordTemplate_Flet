from database.database_control import getData_byRandom
import flet as ft

def render_questions(ft: ft, page: ft.Page, select_key):
    random_data = getData_byRandom(select_key)
    # print(random_data)
    cache_data = {}
    cache_number = []

    def set_cacheData(e):
        value = e.control.value
        key = e.control.data
        cache_data[key] = value
        # print(cache_data)

    def check_answer(e):
        list_index = cache_number.index(e.control.data[0])
        icon = lv.controls[list_index].controls[0]
        text = lv.controls[list_index].controls[1].controls[1]
        try:
            answer_user = cache_data[e.control.data[0]]
            answer_prototype = e.control.data[1]
            if answer_user == answer_prototype:
                icon.name = "VERIFIED"
                icon.color = "green"
            else:
                icon.name = "CLEAR"
                icon.color = "red"
        except Exception:
            pass
        text.visible = not text.visible
        lv.update()

    def check_allAnswer(e):
        for number in cache_number:
            list_index = cache_number.index(number)
            icon = lv.controls[list_index].controls[0]
            text = lv.controls[list_index].controls[1].controls[1]
            que = lv.controls[list_index].controls[2].data[1]
            try:
                answer_user = cache_data[number]
                if answer_user == que:
                    icon.name = "VERIFIED"
                    icon.color = "green"
                else:
                    icon.name = "CLEAR"
                    icon.color = "red"
            except Exception:
                pass
            text.visible = True
        lv.update()

    lv = ft.ListView(spacing=5, padding=5, auto_scroll=True)

    for index, data in enumerate(random_data):
        data_list = data[1].split(data[0])
        if len(data_list) >= 2:
            cache_number.append(index)
            row_text = ft.Row([
                ft.Text(data_list[0]),
                ft.TextField(border="underline", width=130, content_padding=5, text_align=ft.TextAlign.CENTER, data=index, on_change=set_cacheData),
                ft.Text(data_list[1]),
            ], spacing=0)

            col_text = ft.Column([
                row_text,
                ft.Text(f"「{data[1]}」", color="pink500", italic=True, visible=False)
            # ここのexpand=3は3/5, question_row 1+3+1=5
            ], spacing=0, expand=3)

            question_row = ft.Row([
                # ft.Icon(ft.icons.QUESTION_MARK, expand=1),
                ft.Icon(ft.icons.QUORA, expand=1),
                col_text,
                ft.IconButton(ft.icons.ANDROID_OUTLINED, expand=1, data=[index, data[0]], on_click=check_answer)
            ])

            lv.controls.append(question_row)

    question_list = ft.Column([
        ft.Row([
            ft.Text(f"絶対否定の問題集 At {select_key}", color="purple400", weight=ft.FontWeight.W_500),
            ft.IconButton(ft.icons.NEXT_PLAN, icon_color="purple400", on_click=check_allAnswer),
        ], alignment=ft.MainAxisAlignment.SPACE_AROUND),
        ft.Divider(height=1, color="pink"),
        lv
    ], spacing=0)

    try:
        # print(page.controls)
        page.remove(page.controls[1])
    except Exception:
        pass
    page.add(question_list)