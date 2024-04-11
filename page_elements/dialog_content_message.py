import flet as ft

def dialog_content_message():
    return ft.Column([
            # ft.Divider(height=1, color="purple"),
            # ft.Text("開発者メッセージ  By Takeuchi"),
            ft.Text("10倍速学習法"),
            # ft.Divider(height=1, color="purple"),
            # ft.Column([
            #     ft.Text("別にこれは紹介文でも、使用説明文でもありません、ただとある人へのメッセージです。"),
            # ], spacing=0, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            # ft.Text("君がいくら永遠拒絶しても、僕はそれを絶対否定します。", color="purple600")

            # ft.Column([
            #     ft.Text("1. 作業前、25~30回の深呼吸 or Box Breathing 10回\n    Box Breathing: 4秒吸って -> 4秒止める -> 4秒吐いて -> 4秒止める", color="purple600"),
            #     ft.Divider(height=1, color="pink500"),
            #     ft.Text("2. 作業前、30秒~60秒間何も考えずに一点を見つめる", color="purple600"),
            #     ft.Divider(height=1, color="pink500"),
            #     ft.Text("3. 作業中に10秒程度「何もしない時間」あえて作る (1時間ランダム30回)", color="purple600"),
            #     ft.Divider(height=1, color="pink500"),
            #     ft.Text("4. 休憩時間NSDR式リカバリー\n    NSDR: 深い睡眠ではない\"睡眠のような\"休憩をとる", color="purple600"),
            #     # ft.Divider(height=1, color="pink500"),
            # ], spacing=0, expand=2, alignment=ft.MainAxisAlignment.SPACE_AROUND),

            ft.ListView([
                ft.Text("1. 作業前、25~30回の深呼吸 or Box Breathing 10回\n    Box Breathing: 4秒吸って -> 4秒止める -> 4秒吐いて -> 4秒止める", color="purple600"),
                ft.Divider(height=1, color="pink500"),
                ft.Text("2. 作業前、30秒~60秒間何も考えずに一点を見つめる", color="purple600"),
                ft.Divider(height=1, color="pink500"),
                ft.Text("3. 作業中に10秒程度「何もしない時間」あえて作る (1時間ランダム30回)", color="purple600"),
                ft.Divider(height=1, color="pink500"),
                ft.Text("4. 休憩時間NSDR式リカバリー\n    NSDR: 深い睡眠ではない\"睡眠のような\"休憩をとる", color="purple600"),
                ft.Divider(height=1, color="pink500"),
            ], spacing=5, width=420),

            ft.ListView([
                ft.Text("tips1: 毎回ほんの少しだけ何か変えてみて", color="pink500"),
                ft.Text("tips2: 十歳の子供でも分かるような言葉で教えてみて", color="pink500"),
                ft.Text("tips3: 期間中スマホは触らない", color="pink500"),
            ], spacing=2, width=300)
        ],
        spacing=5,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )