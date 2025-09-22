import json
import tkinter as tk
from tkinter import messagebox
from collections import Counter, deque


def load_petri(filename):
    with open(filename, encoding="utf-8") as f:
        data = json.load(f)

    places = []
    init_marking = {}
    for p in data["places"]:
        parts = p.split(",")
        name = parts[0]
        tokens = int(parts[3])
        places.append(name)
        init_marking[name] = tokens

    transitions = []
    for t in data["trans"]:
        name = t.split(",")[0]
        transitions.append(name)

    pre = {t: {} for t in transitions}
    post = {t: {} for t in transitions}
    for arc in data["arcs"]:
        s, d = arc.split(",")
        if s in places and d in transitions:
            pre[d][s] = pre[d].get(s, 0) + 1
        elif s in transitions and d in places:
            post[s][d] = post[s].get(d, 0) + 1

    return places, transitions, pre, post, init_marking


def enabled(t, marking, pre):
    for p, w in pre[t].items():
        if marking.get(p, 0) < w:
            return False
    return True


def fire(t, marking, pre, post):
    new = Counter(marking)
    for p, w in pre[t].items():
        new[p] -= w
    for p, w in post[t].items():
        new[p] += w
    return dict(new)


def build_diagram(places, transitions, pre, post, init):
    start = tuple(init[p] for p in places)
    q = deque([start])
    seen = {start: None}
    edges = []

    while q:
        mtuple = q.popleft()
        marking = {p: mtuple[i] for i, p in enumerate(places)}
        for t in transitions:
            if enabled(t, marking, pre):
                new_mark = fire(t, marking, pre, post)
                m2 = tuple(new_mark[p] for p in places)
                edges.append((mtuple, t, m2))
                if m2 not in seen:
                    seen[m2] = (mtuple, t)
                    q.append(m2)

    return list(seen.keys()), edges


def export_to_dot(places, markings, edges, filename="diagram"):
    def fmt(mtuple):
        return "[" + ",".join(f"{mtuple[i]}" for i, p in enumerate(places)) + "]"

    with open(filename, "w", encoding="utf-8") as f:
        f.write("digraph Diagram {\n")
        f.write("rankdir=TB;\n")
        for m in markings:
            f.write(f"  \"{m}\" [label=\"{fmt(m)}\"];\n")
        for m1, t, m2 in edges:
            f.write(f"  \"{m1}\" -> \"{m2}\" [label=\"{t}\"];\n")
        f.write("}\n")


class PetriUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Petri Net Analyzer")
        self.geometry("1000x700")

        self.places = []
        self.markings = []
        self.edges = []

        intro_text = (
            "Классы сетей Петри:\n"
            "Автоматные сети — сети, в которых переход имеет не более одного входа и не более одного выхода\n"
            "Маркированные сети — сети, в которых каждая позиция имеет не более одного входа и не более одного выхода\n"
            "Сети свободного выбора — сети, в которых каждая дуга, выходящая из позиции, является либо единственным выходом из нее, либо единственным входом в переход\n"
            "Простые сети — сети, в которых каждый переход может иметь не более одной общей позиции с другими переходами\n"
            "\nПервая сеть:\n"
            "Срабатывание нескольких переходов возможно (Например a, b)\n"
            "Классификация по динамическим ограничениям:\n"
            "1) безопасная, (ограниченная, 1-ограниченная)\n"
            "2) 1-консарвативная (кол-во маркеров постоянно)\n"
            "3) живая (каждый переход является потенциально срабатывающим)\n"
            "4) неустойчивая (срабатывание одного перехода снимает возбуждение другого)\n"
            "Классификация по статическим ограничениям:\n"
            "Сеть свободного выбора (каждая дуга, выходящая из позиции, является либо единственным выходом из нее, либо единственным входом в переход)\n"
            "\nВторая сеть:\n"
            "Срабатывание нескольких переходов возможно (Например t2, t3)\n"
            "Классификация по динамическим ограничениям:\n"
            "1) ограниченная, 2-ограниченная\n"
            "2) консарвативная (кол-во маркеров никогда не превышает 4)\n"
            "3) живая (каждый переход является потенциально срабатывающим)\n"
            "4) устойчивая (срабатывание одного перехода не снимает возбуждение другого)\n"
            "Классификация по статическим ограничениям:\n"
            "Маркированная сеть (каждая позиция имеет не более одного входа и не более одного выхода)\n"
        )
        tk.Label(self, text=intro_text, justify="left", anchor="w").pack(fill="x", padx=10, pady=10)

        frame = tk.Frame(self)
        frame.pack(pady=10, fill="x")

        tk.Label(frame, text="Файл с сетью:").grid(row=0, column=0, sticky="e")
        self.entry_input = tk.Entry(frame, width=40)
        self.entry_input.insert(0, "pnet.txt")
        self.entry_input.grid(row=0, column=1, padx=5)

        tk.Label(frame, text="Файл для диаграммы:").grid(row=1, column=0, sticky="e")
        self.entry_output = tk.Entry(frame, width=40)
        self.entry_output.insert(0, "diagram")
        self.entry_output.grid(row=1, column=1, padx=5)

        tk.Button(frame, text="Сохранить диаграмму", command=self.build).grid(row=2, column=1, pady=5)

        tk.Label(frame, text="Маркировка (например: 0,1,0,1,0):").grid(row=3, column=0, sticky="e")
        self.entry_marking = tk.Entry(frame, width=40)
        self.entry_marking.grid(row=3, column=1, padx=5)

        tk.Button(frame, text="Проверить достижимость", command=self.check).grid(row=4, column=1, pady=5)

    def build(self):
        filename = self.entry_input.get().strip()
        out_file = self.entry_output.get().strip()
        if not filename:
            messagebox.showerror("Ошибка", "Укажите имя входного файла")
            return
        try:
            self.places, transitions, pre, post, init = load_petri(filename)
            self.markings, self.edges = build_diagram(self.places, transitions, pre, post, init)
            export_to_dot(self.places, self.markings, self.edges, out_file)
            messagebox.showinfo("Готово", f"Диаграмма сохранена в {out_file}")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def check(self):
        if not self.markings:
            messagebox.showerror("Ошибка", "Сначала постройте диаграмму")
            return
        text = self.entry_marking.get().strip()
        try:
            mtuple = tuple(int(x) for x in text.split(","))
        except ValueError:
            messagebox.showerror("Ошибка", "Введите маркировку через запятую, например 0,1,0")
            return
        if mtuple in self.markings:
            messagebox.showinfo("Результат", f"Маркировка {mtuple} достижима")
        else:
            messagebox.showinfo("Результат", f"Маркировка {mtuple} недостижима")


if __name__ == "__main__":
    app = PetriUI()
    app.mainloop()

#https://petri.hp102.ru/pnet.html
#https://dreampuf.github.io/GraphvizOnline/?engine=dot#digraph%20G%20%7B%0A%0A%20%20subgraph%20cluster_0%20%7B%0A%20%20%20%20style%3Dfilled%3B%0A%20%20%20%20color%3Dlightgrey%3B%0A%20%20%20%20node%20%5Bstyle%3Dfilled%2Ccolor%3Dwhite%5D%3B%0A%20%20%20%20a0%20-%3E%20a1%20-%3E%20a2%20-%3E%20a3%3B%0A%20%20%20%20label%20%3D%20%22process%20%231%22%3B%0A%20%20%7D%0A%0A%20%20subgraph%20cluster_1%20%7B%0A%20%20%20%20node%20%5Bstyle%3Dfilled%5D%3B%0A%20%20%20%20b0%20-%3E%20b1%20-%3E%20b2%20-%3E%20b3%3B%0A%20%20%20%20label%20%3D%20%22process%20%232%22%3B%0A%20%20%20%20color%3Dblue%0A%20%20%7D%0A%20%20start%20-%3E%20a0%3B%0A%20%20start%20-%3E%20b0%3B%0A%20%20a1%20-%3E%20b3%3B%0A%20%20b2%20-%3E%20a3%3B%0A%20%20a3%20-%3E%20a0%3B%0A%20%20a3%20-%3E%20end%3B%0A%20%20b3%20-%3E%20end%3B%0A%0A%20%20start%20%5Bshape%3DMdiamond%5D%3B%0A%20%20end%20%5Bshape%3DMsquare%5D%3B%0A%7D
