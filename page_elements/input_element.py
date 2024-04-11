from database.database_control import inset_data
from page_elements.render_questions import render_questions
import datetime
import flet as ft

date = datetime.datetime.now()

word_data = {
    "word": "",
    "wordClass": "",
    "IPA": "",
    "phrase": "",
    "others": "",
    "experience": "@NORMAL"
}

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

def input_element(ft: ft, page, render_cards, select_key, selected_index):
    input_word = ft.Ref[ft.TextField]()
    input_wordClass= ft.Ref[ft.TextField]()
    input_IPA = ft.Ref[ft.TextField]()
    input_phrase = ft.Ref[ft.TextField]()
    input_others = ft.Ref[ft.TextField]()

    def inset_word(e):
        inset_data(word_data["word"], word_data["wordClass"], word_data["IPA"], word_data["phrase"], word_data["others"], word_data["experience"], date, None)
        word_data["word"] = ""
        word_data["wordClass"] = ""
        word_data["IPA"] = ""
        word_data["phrase"] = ""
        word_data["others"] = ""

        input_word.current.value = ""
        input_wordClass.current.value = ""
        input_IPA.current.value = ""
        input_phrase.current.value = ""
        input_others.current.value = ""
        if selected_index == 2:
            render_questions(ft, page, select_key)
        else:
            render_cards(ft, page)

    return ft.Column([
        ft.Divider(height=1, color="purple"),
        ft.Row([
            ft.TextField(ref=input_word, label="単語", width=210, height=35, content_padding=10, autofocus=True, value=word_data["word"], on_change=set_word),
            ft.TextField(ref=input_wordClass, label="語類", width=160, height=35, content_padding=10, value=word_data["wordClass"], on_change=set_wordClass),
            ft.TextField(ref=input_IPA, label="国際音声記号", width=160, height=35, content_padding=10, value=word_data["IPA"], on_change=set_IPA),
        ], spacing=3, alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([
            ft.TextField(ref=input_phrase, label="フレーズ", width=303, height=35, content_padding=10, value=word_data["phrase"], on_change=set_phrase),
            ft.TextField(ref=input_others, label="トランスレーションなど", width=190, content_padding=10, height=35, value=word_data["others"], on_change=set_others),
            ft.IconButton(
                # icon=ft.icons.DONE_OUTLINE_OUTLINED,
                icon=ft.icons.SETTINGS_SUGGEST,
                icon_color=ft.colors.GREEN,
                tooltip="単語をデータベースに記入",
                on_click=inset_word,
                ),
        ], spacing=3, alignment=ft.MainAxisAlignment.CENTER),
        ft.Divider(height=1, color="purple"),
        ],
        # visible=False,
        spacing=5,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )