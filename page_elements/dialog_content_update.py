from database.database_control import update_byId
import flet as ft

def dialog_content_update(ft: ft, page, word_data, render_cards, dlg_modal, dialog_content, ref_text):
    input_word = ft.Ref[ft.TextField]()
    input_wordClass= ft.Ref[ft.TextField]()
    input_IPA = ft.Ref[ft.TextField]()
    input_phrase = ft.Ref[ft.TextField]()
    input_others = ft.Ref[ft.TextField]()

    def set_word(e):
        word_data["word"] = e.control.value

    def set_wordClass(e):
        word_data["wordClass"] = e.control.value

    def set_IPA(e):
        word_data["IPA"] = e.control.value

    def set_phrase(e):
        word_data["phrase"] = e.control.value

    def set_others(e):
        word_data["others"] = e.control.value
    
    def update_word(e):
        update_byId(word_data["word"], word_data["wordClass"], word_data["IPA"], word_data["phrase"], word_data["others"], word_data["id"])
        dlg_modal.content.content = dialog_content(ft, word_data["id"], ref_text)
        render_cards(ft, page)

    return ft.Column([
        ft.Divider(height=1, color="purple"),
        ft.Row([
            ft.TextField(ref=input_word, label="word", width=210, height=35, content_padding=10, autofocus=True, value=word_data["word"], on_change=set_word),
            ft.TextField(ref=input_wordClass, label="class", width=110, height=35, content_padding=10, value=word_data["wordClass"], on_change=set_wordClass),
            ft.TextField(ref=input_IPA, label="IPA", width=110, height=35, content_padding=10, value=word_data["IPA"], on_change=set_IPA),
        ], spacing=3, alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([
            ft.TextField(ref=input_phrase, label="phrase", width=270, height=35, content_padding=10, value=word_data["phrase"], on_change=set_phrase),
            ft.TextField(ref=input_others, label="others", width=120, height=35, content_padding=10, value=word_data["others"], on_change=set_others),
            ft.IconButton(
                # icon=ft.icons.DONE_OUTLINE_OUTLINED,
                icon=ft.icons.SETTINGS_SUGGEST,
                icon_color=ft.colors.GREEN,
                tooltip="データベースのデータを更新",
                on_click=update_word,
                ),
        ], spacing=3, alignment=ft.MainAxisAlignment.CENTER),
        ft.Divider(height=1, color="purple"),
        ],
        # visible=False,
        spacing=5,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )