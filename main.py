
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

def back_root(frame):
    frame.grid_remove()

def exit_app():
    global db
    db.close_db()
    exit()

def sort_table(table,col, reverse):
    # получаем все значения столбцов в виде отдельного списка
    l = [(table.set(k, col), k) for k in table.get_children("")]
    # сортируем список
    l.sort(reverse=reverse)
    # переупорядочиваем значения в отсортированном порядке
    for index,  (_, k) in enumerate(l):
        table.move(k, "", index)
#    в следующий раз выполняем сортировку в обратном порядке
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
    search_window.resizable(False, False)

    search_entry = CTK.CTkEntry(master=search_window,  width = 250)
    search_entry.pack(padx = 20, pady = 20)

    b_cancel = CTK.CTkButton(master=search_window, width=100, text="cancel", command= lambda : cancel_search(table, records, search_window))
    b_cancel.place(relx = 0.09, rely = 0.6)

    def search_in_bd(db, req, table, flag):
        # req = ()
        if flag == "secure":
            db.cursor.execute("SELECT * FROM authInfo WHERE desc LIKE ? OR date LIKE ? OR proc LIKE ?", ('%'+req+'%','%'+req+'%','%'+req+'%',))
        elif flag == "lastlog":
            db.cursor.execute("SELECT * FROM lastLogInfo WHERE user LIKE ? OR proc LIKE ? OR out LIKE ? OR day LIKE ? OR date LIKE ? OR time LIKE ? OR rangeTime LIKE ?", ('%'+req+'%','%'+req+'%','%'+req+'%','%'+req+'%','%'+req+'%','%'+req+'%','%'+req+'%',))
        elif flag == "log_btmp":
            db.cursor.execute("SELECT * FROM btmpLogInfo WHERE user LIKE ? OR proc LIKE ? OR out LIKE ? OR day LIKE ? OR date LIKE ? OR time LIKE ? OR rangeTime LIKE ?", ('%'+req+'%','%'+req+'%','%'+req+'%','%'+req+'%','%'+req+'%','%'+req+'%','%'+req+'%',))
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
    global db, parser, root

    x = 480
    y = 120

    root.wm_geometry("+%d+%d" % (x, y))

    parser.log_secure()
    col = ("date", "time", "proc", "desc")

    frame_table = CTK.CTkFrame(master=root)
    frame_table.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

    frame_buttons = CTK.CTkFrame(master = frame_table)
    frame_buttons.pack(fill="both", expand=True)
    
    b_back = CTK.CTkButton(master=frame_buttons, text="back", command= lambda: back_root(frame_table))
    b_back.grid(row=0, column = 0,padx = 20, pady = 20)

    b_search = CTK.CTkButton(master=frame_buttons, text="search", command= lambda: search(db, table=table, flag="secure", records= records))
    b_search.grid(row=0, column = 2, pady = 20)

    table = ttk.Treeview(master=frame_table, columns=col, show="headings", selectmode="browse")
    table.pack(fill="both", expand=True, anchor="s")

    table.heading("date", text="Date", anchor="n", command=lambda: sort_table(table, 0, False))
    table.heading("time", text="Time", anchor="n", command=lambda: sort_table(table, 1, False))
    table.heading("proc", text="Process", anchor="n")
    table.heading("desc", text="Description", anchor="n")

    table.column("#1", stretch=False, width=100, anchor="center")
    table.column("#2", stretch=False, width=100, anchor="center")
    table.column("#3", stretch=False, width=300, anchor="center")
    table.column("#4", stretch=False, width=800)

    db.cursor.execute("SELECT * FROM authInfo")
    records = db.cursor.fetchall()
    for r in records:
        table.insert("", "end", values=r)

    table.bind('<Motion>', 'break') #запрет изменения размера столбцов

