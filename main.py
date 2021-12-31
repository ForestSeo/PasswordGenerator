import string
import random
import pyperclip
import itertools
import PySimpleGUI as sg

# ランダムな文字列を作ってくれる

MARKS = ["!", "-", "_", ".", "?", "+"]


def make_pass(lt, letters_idx, marks_idx, use_marks_fl):
	letter_lst1 = list(string.ascii_lowercase)
	letter_lst2 = list(string.ascii_uppercase)
	letter_lst3 = list(string.digits)
	lst1 = [j for i, j in enumerate([letter_lst1, letter_lst2, letter_lst3]) if letters_idx[i]]
	lst1 = list(itertools.chain.from_iterable(lst1))
	lst2 = [i for i in MARKS if marks_idx[MARKS.index(i)]]
	pas_lst1 = [random.choice(lst1) for _ in range(lt-len(lst2))]
	lst = pas_lst1 + lst2
	random.shuffle(lst)
	if use_marks_fl:
		while set(MARKS) & {lst[0], lst[-1]}:
			random.shuffle(lst)
	pas = "".join(lst)
	return pas


checks_layout = [
	[sg.Checkbox(MARKS[i], default=(i<=2), key=f"-mark{i}-") for i in range(len(MARKS))]
]
checks_layout[0] += [sg.Checkbox("初めと終わりに記号を使わない", default=True, key="-use_marks_fl-")]
letters_layout = [
	[
		sg.Checkbox("小文字英字(a~z)", default=True, key=f"-lows-"),
		sg.Checkbox("大文字英字(A~Z)", default=True, key=f"-ups-"),
		sg.Checkbox("数字(0~9)", default=True, key=f"-nums-"),
	]
]

layout = [
	[sg.Text("パスワード作成", size=[54, 1])],
	[sg.Slider(range=(1, 32), default_value=15, resolution=1, orientation="h", key="-length-")],
	[sg.Frame("文字", letters_layout)],
	[sg.Frame("記号", checks_layout), sg.Button("作成する", key="-make-")],
	[sg.InputText(default_text="", key="-result-"), sg.Button("コピー", key="-copy-")],
]
window = sg.Window("メモ帳", layout, icon="favicon.ico")


event = "default"
while event is not None:
	event, values = window.read()
	if event == "-make-":
		letters_bool_lst = [values[f"-{i}-"] for i in ["lows", "ups", "nums"]]
		marks_bool_lst = [values[f"-mark{i}-"] for i in range(len(MARKS))]
		use_marks_fl = values["-use_marks_fl-"]
		lt = int(values["-length-"])
		result_pas = make_pass(lt, letters_bool_lst, marks_bool_lst, use_marks_fl)
		window["-result-"].update(result_pas)
	elif event == "-copy-":
		pyperclip.copy(values["-result-"])
		sg.popup("コピーしました")

window.close()
