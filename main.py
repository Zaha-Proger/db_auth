
import customtkinter as CTK
from tkinter import ttk
from db import DB
from parserlog import ParseLog

db = None
parser = None
root = None

def load_app():
    global db, parser
    db = DB("./auth_db.sqlite")
    parser = ParseLog(db)
    update_db()
    create_root_win()

def update_db():
    parser.log_secure()
    parser.log_BWtmp("wtmp")
    parser.log_BWtmp("btmp")
    
def exit_app():
    global db
    db.close_db()
    exit()

def sort_table(table,col, reverse):
    l = [(table.set(k, col), k) for k in table.get_children("")]
    l.sort(reverse=reverse)
    for index,  (_, k) in enumerate(l):
        table.move(k, "", index)
    table.heading(col, command=lambda: sort_table(table, col, not reverse))

def cancel_search(table,records, window):
    for item in table.get_children():
        table.delete(item)

    for r in records:
        table.insert('', 'end', values=r)
    window.destroy()

def search(db, table, flag, records):
    search_window = CTK.CTkToplevel()
    search_window.geometry("300x100+400+300")
    search_window.title("Поиск")
    search_window.resizable(False, False)

    search_entry = CTK.CTkEntry(master=search_window,  width = 250)
    search_entry.pack(padx = 20, pady = 20)

    b_cancel = CTK.CTkButton(master=search_window, width=100, text="отмена", command= lambda : cancel_search(table, records, search_window))
    b_cancel.place(relx = 0.09, rely = 0.6)

    def search_in_bd(db, req, table, flag):
        if flag == "secure":
            if ":" in req:
                print(req[:10], req[11:])
                db.cursor.execute(f"SELECT * FROM authInfo_with_date WHERE date >= '{req[:10]}' AND date <= '{req[11:]}'")
            else: db.cursor.execute("SELECT * FROM authInfo_with_date WHERE desc LIKE ? OR date LIKE ? OR proc LIKE ?", ('%'+req+'%','%'+req+'%','%'+req+'%',))
        elif flag == "wtmp":
            if ":" in req:
                print(req[:10], req[11:])
                db.cursor.execute(f"SELECT * FROM wtmp_with_date WHERE date >= '{req[:10]}' AND date <= '{req[11:]}'")
            else:
                db.cursor.execute("SELECT * FROM wtmp_with_date WHERE user LIKE ? OR tty LIKE ? OR host LIKE ? OR date LIKE ? OR time LIKE ? OR session LIKE ?", ('%'+req+'%','%'+req+'%','%'+req+'%','%'+req+'%','%'+req+'%','%'+req+'%',))
        elif flag == "btmp":
            if ":" in req:
                print(req[:10], req[11:])
                db.cursor.execute(f"SELECT * FROM btmp_with_date WHERE date >= '{req[:10]}' AND date <= '{req[11:]}'")
            else:
                db.cursor.execute("SELECT * FROM btmp_with_date WHERE user LIKE ? OR tty LIKE ? OR host LIKE ? OR date LIKE ? OR time LIKE ? OR session LIKE ?", ('%'+req+'%','%'+req+'%','%'+req+'%','%'+req+'%','%'+req+'%','%'+req+'%',))
        results = db.cursor.fetchall()

        for item in table.get_children():
            table.delete(item)

        for row in results:
            table.insert('', 'end', values=row)
    
    b_search = CTK.CTkButton(master=search_window, width=100, text="поиск", command= lambda: search_in_bd(db, search_entry.get(), table, flag))
    b_search.place(relx = 0.59, rely = 0.6)

def open_table_secure_log():
    global db, parser, root

    x = 480
    y = 120

    root.wm_geometry("+%d+%d" % (x, y))

    col = ("date", "time", "proc", "desc")

    frame_table = CTK.CTkFrame(master=root)
    frame_table.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

    frame_buttons = CTK.CTkFrame(master = frame_table)
    frame_buttons.pack(fill="both", expand=True)
    
    b_back = CTK.CTkButton(master=frame_buttons, text="назад", command= lambda: frame_table.grid_remove())
    b_back.grid(row=0, column = 0,padx = 20, pady = 20)

    b_search = CTK.CTkButton(master=frame_buttons, text="поиск", command= lambda: search(db, table=table, flag="secure", records= records))
    b_search.grid(row=0, column = 2, pady = 20)

    table = ttk.Treeview(master=frame_table, columns=col, show="headings", selectmode="browse")
    table.pack(fill="both", expand=True, anchor="s")

    table.heading("date", text="Дата", anchor="n", command=lambda: sort_table(table, 0, False))
    table.heading("time", text="Время", anchor="n", command=lambda: sort_table(table, 1, False))
    table.heading("proc", text="Процесс", anchor="n")
    table.heading("desc", text="Описание", anchor="n")

    table.column("#1", stretch=False, width=100, anchor="center")
    table.column("#2", stretch=False, width=100, anchor="center")
    table.column("#3", stretch=False, width=300, anchor="center")
    table.column("#4", stretch=False, width=800)

    db.cursor.execute("SELECT * FROM authInfo_with_date")
    records = db.cursor.fetchall()
    for r in records:
        table.insert("", "end", values=r)

    table.bind('<Motion>', 'break') #запрет изменения размера столбцов

