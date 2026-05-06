import tkinter as tk
import math
import json
import os
import time
import re

# ---------- HISTORY ----------
HISTORY_FILE = "history.json"
HISTORY_DURATION = 72 * 60 * 60


def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r") as f:
        data = json.load(f)
    now = time.time()
    return [h for h in data if now - h["time"] <= HISTORY_DURATION]


def save_history(exp, res):
    history = load_history()
    history.append({"exp": exp, "res": res, "time": time.time()})
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f)


# ---------- MAIN ----------
root = tk.Tk()
root.title("SINCA Scientific Calculator")
root.geometry("400x600")
root.configure(bg="black")

expression = ""


def update(val):
    entry.delete(0, tk.END)
    entry.insert(0, val)


def press(val):
    global expression
    expression += str(val)
    update(expression)


def clear():
    global expression
    expression = ""
    update("")


def backspace():
    global expression
    expression = expression[:-1]
    update(expression)


# ---------- ✅ FIXED CALCULATE ----------
def calculate():
    global expression
    try:
        exp = expression

        # Step 1: Handle + and - percentage (like 50+10%)
        pattern = r'(\d+\.?\d*)([\+\-])(\d+\.?\d*)%'

        def replace_pm(match):
            a = float(match.group(1))
            op = match.group(2)
            b = float(match.group(3))

            percent = (a * b) / 100

            if op == '+':
                return str(a + percent)
            else:
                return str(a - percent)

        exp = re.sub(pattern, replace_pm, exp)

        # Step 2: Replace remaining % (like 50% → 0.5)
        exp = re.sub(r'(\d+\.?\d*)%', lambda m: str(float(m.group(1)) / 100), exp)

        # Constants
        exp = exp.replace("π", str(math.pi)).replace("e", str(math.e))

        result = str(eval(exp))

        save_history(expression, result)
        expression = result
        entry.delete(0, tk.END)
        entry.insert(0, result)

    except:
        entry.delete(0, tk.END)
        entry.insert(0, "Error")
        expression = ""

# ---------- FUNCTIONS ----------
def func(f):
    global expression
    try:
        val = float(expression)

        if f == "sin":
            res = math.sin(math.radians(val))
        elif f == "cos":
            res = math.cos(math.radians(val))
        elif f == "tan":
            res = math.tan(math.radians(val))
        elif f == "log":
            res = math.log10(val)
        elif f == "ln":
            res = math.log(val)
        elif f == "sqrt":
            res = math.sqrt(val)
        elif f == "square":
            res = val ** 2
        else:
            return

        save_history(expression, res)
        expression = str(res)
        update(res)

    except:
        update("Error")


# ---------- EXTRA ----------
def to_binary():
    global expression
    try:
        res = bin(int(float(expression)))[2:]
        expression = res
        update(res)
    except:
        update("Error")


def to_decimal():
    global expression
    try:
        res = str(int(expression, 2))
        expression = res
        update(res)
    except:
        update("Error")


def to_hex():
    global expression
    try:
        res = hex(int(float(expression)))[2:]
        expression = res
        update(res)
    except:
        update("Error")


def npr():
    global expression
    try:
        exp = entry.get().strip()

        # साफ input लेना
        exp = exp.replace(" ", "")

        if ',' not in exp:
            entry.delete(0, tk.END)
            entry.insert(0, "Enter n,r")
            return

        parts = exp.split(',')

        if len(parts) != 2:
            raise ValueError

        n = int(parts[0])
        r = int(parts[1])

        if n < 0 or r < 0 or r > n:
            raise ValueError

        result = math.perm(n, r)

        save_history(exp, result)

        entry.delete(0, tk.END)
        entry.insert(0, result)

        expression = str(result)

    except:
        entry.delete(0, tk.END)
        entry.insert(0, "Invalid (5,2)")
        expression = ""
   

      
def ncr():
    global expression
    try:
        exp = expression.replace(" ", "")

        if ',' not in exp:
            raise ValueError

        n, r = map(int, exp.split(','))

        if n < 0 or r < 0 or r > n:
            raise ValueError

        result = math.comb(n, r)

        save_history(expression, result)
        expression = str(result)

        entry.delete(0, tk.END)
        entry.insert(0, result)

    except:
        entry.delete(0, tk.END)
        entry.insert(0, "Use n,r (e.g. 5,2)")
        expression = ""


def fibs():
    global expression
    try:
        n = int(expression)
        a, b = 0, 1
        seq = []
        for _ in range(n):
            seq.append(str(a))
            a, b = b, a + b
        res = ", ".join(seq)
        expression = res
        update(res)
    except:
        update("Error")


