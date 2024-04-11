import flet as ft
from page_elements.core_element import top_icons, render_cards

def main(page: ft.Page):
    page.title = "永遠拒絶の単語帳"
    page.window_width = 600
    page.window_height = 750
    page.padding = 0
    page.spacing = 0
    page.window_resizable = False  # ウインドウサイズ変更可否
    page.window_center()  # ウィンドウをデスクトップの中心に移動
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER  # 多分水平方向の中央寄せ
    
    control_icons = top_icons(ft, page)
    page.add(control_icons)

    render_cards(ft, page)

ft.app(target=main)
