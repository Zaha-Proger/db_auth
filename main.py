
import customtkinter as CTK
from tkinter import ttk
from db import DB
from testBD import ParseLog

CTK.set_appearance_mode("System")  # Modes: system (default), light, dark
CTK.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

root = CTK.CTk()
#root.geometry("500x400")
root.title("authDB")
root.resizable(False, False)

bg_color = root._apply_appearance_mode(CTK.ThemeManager.theme["CTkFrame"]["fg_color"])
text_color = root._apply_appearance_mode(CTK.ThemeManager.theme["CTkLabel"]["text_color"])
selected_color = root._apply_appearance_mode(CTK.ThemeManager.theme["CTkButton"]["fg_color"])

# создание стиля для таблиц
tablestyle = ttk.Style()
tablestyle.theme_use('default')
tablestyle.configure("Treeview", background=bg_color, foreground=text_color, fieldbackground=bg_color, borderwidth=0)
tablestyle.configure("Treeview.Heading", background=bg_color, foreground=text_color, fieldbackground=bg_color, borderwidth=0)
tablestyle.map('Treeview', background=[('selected', bg_color)], foreground=[('selected', selected_color)])
tablestyle.map('Treeview.Heading', background=[('selected', bg_color)], foreground=[('selected', selected_color)])
tablestyle.configure('Treeview', rowheight=80)
root.bind("<<TreeviewSelect>>", lambda event: root.focus_set())

db = None
parser = None

def load_app():
    global db, parser
    db = DB("./test.sqlite")
    parser = ParseLog(db)

def back_root(frame):
    frame.grid_remove()

def exit_app():
    global db
    db.close_db()
    exit()

def sort_table(table,col):
    # получаем все значения столбцов в виде отдельного списка
    l = [(table.set(k, col), k) for k in table.get_children("")]
    # сортируем список
    l.sort()
    # переупорядочиваем значения в отсортированном порядке
    for index,  (_, k) in enumerate(l):
        table.move(k, "", index)

def search(db, table, flag):
    search_window = CTK.CTkToplevel()
    search_window.geometry("300x100+400+300")
    search_window.resizable(False, False)

    search_entry = CTK.CTkEntry(master=search_window,  width = 250)
    search_entry.pack(padx = 20, pady = 20)

    b_cancel = CTK.CTkButton(master=search_window, width=100, text="cancel", command= lambda : search_window.destroy())
    b_cancel.place(relx = 0.09, rely = 0.6)

    def search_in_bd(db, req, table, flag):
        # req = ()
        if flag == "secure":
            db.cursor.execute("SELECT * FROM authInfo WHERE desc LIKE ? OR date LIKE ? OR proc LIKE ?", ('%'+req+'%','%'+req+'%','%'+req+'%',))
        elif flag == "lastlog":
            db.cursor.execute("SELECT * FROM lastLogInfo WHERE user LIKE ? OR proc LIKE ? OR out LIKE ? OR day LIKE ? OR date LIKE ? OR time LIKE ? OR rangeTime LIKE ?", ('%'+req+'%','%'+req+'%','%'+req+'%','%'+req+'%','%'+req+'%','%'+req+'%','%'+req+'%',))
        results = db.cursor.fetchall()
        # Очистка результатов
        for item in table.get_children():
            table.delete(item)

        # Отображение результатов в таблице
        for row in results:
            table.insert('', 'end', values=row)
    
    b_search = CTK.CTkButton(master=search_window, width=100, text="search", command= lambda: search_in_bd(db, search_entry.get(), table, flag))
    b_search.place(relx = 0.59, rely = 0.6)

