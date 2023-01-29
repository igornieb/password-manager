import sqlite3
from account import Account
from entry import Entry
import tkinter
import customtkinter

# TODO tkinker gui, scroling
# TODO copy to clipboard on click
# TODO store salt and pepper (?)


customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        # TODO login
        ########
        self.db_user = None
        self.db_user = Account("igornieb", "password")
        #user.register()
        self.db_user.login()
        ##########
        #
        self.title("password-manager")
        self.geometry(f"{1000}x{500}")
        # first row
        self.columnconfigure(0)
        # TODO search logic, resize buttons, cancel search
        self.search_frame = customtkinter.CTkFrame(master=self, corner_radius=10)
        self.search_frame.grid(row=0, column=0, padx=10, pady=10)
        self.search_entry = customtkinter.CTkEntry(master=self.search_frame)
        self.search_entry.grid(row=0, column=0, padx=20)
        self.search_cancel_button = customtkinter.CTkButton(master=self.search_frame, text="cancel",
                                                            command=self.button_callback)
        self.search_cancel_button.grid(row=0, column=1)
        self.search_button = customtkinter.CTkButton(master=self.search_frame, text="search", command=self.search)
        self.search_button.grid(row=0, column=2, padx=10, pady=10)
        self.logout_frame = customtkinter.CTkFrame(master=self, corner_radius=10)
        self.logout_frame.grid(row=0, column=1, padx=10, pady=10)
        self.logout_btn = customtkinter.CTkButton(master=self.logout_frame, text="logout", command=self.logout)
        self.logout_btn.grid(row=0, column=0, padx=10, pady=10)
        # 2nd row

        self.frame_entries = customtkinter.CTkFrame(master=self, corner_radius=10)
        self.frame_entries.grid(row=1, column=0, padx=10, pady=10)
        self.show_entries(self.all_entries())
        # frame for editing entry info
        self.frame_entry_info = customtkinter.CTkFrame(master=self, corner_radius=10)
        self.frame_entry_info.grid(row=1, column=1, padx=10, pady=10, sticky="N")


    def show_entries(self, entries):
        # for each entry create own frame
        # TODO fix naming
        i=0
        for entry in entries:
            self.frame_entry = customtkinter.CTkFrame(master=self.frame_entries, corner_radius=10)
            self.frame_entry.grid(row=i, column=0, padx=10, pady=10)
            self.entry_webiste_label = customtkinter.CTkLabel(master=self.frame_entry, text=f"{entry.website}")
            self.entry_webiste_label.grid(row=0, column=0, padx=10)
            self.entry_username_label = customtkinter.CTkLabel(master=self.frame_entry, text=f"{entry.username}")
            self.entry_username_label.grid(row=1, column=1, padx=10)
            self.entry_edit_button = customtkinter.CTkButton(master=self.frame_entry, text="Edit",
                                                             command=self.show_entry_info)
            self.entry_edit_button.grid(row=1, column=2)
            i+=1

    def show_entry_info(self):
        data = [self.entry_username_label.cget("text"), self.entry_webiste_label.cget("text")]
        self.frame_website_label = customtkinter.CTkLabel(master=self.frame_entry_info, text=f"Website:{data[1]}")
        self.frame_website_label.grid(row=0, column=0, padx=10, pady=10)
        self.frame_website_entry = customtkinter.CTkEntry(master=self.frame_entry_info)
        self.frame_website_entry.grid(row=0, column=1, padx=10, pady=10)
        self.frame_website_copy = customtkinter.CTkButton(master=self.frame_entry_info, text="copy",
                                                          command=self.button_callback)
        self.frame_website_copy.grid(row=0, column=2, padx=10, pady=10)

        self.frame_username_label = customtkinter.CTkLabel(master=self.frame_entry_info, text="Username:")
        self.frame_username_label.grid(row=1, column=0, padx=10, pady=10)
        self.frame_username_entry = customtkinter.CTkEntry(master=self.frame_entry_info)
        self.frame_username_entry.grid(row=1, column=1, padx=10, pady=10)
        self.frame_username_copy = customtkinter.CTkButton(master=self.frame_entry_info, text="copy",
                                                           command=self.button_callback)
        self.frame_username_copy.grid(row=1, column=2, padx=10, pady=10)

        self.frame_password_label = customtkinter.CTkLabel(master=self.frame_entry_info, text="Password:")
        self.frame_password_label.grid(row=2, column=0, padx=10, pady=10)
        self.frame_password_entry = customtkinter.CTkEntry(master=self.frame_entry_info)
        self.frame_password_entry.grid(row=2, column=1, padx=10, pady=10)
        self.frame_password_copy = customtkinter.CTkButton(master=self.frame_entry_info, text="copy",
                                                           command=self.button_callback)
        self.frame_password_copy.grid(row=2, column=2, padx=10, pady=10)

        self.frame_save = customtkinter.CTkButton(master=self.frame_entry_info, text="Save",
                                                  command=self.button_callback())
        self.frame_save.grid(row=3, column=1, padx=10, pady=10)

    def button_callback(self):
        print(self.search_entry.get())

    def search(self):
        self.show_entries([])

    def all_entries(self):
        return all_entries(self.db_user)

    def logout(self):
        # TODO return to login page
        exit()


def search_db(user: Account, query: str):
    results = []
    if user.is_authenticated():
        db_conn = sqlite3.connect('password-manager.sqlite')
        c = db_conn.cursor()
        db_query = c.execute(
            f'''SELECT username, website, password FROM entries WHERE owner="{user.username}" AND username LIKE "%{query}%" OR website like "%{query}%"''')
        for res in db_query:
            results.append(Entry(user, res[0], res[1], res[2]))
        db_conn.close()
    return results


def all_entries(user: Account):
    results = []
    if user.is_authenticated():
        db_conn = sqlite3.connect('password-manager.sqlite')
        c = db_conn.cursor()
        db_query = c.execute(
            f'''SELECT username, website, password FROM entries WHERE owner="{user.username}"''')
        for res in db_query:
            results.append(Entry(user, res[0], res[1], res[2]))
        db_conn.close()
    return results


def test():
    app = App()
    app.mainloop()
    # user = Account("igornieb", "password")
    # #user.register()
    # user.login()
    # e = Entry(user,"igorn","www.polska.pl", "skomplikowane hslo")
    # print(search_db(user, "igor"))


if __name__ == "__main__":
    try:
        db_conn = sqlite3.connect('password-manager.sqlite')
        c = db_conn.cursor()
        c.execute(
            '''CREATE TABLE accounts (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, salt TEXT, password TEXT)''')
        c.execute(
            '''CREATE TABLE entries (id INTEGER PRIMARY KEY AUTOINCREMENT, owner TEXT, username TEXT, website TEXT, password TEXT, FOREIGN KEY(owner) REFERENCES accounts(username))''')
        db_conn.commit()
        db_conn.close()
        test()
    except:
        test()