def open_table_bWtmp_log(flag):
    global db, parser, root
    
    x = 480
    y = 120

    root.wm_geometry("+%d+%d" % (x, y))

    col = ("user","tty","host","date","time","session")

    frame_table = CTK.CTkFrame(master=root)
    frame_table.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

    frame_buttons = CTK.CTkFrame(master = frame_table)
    frame_buttons.pack(fill="both", expand=True)
    
    b_back = CTK.CTkButton(master=frame_buttons, text="назад", command= lambda: frame_table.grid_remove())
    b_back.grid(row=0, column = 0, padx = 20, pady = 20)

    b_search = CTK.CTkButton(master=frame_buttons, text="поиск", command= lambda: search(db, table=table, flag=flag, records=records))
    b_search.grid(row=0, column = 2, pady = 20)

    table = ttk.Treeview(master=frame_table, columns=col, show="headings", selectmode="browse")
    table.pack(fill="both", expand=True, anchor="s")

    table.heading("user", text="Пользователь", anchor="n")
    table.heading("tty", text="Tty-сессия", anchor="n")
    table.heading("host", text="Хост", anchor="n")
    table.heading("date", text="Дата", anchor="n", command=lambda: sort_table(table, 3, False))
    table.heading("time", text="Время", anchor="n", command=lambda: sort_table(table, 4, False))
    table.heading("session", text="Прод-ть сессии", anchor="n", command=lambda: sort_table(table, 5, False))

    table.column("#1", stretch=False, width=100, anchor="center")
    table.column("#2", stretch=False, width=100, anchor="center")
    table.column("#3", stretch=False, width=100, anchor="center")
    table.column("#4", stretch=False, width=100, anchor="center")
    table.column("#5", stretch=False, width=100, anchor="center")
    table.column("#6", stretch=False, width=100, anchor="center")

    if flag == "wtmp":
        db.cursor.execute("SELECT * FROM wtmp_with_date")
        records = db.cursor.fetchall()
        for r in records:
            table.insert("", "end", values=r)
    elif flag == "btmp":
        db.cursor.execute("SELECT * FROM btmp_with_date")
        records = db.cursor.fetchall()
        for r in records:
            table.insert("", "end", values=r)

    table.bind('<Motion>', 'break') #запрет изменения размера столбцов

def create_root_win():
    global root
    root = CTK.CTk()
    root.title("authDB")
    root.resizable(False, False)

    CTK.set_appearance_mode("System")  # Modes: system (default), light, dark
    CTK.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

    bg_color = root._apply_appearance_mode(CTK.ThemeManager.theme["CTkFrame"]["fg_color"])
    text_color = root._apply_appearance_mode(CTK.ThemeManager.theme["CTkLabel"]["text_color"])
    selected_color = root._apply_appearance_mode(CTK.ThemeManager.theme["CTkButton"]["fg_color"])

    tablestyle = ttk.Style()
    tablestyle.theme_use('default')
    tablestyle.configure("Treeview", background=bg_color, foreground=text_color, fieldbackground=bg_color, borderwidth=0)
    tablestyle.configure("Treeview.Heading", background=bg_color, foreground=text_color, fieldbackground=bg_color, borderwidth=0)
    tablestyle.map('Treeview', background=[('selected', bg_color)], foreground=[('selected', selected_color)])
    tablestyle.map('Treeview.Heading', background=[('selected', bg_color)], foreground=[('selected', selected_color)])
    tablestyle.configure('Treeview', rowheight=80)
    root.bind("<<TreeviewSelect>>", lambda event: root.focus_set())
    frame_with_buttons = CTK.CTkFrame(master=root)
    frame_with_buttons.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

    b_secure = CTK.CTkButton(master=frame_with_buttons, text="/var/log/secure", command= open_table_secure_log)
    b_secure.grid(row=0, column = 0, padx = 20, pady = 15)

    b_lastlog = CTK.CTkButton(master=frame_with_buttons, text="/var/log/wtmp", command= lambda: open_table_bWtmp_log("wtmp"))
    b_lastlog.grid(row=1, column = 0, padx = 20)
    
    b_btmplog = CTK.CTkButton(master=frame_with_buttons, text="/var/log/btmp", command= lambda: open_table_bWtmp_log("btmp"))
    b_btmplog.grid(row=3, column = 0, padx = 20, pady = 15)

    b_updateDB = CTK.CTkButton(master=frame_with_buttons, text="обновить БД", command= update_db)
    b_updateDB.grid(row=4, column = 0, padx = 20, pady = 15)

    b_exit = CTK.CTkButton(master=frame_with_buttons, text="выход", command=exit_app)
    b_exit.grid(row=5, column = 0, padx = 20, pady = 30)

    root.mainloop()
    
if __name__ == "__main__":
    load_app()