def open_table_secure_log():
    global db, parser
    parser.log_secure()
    col = ("date", "time", "proc", "desc")

    frame_table = CTK.CTkFrame(master=root)
    frame_table.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
    table = ttk.Treeview(master=frame_table, columns=col, show="headings", selectmode="browse")
    table.pack(fill="both", expand=True)

    table.heading("date", text="Date", anchor="n", command=lambda: sort_table(table, 0))
    table.heading("time", text="Time", anchor="n", command=lambda: sort_table(table, 1))
    table.heading("proc", text="Process", anchor="n")
    table.heading("desc", text="Description", anchor="n")

    table.column("#1", stretch=False, width=100, anchor="center")
    table.column("#2", stretch=False, width=100, anchor="center")
    table.column("#3", stretch=False, width=300, anchor="center")
    table.column("#4", stretch=True, width=800)

    db.cursor.execute("SELECT * FROM authInfo")
    records = db.cursor.fetchall()
    for r in records:
        table.insert("", "end", values=r)
    
    # frame_with_buttons = CTK.CTkFrame(master=root)
    # frame_with_buttons.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
    frame_buttons = CTK.CTkFrame(master = frame_table)
    frame_buttons.pack(fill="both", expand=True, side = "bottom")
    
    b_back = CTK.CTkButton(master=frame_buttons, text="back", command= lambda: back_root(frame_table))
    b_back.grid(row=0, column = 0, pady = 20)

    b_search = CTK.CTkButton(master=frame_buttons, text="search", command= lambda: search(db, table=table, flag="secure"))
    b_search.grid(row=0, column = 2, pady = 20)

def open_table_last_log():
    global db, parser
    parser.log_last()

    col = ("user","proc","out","day","date","time","rangeTime")

    frame_table = CTK.CTkFrame(master=root)
    frame_table.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

    table = ttk.Treeview(master=frame_table, columns=col, show="headings", selectmode="browse")
    table.pack(fill="both", expand=True)

    table.heading("user", text="User", anchor="n")
    table.heading("proc", text="Proc", anchor="n")
    table.heading("out", text="Out", anchor="n")
    table.heading("day", text="Day", anchor="n")
    table.heading("date", text="Date", anchor="n")
    table.heading("time", text="Time", anchor="n")
    table.heading("rangeTime", text="RangeTime", anchor="n")

    table.column("#1", stretch=False, width=100, anchor="center")
    table.column("#2", stretch=False, width=100, anchor="center")
    table.column("#3", stretch=False, width=100, anchor="center")
    table.column("#4", stretch=True, width=100, anchor="center")
    table.column("#5", stretch=True, width=100, anchor="center")
    table.column("#6", stretch=True, width=100, anchor="center")
    table.column("#7", stretch=True, width=100, anchor="center")

    db.cursor.execute("SELECT * FROM lastLogInfo")
    records = db.cursor.fetchall()
    for r in records:
        table.insert("", "end", values=r)
    
    frame_buttons = CTK.CTkFrame(master = frame_table)
    frame_buttons.pack(fill="both", expand=True, side = "bottom")
    
    b_back = CTK.CTkButton(master=frame_buttons, text="back", command= lambda: back_root(frame_table))
    b_back.grid(row=0, column = 0, pady = 20)

    b_search = CTK.CTkButton(master=frame_buttons, text="search", command= lambda: search(db, table=table, flag="lastlog"))
    b_search.grid(row=0, column = 2, pady = 20)
# root.geometry("400x200")
# root.grid_columnconfigure(0, weight=1)

load_app()

frame_with_buttons = CTK.CTkFrame(master=root)
frame_with_buttons.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

b_secure = CTK.CTkButton(master=frame_with_buttons, text="/var/log/secure", command=open_table_secure_log)
b_secure.grid(row=0, column = 0, padx = 20, pady = 15)

b_lastlog = CTK.CTkButton(master=frame_with_buttons, text="/var/log/wtmp", command=open_table_last_log)
b_lastlog.grid(row=1, column = 0, padx = 20)

b_exit = CTK.CTkButton(master=frame_with_buttons, text="exit", command=exit_app)
b_exit.grid(row=2, column = 0, padx = 20, pady = 30)

root.mainloop()