from tkinter import filedialog

filename = filedialog.askopenfilename(
    title = "座標読み取り",
    filetypes = [("テキストファイルオンリー", ".txt") ], # ファイルフィルタ
    initialdir = "./" # 自分自身のディレクトリ
    )
print(filename)

f = open(filename)

# テキスト読み込みなどの処理文

print(f)

f.close()