# ---------- UI ----------
entry = tk.Entry(root, font=("Arial", 20),
                 bg="#dcdcdc", justify="right")
entry.pack(fill="both", ipadx=8, ipady=20, padx=10, pady=10)

frame = tk.Frame(root, bg="black")
frame.pack(expand=True, fill="both")

for i in range(10):
    frame.rowconfigure(i, weight=1)
for j in range(4):
    frame.columnconfigure(j, weight=1)


def btn(t, r, c, cmd, bg, fg):
    tk.Button(frame, text=t, command=cmd,
              font=("Arial", 12, "bold"),
              bg=bg, fg=fg).grid(row=r, column=c,
                                 sticky="nsew", padx=2, pady=2)


digit = "#2b2b2b"
op = "#2b2b2b"
func_c = "#3a3a3a"

buttons = [
    ('7', lambda: press('7'), digit, 'white'),
    ('8', lambda: press('8'), digit, 'white'),
    ('9', lambda: press('9'), digit, 'white'),
    ('/', lambda: press('/'), digit, '#00bfff'),

    ('4', lambda: press('4'), digit, 'white'),
    ('5', lambda: press('5'), digit, 'white'),
    ('6', lambda: press('6'), digit, 'white'),
    ('*', lambda: press('*'), digit, '#00bfff'),

    ('1', lambda: press('1'), digit, 'white'),
    ('2', lambda: press('2'), digit, 'white'),
    ('3', lambda: press('3'), digit, 'white'),
    ('-', lambda: press('-'), digit, '#00bfff'),

    ('0', lambda: press('0'), digit, 'white'),
    ('.', lambda: press('.'), digit, '#00bfff'),
    ('+', lambda: press('+'), digit, '#00bfff'),
    ('=', calculate, digit, '#00bfff'),

    ('sin', lambda: func("sin"), '#1f3b4d', 'lightgrey'),
    ('cos', lambda: func("cos"), '#1f3b4d', 'lightgrey'),
    ('tan', lambda: func("tan"), '#1f3b4d', 'lightgrey'),
    ('√', lambda: func("sqrt"), func_c, '#00bfff'),

    ('log', lambda: func("log"), '#1f3b4d', 'lightgrey'),
    ('ln', lambda: func("ln"), '#1f3b4d', 'lightgrey'),
    ('x²', lambda: func("square"), '#1f3b4d', 'lightgrey'),
    ('%', lambda: press('%'), func_c, '#00bfff'),

    ('Bin', to_binary, '#1f3b4d', 'lightgrey'),
    ('Dec', to_decimal, '#1f3b4d', 'lightgrey'),
    ('Hex', to_hex, '#1f3b4d', 'lightgrey'),
    ('e', lambda: press('e'), func_c, '#00bfff'),

    ('nPr', npr, '#1f3b4d', 'lightgrey'),
    ('nCr', ncr, '#1f3b4d', 'lightgrey'),
    ('Fibs', fibs, '#1f3b4d', 'lightgrey'),
    ('π', lambda: press('π'), func_c, '#00bfff'),

    (',', lambda: press(','), func_c, '#00bfff'),
    ('00', lambda: press('00'), digit, 'white'),
    ('C', clear, func_c, 'lightcoral'),
    ('CE', backspace, func_c, 'lightcoral'),
]

r = c = 0
for t, cmd, bg, fg in buttons:
    btn(t, r, c, cmd, bg, fg)
    c += 1
    if c > 3:
        c = 0
        r += 1


# ---------- HISTORY ----------
history_visible = False
history_frame = tk.Frame(root, bg="black")

history_text = tk.Text(history_frame, height=6,
                       bg="#111", fg="white")
history_text.pack(fill="both")


def toggle_history():
    global history_visible
    if history_visible:
        history_frame.pack_forget()
        history_visible = False
    else:
        history_text.delete("1.0", tk.END)
        for h in load_history():
            history_text.insert(tk.END, f"{h['exp']} = {h['res']}\n")
        history_frame.pack(fill="both")
        history_visible = True


tk.Button(root, text="History", command=toggle_history,
          bg="black", fg="cyan").pack(fill="x")


# ---------- KEYBOARD ----------
def key(event):
    k = event.char
    if k in "0123456789+-*/.%":
        press(k)
    elif event.keysym == "Return":
        calculate()
    elif event.keysym == "BackSpace":
        backspace()


root.bind("<Key>", key)


root.mainloop()