import datetime
from page_elements.input_element import input_element
from page_elements.create_dlg_element import create_dlg
from page_elements.render_questions import render_questions
from database.database_control import get_firstDate, get_allData, getData_byStr
import flet as ft

select_key = "ALL"
select_key_withParam = ""
select_name = "ALL"
selected_index=0

# ****************Top ICON********************
def top_icons(ft: ft, page):
    # themeを切り替え
    def theme_changed(e):
        page.theme_mode = (
            ft.ThemeMode.DARK
            if page.theme_mode == ft.ThemeMode.LIGHT
            else ft.ThemeMode.LIGHT
        )
        # print(theme_icon)
        theme_icon.icon = (
            "dark_mode"
            if  theme_icon.icon == "light_mode"
            else "light_mode"
        )
        page.update()
    page.theme_mode = ft.ThemeMode.LIGHT
    theme_icon = ft.IconButton(ft.icons.LIGHT_MODE, on_click=theme_changed)

    # 新規単語を記入
    def open_inputField(e):
        # 単語の記入欄
        input_column = input_element(ft, page, render_cards, select_key, selected_index)
        control_list = top_column_ref.current.controls
        if len(control_list) < 2:
            control_list.append(input_column),
        else:
            control_list.remove(control_list[1])
        page.update()

    fillIn_icon = ft.IconButton(
        ft.icons.TEXT_INCREASE,
        # tooltip="新規単語を記入"
        on_click=open_inputField
    )

    def tabs_changed(e):
        global selected_index
        selected_index = e.control.selected_index
        if selected_index == 1:
            def close_bs(e):
                bs.open = False
                bs.update()

            def bs_dismissed(e):
                global select_key_withParam
                if select_key_withParam == "" or select_key_withParam == "{[]}":
                    select_key_withParam = "{[]}"
                    render_cards(ft, page)
                else:
                    select_key_withParam = ""

            def select_cards_byStr(e):
                global select_key_withParam
                select_key_withParam = e.control.value
                render_cards(ft, page)

            def select_card_byEXP(e):
                global select_key_withParam
                match select_key_withParam:
                    case "@NORMAL":
                        select_key_withParam = "@HIGH"
                        e.control.icon = "SENTIMENT_VERY_SATISFIED_SHARP"
                        e.control.icon_color = "green"
                    case "@HIGH":
                        select_key_withParam = "@LOW"
                        e.control.icon = "SENTIMENT_VERY_DISSATISFIED_SHARP"
                        e.control.icon_color = "red"
                    case _:
                        select_key_withParam = "@NORMAL"
                        e.control.icon = "SENTIMENT_SATISFIED_SHARP"
                        e.control.icon_color = None
                render_cards(ft, page)

            bs = ft.BottomSheet(
                ft.Container(
                    ft.Row([
                        ft.IconButton(ft.icons.TAG_FACES_ROUNDED, icon_size=22, on_click=select_card_byEXP),
                        ft.TextField(label="Search Words", height=40, content_padding=10, text_align=ft.TextAlign.CENTER, autofocus=True, on_change=select_cards_byStr),
                        ft.IconButton(ft.icons.MORE_TIME, icon_size=22, on_click=close_bs, tooltip="開発中未実装"),
                        ],
                        tight=True,
                        spacing=3,
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    padding=10,
                ),
                open=True,
                on_dismiss=bs_dismissed,
            )
            page.overlay.append(bs)
            page.update()
        elif selected_index == 2:
            # select_key = select_key
            render_questions(ft, page, select_key)
        else:
            render_cards(ft, page)

    tabs_ref = ft.Ref[ft.Tabs]()

    filter_control = ft.Tabs(
        ref=tabs_ref,
        selected_index=0,
        tab_alignment=ft.MainAxisAlignment.CENTER,
        on_change=tabs_changed,
        height=35,
        tabs=[
            ft.Tab(
                icon=ft.icons.CALENDAR_VIEW_DAY_OUTLINED,
                text=f"{select_name}",
                ), 
            ft.Tab(
                icon=ft.icons.SEARCH,
                text="EXP"
                ), 
            ft.Tab(
                icon=ft.icons.QUESTION_ANSWER_OUTLINED,
                text="Q&A"
                ),
            ]
    )

    # 全データ取得
    def getAll_card(e):
        global select_key, select_name
        select_key = "ALL"
        select_name = "ALL"
        tabs_ref.current._Control__previous_children[0].text = select_name
        if selected_index == 2:
            render_questions(ft, page, select_key)
        else:
            render_cards(ft, page)

    getAll_button = ft.IconButton(
        icon = ft.icons.DATA_USAGE,
        tooltip="全データを取得",
        on_click=getAll_card
    )

    # 特定時間を設置
    def change_date(e):
        global select_key, select_name
        select_key = date_picker.value
        select_str = select_key.strftime("%Y-%m-%d %H:%M:%S").split()[0].split("-")
        select_name = f"{select_str[1]}/{select_str[2]}"
        tabs_ref.current._Control__previous_children[0].text = select_name
        if selected_index == 2:
            render_questions(ft, page, select_key)
        else:
            render_cards(ft, page)

    date_button = ft.IconButton(
        icon=ft.icons.CALENDAR_MONTH,
        tooltip="特定時間のデータを取得",
        on_click=lambda _: date_picker.pick_date(),
    )
    date_picker = ft.DatePicker(
        on_change=change_date,
        # on_dismiss=date_picker_dismissed,
        first_date=get_firstDate(),
        last_date=datetime.datetime.now(),
    )
    page.overlay.append(date_picker)

    top_column_ref = ft.Ref[ft.Column]()

    return ft.Column([
        ft.Row([

        ft.Row([
            date_button,
            getAll_button
        ], alignment=ft.MainAxisAlignment.CENTER),

        filter_control,

        ft.Row([
            fillIn_icon,
            theme_icon
        ], alignment=ft.MainAxisAlignment.CENTER),

        ], alignment=ft.MainAxisAlignment.SPACE_AROUND, height=40),

        # input_column
    ], ref=top_column_ref, spacing=0)


# ****************カード生成******************
def render_cards(ft: ft, page):
    def open_dlg(e):
        create_dlg(ft, page, e, render_cards)

    if selected_index == 0:
        word_list = get_allData(select_key)
    elif selected_index == 1:
        word_list = getData_byStr(select_key_withParam)
    else:
        word_list = []

    word_cards = ft.GridView(
        expand=1,
        runs_count=5,
        max_extent=200,
        child_aspect_ratio=1.5,
        spacing=5,
        run_spacing=5,
        padding=10
    )

    for i in range(len(word_list)):
        word_cards.controls.append(
            ft.Container(
                content=ft.Column([
                    ft.Text(word_list[i][1], size=20, weight=ft.FontWeight.W_800),
                    ft.Text(f"[{word_list[i][3]}] [{word_list[i][2]}]", color="pink", size=13),
                    ft.Text(word_list[i][4], color="purple", italic=True, text_align=ft.TextAlign.JUSTIFY, width=170)
                ],
                spacing=0,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                # bgcolor="green",
                border_radius=ft.border_radius.all(5),
                border=ft.border.all(1.0, ft.colors.PURPLE_100),
                ink=True,
                shadow=ft.BoxShadow(
                    # spread_radius=1,
                    blur_radius=10,
                    color=ft.colors.PURPLE_100,
                    offset=ft.Offset(0, 0),
                    blur_style=ft.ShadowBlurStyle.OUTER,
                ),
                data={"id": word_list[i][0]},
                on_click=open_dlg,
            )
        )

    try:
        # print(page.controls)
        page.remove(page.controls[1])
    except Exception:
        pass
    page.add(word_cards)