def open_table_last_log():
    global db, parser, root
   
    x = 480
    y = 120

    root.wm_geometry("+%d+%d" % (x, y))
    
    parser.log_last()

    col = ("user","proc","out","day","date","time","rangeTime")

    frame_table = CTK.CTkFrame(master=root)
    frame_table.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

    frame_buttons = CTK.CTkFrame(master = frame_table)
    frame_buttons.pack(fill="both", expand=True)
    
    b_back = CTK.CTkButton(master=frame_buttons, text="back", command= lambda: back_root(frame_table))
    b_back.grid(row=0, column = 0, padx = 20, pady = 20)

    b_search = CTK.CTkButton(master=frame_buttons, text="search", command= lambda: search(db, table=table, flag="lastlog", records=records))
    b_search.grid(row=0, column = 2, pady = 20)

    table = ttk.Treeview(master=frame_table, columns=col, show="headings", selectmode="browse")
    table.pack(fill="both", expand=True, anchor="s")

    table.heading("user", text="User", anchor="n")
    table.heading("proc", text="Proc", anchor="n")
    table.heading("out", text="Out", anchor="n")
    table.heading("day", text="Day", anchor="n")
    table.heading("date", text="Date", anchor="n", command=lambda: sort_table(table, 4, False))
    table.heading("time", text="Time", anchor="n", command=lambda: sort_table(table, 5, False))
    table.heading("rangeTime", text="RangeTime", anchor="n", command=lambda: sort_table(table, 6, False))

    table.column("#1", stretch=False, width=100, anchor="center")
    table.column("#2", stretch=False, width=100, anchor="center")
    table.column("#3", stretch=False, width=100, anchor="center")
    table.column("#4", stretch=False, width=100, anchor="center")
    table.column("#5", stretch=False, width=100, anchor="center")
    table.column("#6", stretch=False, width=100, anchor="center")
    table.column("#7", stretch=False, width=100, anchor="center")

    db.cursor.execute("SELECT * FROM lastLogInfo")
    records = db.cursor.fetchall()
    for r in records:
        table.insert("", "end", values=r)

    table.bind('<Motion>', 'break') #запрет изменения размера столбцов

def open_table_btmp_log():
    global db, parser, root
   
    x = 480
    y = 120

    root.wm_geometry("+%d+%d" % (x, y))
    
    parser.log_btmp()

    col = ("user","proc","out","day","date","time","rangeTime")

    frame_table = CTK.CTkFrame(master=root)
    frame_table.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

    frame_buttons = CTK.CTkFrame(master = frame_table)
    frame_buttons.pack(fill="both", expand=True)
    
    b_back = CTK.CTkButton(master=frame_buttons, text="back", command= lambda: back_root(frame_table))
    b_back.grid(row=0, column = 0, padx = 20, pady = 20)

    b_search = CTK.CTkButton(master=frame_buttons, text="search", command= lambda: search(db, table=table, flag="btmplog", records=records))
    b_search.grid(row=0, column = 2, pady = 20)

    table = ttk.Treeview(master=frame_table, columns=col, show="headings", selectmode="browse")
    table.pack(fill="both", expand=True, anchor="s")

    table.heading("user", text="User", anchor="n")
    table.heading("proc", text="Proc", anchor="n")
    table.heading("out", text="Out", anchor="n")
    table.heading("day", text="Day", anchor="n")
    table.heading("date", text="Date", anchor="n", command=lambda: sort_table(table, 4, False))
    table.heading("time", text="Time", anchor="n", command=lambda: sort_table(table, 5, False))
    table.heading("rangeTime", text="RangeTime", anchor="n", command=lambda: sort_table(table, 6, False))

    table.column("#1", stretch=False, width=100, anchor="center")
    table.column("#2", stretch=False, width=100, anchor="center")
    table.column("#3", stretch=False, width=100, anchor="center")
    table.column("#4", stretch=False, width=100, anchor="center")
    table.column("#5", stretch=False, width=100, anchor="center")
    table.column("#6", stretch=False, width=100, anchor="center")
    table.column("#7", stretch=False, width=100, anchor="center")

    db.cursor.execute("SELECT * FROM btmpLogInfo")
    records = db.cursor.fetchall()
    for r in records:
        table.insert("", "end", values=r)

    table.bind('<Motion>', 'break') #запрет изменения размера столбцов

def main():
    global root
    CTK.set_appearance_mode("System")  # Modes: system (default), light, dark
    CTK.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

    root = CTK.CTk()
    #root.geometry("500x400")
    root.title("authDB")
    root.resizable(False, False)

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

    load_app()

    frame_with_buttons = CTK.CTkFrame(master=root)
    frame_with_buttons.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

    b_secure = CTK.CTkButton(master=frame_with_buttons, text="/var/log/secure", command=open_table_secure_log)
    b_secure.grid(row=0, column = 0, padx = 20, pady = 15)

    b_lastlog = CTK.CTkButton(master=frame_with_buttons, text="/var/log/wtmp", command=open_table_last_log)
    b_lastlog.grid(row=1, column = 0, padx = 20)
    
    b_btmplog = CTK.CTkButton(master=frame_with_buttons, text="/var/log/btmp", command=open_table_btmp_log)
    b_btmplog.grid(row=3, column = 0, padx = 20, pady = 15)

    b_exit = CTK.CTkButton(master=frame_with_buttons, text="exit", command=exit_app)
    b_exit.grid(row=4, column = 0, padx = 20, pady = 30)

    root.mainloop()

if __name__ == "__main__":
    main()