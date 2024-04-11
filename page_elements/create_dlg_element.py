from database.database_control import getData_byId, delete_byId, updateEXP_byId
from page_elements.dialog_content_update import dialog_content_update
from page_elements.dialog_content import dialog_content
from page_elements.dialog_content_message import dialog_content_message
import flet as ft

def get_expStatus(id):
    result = getData_byId(id)
    match result[6]:
        case "@LOW":
            exp_status = {
            "exp_icon": ft.icons.SENTIMENT_VERY_DISSATISFIED_SHARP,
            "exp_text": "EXP: LOW",
            "exp_color": "red"
            }
        case "@HIGH":
            exp_status = {
                "exp_icon": ft.icons.SENTIMENT_VERY_SATISFIED_SHARP,
                "exp_text": "EXP: HIGH",
                "exp_color": "green"
            }
        case _:
            exp_status = {
                "exp_icon": ft.icons.SENTIMENT_SATISFIED_SHARP,
                "exp_text": "EXP: NORMAL",
                "exp_color": None
            }
    return exp_status

def create_dlg(ft: ft, page, e, render_cards):
    id = e.control.data["id"]
    exp_status = get_expStatus(id)

    message_state = False
    ref_text = ft.Ref[ft.Text]()

    # ダイアログを閉じる
    def close_dlg(e):
        dlg_modal.open = False
        dlg_modal.update()


    # 自分の言いたい言葉
    def show_message(e):
        nonlocal message_state
        message = dialog_content_message()
        if message_state:
            dlg_modal.content.content = dlg_content
            message_state = False
        else:
            dlg_modal.content.content = message
            message_state = True
        dlg_modal.update()


    # EXP状態変更
    def change_exp(e):
        result = getData_byId(id)
        if result[6] == "@NORMAL":
            updateEXP_byId("@HIGH", id)
        elif result[6] == "@HIGH":
            updateEXP_byId("@LOW", id)
        else:
            updateEXP_byId("@NORMAL", id)
        exp_status = get_expStatus(id)
        e.control.icon = exp_status["exp_icon"]
        e.control.tooltip = exp_status["exp_text"]
        e.control.icon_color = exp_status["exp_color"]
        e.control.update()
        try:
            ref_text.current.color = exp_status["exp_color"]
            ref_text.current.update()
        except Exception:
            pass


    # 表示データ変更
    def show_otherInfo(e):
        # 毎回新しいresultを貰う必要があります
        result = getData_byId(id)
        try:
            if ref_text.current.value == result[1]:
                # ref_text.current.value = f'{result[1]} => [{result[5]}]'
                ref_text.current.value = f'「{result[5]}」'
                ref_text.current.color = "yellow"
                ref_text.current.bgcolor = "blue"
            else:
                exp_status = get_expStatus(id)
                ref_text.current.value = f'{result[1]}'
                ref_text.current.color = exp_status["exp_color"]
                ref_text.current.bgcolor = None
            ref_text.current.update()
        except Exception:
            pass

    def delete_record(e):
        delete_byId(id)
        dlg_modal.open = False
        render_cards(ft, page)

    def update_card(e):
        # 毎回新しいresultを貰う必要があります
        result = getData_byId(id)
        word_data = {
            "id": result[0],
            "word": result[1],
            "wordClass": result[2],
            "IPA": result[3],
            "phrase": result[4],
            "others": result[5],
        }
        dlg_content_AtChanged = dialog_content_update(ft, page, word_data, render_cards, dlg_modal, dialog_content, ref_text)
        dlg_modal.content.content = dlg_content_AtChanged
        dlg_modal.update()

    dlg_content = dialog_content(ft, id, ref_text)

    dlg_modal = ft.AlertDialog(
        # modalをFalseにするとダイアログ以外の場所をクリックするとダイアログが消せるように
        modal=False,
        content=ft.Container(
            content=dlg_content,
            # content=update_dialog,
            width=480,
            height=270,
            ink=True,
            border_radius=ft.border_radius.vertical(top=26),
            shadow=ft.BoxShadow(
                blur_radius=10,
                color=ft.colors.PURPLE_100,
                offset=ft.Offset(0, 0),
                blur_style=ft.ShadowBlurStyle.OUTER,
            ),
        ),
        actions=[
            ft.IconButton(ft.icons.ALL_INCLUSIVE, icon_size=22, icon_color="purple300", tooltip="開発者メッセージ", on_click=show_message),
            ft.IconButton(ft.icons.EDIT_OUTLINED, icon_size=22, on_click=update_card),
            ft.IconButton(ft.icons.MORE_TIME, icon_size=22, tooltip="開発中未実装"),
            ft.IconButton(ft.icons.AUTO_STORIES_OUTLINED, icon_size=22, on_click=show_otherInfo),
            ft.IconButton(icon=f"{exp_status['exp_icon']}", icon_size=22, tooltip=f"{exp_status['exp_text']}", icon_color=f"{exp_status['exp_color']}", on_click=change_exp),
            ft.IconButton(ft.icons.DELETE_OUTLINE_SHARP, icon_size=22, on_click=delete_record),
            ft.TextButton("EXIT", on_click=close_dlg),
        ],
        actions_alignment=ft.MainAxisAlignment.SPACE_AROUND,
        title_padding=0,
        content_padding=0,
        actions_padding=0,
    )

    page.dialog = dlg_modal
    dlg_modal.open = True
    page.update()