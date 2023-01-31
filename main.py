import sqlite3
from tkinter import Image
from PIL import Image
from account import Account
from entry import Entry
import customtkinter
import tkinter
from utilis import pswd_gen, search_db, all_entries

# TODO finish tkinker gui,
#  resize buttons
#  scrolling,

# TODO store salt and pepper (?)

# TODO db cascade
# TODO sql injection
#TODO find Entry class authentication bug

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        # self.db_user = None
        # self.loginPrompt()

        self.db_user = Account("igornieb", "password")
        self.db_user.login()
        self.mainWindow()

    def loginPrompt(self):
        # GUI part of Login/Register window
        # TODO hide password input but not value
        self.loginWindow = customtkinter.CTkToplevel()
        # self.loginWindow.geometry(f"{500}x{500}")
        self.loginWindow.title("Login/Register")
        self.label = customtkinter.CTkLabel(master=self.loginWindow, text="password-manager login")
        self.label.grid(row=0, column=0, padx=10, pady=10, sticky="NEWS")
        self.loginLabel = customtkinter.CTkLabel(master=self.loginWindow, text="Login:")
        self.loginLabel.grid(row=2, column=0, padx=10, pady=10)
        self.loginEntry = customtkinter.CTkEntry(master=self.loginWindow)
        self.loginEntry.grid(row=2, column=1, padx=10, pady=10, sticky="N")
        self.passwordLabel = customtkinter.CTkLabel(master=self.loginWindow, text="Password:")
        self.passwordLabel.grid(row=3, column=0, padx=10, pady=10)
        self.passwordEntry = customtkinter.CTkEntry(master=self.loginWindow)
        self.passwordEntry.grid(row=3, column=1, padx=10, pady=10, sticky="N")
        self.loginErrorLabel = customtkinter.CTkLabel(master=self.loginWindow, text="")
        self.loginButton = customtkinter.CTkButton(master=self.loginWindow, command=self.login_action, text="Login")
        self.loginButton.grid(row=5, column=0)
        self.registerButton = customtkinter.CTkButton(master=self.loginWindow, command=self.prepare_register,
                                                      text="Register")
        self.registerButton.grid(row=5, column=1)

    def login_action(self):
        # logic behind logging in Login/Register window
        self.db_user = Account(str(self.loginEntry.get()), str(self.passwordEntry.get()))
        if self.db_user.login():
            self.loginWindow.destroy()
            self.mainWindow()
        else:
            self.loginErrorLabel = customtkinter.CTkLabel(master=self.loginWindow, text="Wrong username or password!",
                                                          text_color="red")
            self.loginErrorLabel.grid(row=4, column=0)

    def prepare_register(self):
        # gui for register in Login/Register window
        self.password1Label = customtkinter.CTkLabel(master=self.loginWindow, text="Repeat password:")
        self.password1Label.grid(row=4, column=0, padx=10, pady=10)
        self.password1Entry = customtkinter.CTkEntry(master=self.loginWindow)
        self.password1Entry.grid(row=4, column=1, padx=10, pady=10, sticky="NESW")
        self.loginButton.destroy()
        self.registerButton.destroy()
        self.loginErrorLabel.destroy()
        self.registerButton = customtkinter.CTkButton(master=self.loginWindow, command=self.register_action,
                                                      text="Register").grid(row=6, column=0)

    def register_action(self):
        # logic behind registering in Login/Register window
        if self.password1Entry.get() == self.passwordEntry.get() and len(self.passwordEntry.get()) > 8:
            if len(self.loginEntry.get()) > 3:
                self.db_user = Account(self.loginEntry.get(), self.passwordEntry.get())
                if self.db_user.register():
                    self.loginWindow.destroy()
                    self.loginPrompt()
                else:
                    self.loginErrorLabel.destroy()
                    self.loginErrorLabel = customtkinter.CTkLabel(master=self.loginWindow,
                                                                  text="Username is already in use",
                                                                  text_color="red")
                    self.loginErrorLabel.grid(row=5, column=0, padx=10, pady=10, )
            else:
                self.loginErrorLabel.destroy()
                self.loginErrorLabel = customtkinter.CTkLabel(master=self.loginWindow,
                                                              text="Username length is less than 3",
                                                              text_color="red")
                self.loginErrorLabel.grid(row=5, column=0, padx=10, pady=10, )
        else:
            self.loginErrorLabel = customtkinter.CTkLabel(master=self.loginWindow, padx=10, pady=10,
                                                          text="Repeat password correctly!\nPassword length must be greater than 7",
                                                          text_color="red")
            self.loginErrorLabel.grid(row=5, column=0)

    def mainWindow(self):
        # main gui window of App, should only be shown if db_user is authenticated
        if self.db_user.is_authenticated:
            self.main = customtkinter.CTkToplevel()
            self.main.title("password-manager")
            self.main.geometry(f"{1150}x{500}")

            self.search_frame = customtkinter.CTkFrame(master=self.main, corner_radius=10)
            self.search_frame.grid(row=0, column=0, padx=(10, 0), pady=10)
            self.search_entry = customtkinter.CTkEntry(master=self.search_frame)
            self.search_entry.grid(row=0, column=0, padx=10)
            search_cancel_image = customtkinter.CTkImage(dark_image=Image.open("assets/cancel_d.png"),
                                                    light_image=Image.open("assets/cancel.png"))
            search_cancel_button = customtkinter.CTkButton(master=self.search_frame, text="", image=search_cancel_image, width=1,
                                                           command=self.cancel_search)
            search_cancel_button.grid(row=0, column=1, padx=0)
            search_image = customtkinter.CTkImage(dark_image=Image.open("assets/search_d.png"),
                                                    light_image=Image.open("assets/search.png"))
            search_button = customtkinter.CTkButton(master=self.search_frame, text="", width=4, image=search_image,
                                                    command=lambda: self.search(self.search_entry.get()))
            search_button.grid(row=0, column=2, padx=10, pady=10)
            settings_frame = customtkinter.CTkFrame(master=self.main, corner_radius=10)
            settings_frame.grid(row=0, column=2, padx=10, pady=10, sticky="NESW")
            add_image = customtkinter.CTkImage(dark_image=Image.open("assets/add_d.png"),
                                                    light_image=Image.open("assets/add.png"))
            add_new_btn = customtkinter.CTkButton(master=settings_frame, image=add_image, text="", width=1, command=self.add_entry_frame)
            add_new_btn.grid(row=0, column=0, padx=10, pady=10, sticky="NESW")
            settings_image = customtkinter.CTkImage(dark_image=Image.open("assets/settings_d.png"), light_image=Image.open("assets/settings.png"))
            settings_button = customtkinter.CTkButton(master=settings_frame, image=settings_image, text="", width=1,
                                                      command=self.accountWindow)
            settings_button.grid(row=0, column=1)
            logout_btn = customtkinter.CTkButton(master=settings_frame, text="logout", command=self.logout)
            logout_btn.grid(row=0, column=2, padx=10, pady=10)
            # 2nd row

            self.frame_entries = customtkinter.CTkFrame(master=self.main, corner_radius=10)
            self.frame_entries.grid(row=1, column=0, padx=10, pady=10, sticky="NWES")
            self.show_entries(self.all_entries())
            # frame for editing entry info
            self.frame_entry_info = customtkinter.CTkFrame(master=self.main, corner_radius=10)
            self.frame_entry_info.grid(row=1, column=1, padx=10, pady=10, sticky="NESW")

            self.frame_pswd_generator = customtkinter.CTkFrame(master=self.main, corner_radius=10)
            self.frame_pswd_generator.grid(row=1, column=2, padx=10, pady=10, sticky="NESW")
            self.add_password_generator_content()
        else:
            self.loginPrompt()

    def add_password_generator_content(self):
        label = customtkinter.CTkLabel(master=self.frame_pswd_generator, text="Password generator").grid(row=0,
                                                                                                         column=0,
                                                                                                         padx=10,
                                                                                                         pady=10,
                                                                                                         sticky="NESW")
        frame = customtkinter.CTkFrame(master=self.frame_pswd_generator)
        frame.grid(row=1, column=0, sticky="NESW")
        slider_label = customtkinter.CTkLabel(master=frame, text="Password length").grid(row=0, column=0, padx="10px",
                                                                                         pady=10, sticky="NESW")

        password = customtkinter.CTkEntry(master=frame)
        password.grid(row=1, column=1, padx=10, pady=10, sticky="NESW")

        def get_password(length: int):
            password = customtkinter.CTkEntry(master=frame)
            password.grid(row=1, column=1, padx=10, pady=10, sticky="NESW")
            a = pswd_gen(length)
            password.insert(0, a)

        slider_val = tkinter.IntVar()
        get_password(slider_val.get())
        slider = customtkinter.CTkSlider(master=frame, from_=1, to=25, variable=slider_val, height=20,
                                         command=lambda x: get_password(slider_val.get()))
        slider.grid(row=0, column=1, padx=0, pady=0, sticky="NESW")
        slider_value_label = customtkinter.CTkLabel(master=frame, textvariable=slider_val).grid(row=1, column=0,
                                                                                                padx=10, pady=10,
                                                                                                sticky="NESW")

    def add_entry_frame(self):
        for widget in self.frame_entry_info.winfo_children():
            widget.destroy()

        self.frame_entry_info = customtkinter.CTkFrame(master=self.main, corner_radius=10)
        self.frame_entry_info.grid(row=1, column=1, padx=10, pady=10, sticky="NESW")
        self.frame_website_label = customtkinter.CTkLabel(master=self.frame_entry_info, text=f"Add new entry")
        self.frame_website_label.grid(row=0, column=0, padx=10, pady=10)
        self.frame_website_label = customtkinter.CTkLabel(master=self.frame_entry_info, text=f"Website:")
        self.frame_website_label.grid(row=1, column=0, padx=10, pady=10)
        self.frame_website_entry = customtkinter.CTkEntry(master=self.frame_entry_info)
        self.frame_website_entry.grid(row=1, column=1, padx=10, pady=10)
        self.frame_username_label = customtkinter.CTkLabel(master=self.frame_entry_info, text="Username:")
        self.frame_username_label.grid(row=2, column=0, padx=10, pady=10)
        self.frame_username_entry = customtkinter.CTkEntry(master=self.frame_entry_info)
        self.frame_username_entry.grid(row=2, column=1, padx=10, pady=10)
        self.frame_password_label = customtkinter.CTkLabel(master=self.frame_entry_info, text="Password:")
        self.frame_password_label.grid(row=3, column=0, padx=10, pady=10)
        self.frame_password_entry = customtkinter.CTkEntry(master=self.frame_entry_info)
        self.frame_password_entry.grid(row=3, column=1, padx=10, pady=10)
        self.frame_save = customtkinter.CTkButton(master=self.frame_entry_info, text="Add", command=self.add_new_entry)
        self.frame_save.grid(row=4, column=0, padx=10, pady=10, sticky="NESW")

    def add_new_entry(self):
        # TODO test (sm is wrong...)
        if len(self.frame_username_entry.get()) > 2 and len(self.frame_website_entry.get()) > 2 and len(
                self.frame_password_entry.get()) > 2:
            e = Entry(-1, self.db_user, self.frame_username_entry.get(), self.frame_website_entry.get(),
                      self.frame_password_entry.get())
            e.add()
            self.show_entries(all_entries(self.db_user))
            for widget in self.frame_entry_info.winfo_children():
                widget.destroy()

    def accountWindow(self):
        # GUI of user settings menu
        self.settings = customtkinter.CTkToplevel()
        self.settings.title("Account settings")
        settings_label = customtkinter.CTkLabel(master=self.settings, text=f"Hello {self.db_user.username}")
        settings_label.grid(row=0, column=0, padx=10, pady=10)
        frame1 = customtkinter.CTkFrame(master=self.settings, corner_radius=10)
        frame1.grid(row=1, column=0, padx=10, pady=10)
        settings_frame = customtkinter.CTkFrame(master=frame1, corner_radius=10)
        settings_frame.grid(row=1, column=0, padx=10, pady=10)

        change_password_label = customtkinter.CTkLabel(master=frame1, text="Change password")
        change_password_label.grid(row=0, column=0, padx=10, pady=10)

        old_password_label = customtkinter.CTkLabel(master=settings_frame, text="Old password")
        old_password_label.grid(row=1, column=0, padx=10, pady=10)
        new_password_label = customtkinter.CTkLabel(master=settings_frame, text="New password")
        new_password_label.grid(row=2, column=0, padx=10, pady=10)
        new_password1_label = customtkinter.CTkLabel(master=settings_frame, text="Repeat new password")
        new_password1_label.grid(row=3, column=0, padx=10, pady=10)

        old_password_entry = customtkinter.CTkEntry(master=settings_frame)
        old_password_entry.grid(row=1, column=1, padx=10, pady=10)
        new_password_entry = customtkinter.CTkEntry(master=settings_frame)
        new_password_entry.grid(row=2, column=1, padx=10, pady=10)
        new_password1_entry = customtkinter.CTkEntry(master=settings_frame)
        new_password1_entry.grid(row=3, column=1, padx=10, pady=10)

        error_label = customtkinter.CTkLabel(master=settings_frame, text="", text_color="red")
        error_label.grid(row=4, column=1, padx=10, pady=10)

        change_password_button = customtkinter.CTkButton(master=frame1, text="Change password")
        change_password_button.grid(row=2, column=0, padx=10, pady=10)

        export_frame = customtkinter.CTkFrame(master=self.settings, corner_radius=10)
        export_frame.grid(row=2, column=0, padx=10, pady=10, sticky="NESW")
        export_btn = customtkinter.CTkButton(master=export_frame, text="Export all data to file",
                                             command=self.export_entries_to_file)
        export_btn.grid(row=0, column=0, padx=10, pady=10, sticky="SW")
        delete_account_btn = customtkinter.CTkButton(master=export_frame, text="Delete account",
                                                     command=self.confirm_delete)
        delete_account_btn.grid(row=0, column=1, padx=10, pady=10, sticky="SW")

    def confirm_delete(self):
        alert = customtkinter.CTkToplevel()
        label = customtkinter.CTkLabel(master=alert, text="Are you sure?")
        label.grid(row=0, column=0, padx=10, pady=10, sticky="NESW")
        confirm_btn = customtkinter.CTkButton(master=alert, text="Yes", command=lambda: delete_account())
        confirm_btn.grid(row=1, column=0, padx=10, pady=10, sticky="NESW")
        cancel_btn = customtkinter.CTkButton(master=alert, text="No", command=lambda: alert.destroy())
        cancel_btn.grid(row=1, column=1, padx=10, pady=10, sticky="NESW")

        def delete_account():
            self.db_user.delete()
            self.settings.destroy()
            alert.destroy()
            self.logout()

    def copy_to_clipboard(self, value: str):
        # copy given value to clipboard
        self.main.clipboard_clear()
        self.main.clipboard_append(value)
        self.main.update()

    def export_entries_to_file(self):
        # TODO
        # show dialog for selecting location, save to that location
        pass

    def cancel_search(self):
        # returns to default view of mainWindow method
        self.search_entry = customtkinter.CTkEntry(master=self.search_frame)
        self.search_entry.grid(row=0, column=0, padx=10)
        self.show_entries(self.all_entries())

    def show_entries(self, entries):
        # gui part of showing passwords in mainWindow method
        # clear frame
        for widget in self.frame_entries.winfo_children():
            widget.destroy()
        # for each entry create own frame
        i = 0
        if len(entries) == 0:
            self.not_found_label = customtkinter.CTkLabel(master=self.frame_entries, text="Nothing was found")
            self.not_found_label.grid(row=0, column=0, padx=10, pady=10, sticky="nesw")

        for entry in entries:
            frame_entry = customtkinter.CTkFrame(master=self.frame_entries, corner_radius=10)
            frame_entry.grid(row=i, column=0, padx=10, pady=10, sticky="news")
            entry_webiste_label = customtkinter.CTkLabel(master=frame_entry, text=f"{entry.website}")
            entry_webiste_label.grid(row=0, column=0, padx=10, sticky="nesw")
            entry_username_label = customtkinter.CTkLabel(master=frame_entry, text=f"{entry.username}")
            entry_username_label.grid(row=1, column=0, padx=(20, 10), sticky="EW")
            entry_edit_image = customtkinter.CTkImage(dark_image=Image.open("assets/edit_d.png"),
                                                    light_image=Image.open("assets/edit.png"))
            entry_edit_button = customtkinter.CTkButton(master=frame_entry, text="", image=entry_edit_image,width=1, command=lambda entry=entry: self.show_entry_info(entry))
            entry_edit_button.grid(row=1, column=2, padx=10, pady=10, sticky="EW")
            i += 1

    def show_entry_info(self, entry: Entry):
        # gui part of showing detailed entry info
        for widget in self.frame_entry_info.winfo_children():
            widget.destroy()
        self.frame_website_label = customtkinter.CTkLabel(master=self.frame_entry_info, text=f"Website:")
        self.frame_website_label.grid(row=0, column=0, padx=10, pady=10)
        self.frame_website_entry = customtkinter.CTkEntry(master=self.frame_entry_info)
        self.frame_website_entry.grid(row=0, column=1, padx=10, pady=10)
        self.frame_website_entry.insert(0, entry.website)
        copy_image = customtkinter.CTkImage(dark_image=Image.open("assets/copy_d.png"),
                                                  light_image=Image.open("assets/copy.png"))
        self.frame_website_copy = customtkinter.CTkButton(master=self.frame_entry_info, text="", image=copy_image, width=1,
                                                          command=lambda: self.copy_to_clipboard(
                                                              self.frame_website_entry.get()))
        self.frame_website_copy.grid(row=0, column=2, padx=10, pady=10)

        self.frame_username_label = customtkinter.CTkLabel(master=self.frame_entry_info, text="Username:")
        self.frame_username_label.grid(row=1, column=0, padx=10, pady=10)
        self.frame_username_entry = customtkinter.CTkEntry(master=self.frame_entry_info)
        self.frame_username_entry.grid(row=1, column=1, padx=10, pady=10)
        self.frame_username_entry.insert(0, entry.username)
        self.frame_username_copy = customtkinter.CTkButton(master=self.frame_entry_info, text="", image=copy_image, width=1,
                                                           command=lambda: self.copy_to_clipboard(
                                                               self.frame_username_entry.get()))
        self.frame_username_copy.grid(row=1, column=2, padx=10, pady=10)

        self.frame_password_label = customtkinter.CTkLabel(master=self.frame_entry_info, text="Password:")
        self.frame_password_label.grid(row=2, column=0, padx=10, pady=10)
        self.frame_password_entry = customtkinter.CTkEntry(master=self.frame_entry_info)
        self.frame_password_entry.grid(row=2, column=1, padx=10, pady=10)
        self.frame_password_entry.insert(0, entry.decrypt())

        self.frame_password_copy = customtkinter.CTkButton(master=self.frame_entry_info, text="", image=copy_image, width=1,
                                                           command=lambda: self.copy_to_clipboard(
                                                               self.frame_password_entry.get()))
        self.frame_password_copy.grid(row=2, column=2, padx=10, pady=10)
        self.frame_save = customtkinter.CTkButton(master=self.frame_entry_info, text="Save",
                                                  command=lambda: self.update_entry(entry))
        self.frame_save.grid(row=3, column=1, padx=10, pady=10, sticky="NESW")
        delete_image = customtkinter.CTkImage(dark_image=Image.open("assets/delete_d.png"),
                                                  light_image=Image.open("assets/delete.png"))

        self.frame_delete = customtkinter.CTkButton(master=self.frame_entry_info, text="", image=delete_image, width=1,
                                                    command=lambda: self.delete_entry(entry))
        self.frame_delete.grid(row=3, column=2, padx=10, pady=10, sticky="NESW")

    def delete_entry(self, entry: Entry):
        alert = customtkinter.CTkToplevel()
        label = customtkinter.CTkLabel(master=alert, text="Are you sure?")
        label.grid(row=0, column=0, padx=10, pady=10, sticky="NESW")
        confirm_btn = customtkinter.CTkButton(master=alert, text="Yes", command=lambda: delete_entry())
        confirm_btn.grid(row=1, column=0, padx=10, pady=10, sticky="NESW")
        cancel_btn = customtkinter.CTkButton(master=alert, text="No", command=lambda: alert.destroy())
        cancel_btn.grid(row=1, column=1, padx=10, pady=10, sticky="NESW")

        def delete_entry():
            entry.delete()
            alert.destroy()
            self.show_entries(all_entries(self.db_user))
            for widget in self.frame_entry_info.winfo_children():
                widget.destroy()

    def update_entry(self, entry: Entry):
        if len(self.frame_username_entry.get()) > 2 and len(self.frame_website_entry.get()) > 2 and len(
                self.frame_password_entry.get()) > 2:
            if entry.update(self.frame_username_entry.get(), self.frame_website_entry.get(),
                            self.frame_password_entry.get()):
                self.show_entries(all_entries(self.db_user))
                frame_message_label = customtkinter.CTkLabel(master=self.frame_entry_info, text="Update succesful",
                                                             text_color="green")
                frame_message_label.grid(row=4, column=1, padx=10, pady=10, sticky="NESW")
            else:
                frame_message_label = customtkinter.CTkLabel(master=self.frame_entry_info, text="error",
                                                             text_color="red")
                frame_message_label.grid(row=4, column=1, padx=10, pady=10, sticky="NESW")
        else:
            frame_message_label = customtkinter.CTkLabel(master=self.frame_entry_info, text="Update is too short",
                                                         text_color="red")
            frame_message_label.grid(row=4, column=1, padx=10, pady=10, sticky="NESW")

    def search(self, query):
        # search database and show results in mainWindow
        data = search_db(self.db_user, str(query))
        self.show_entries(data)

    def all_entries(self):
        # show all entries
        return all_entries(self.db_user)

    def logout(self):
        self.db_user = None
        self.main.destroy()
        self.loginPrompt()


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
