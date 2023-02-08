# password-manager
password-manager is a python app made with customtkinter and tkinter to store user passwords in encrypted database.

![img.png](img.png)

App supports both dark and light themes.

Current version doesn't support changing master password and exporting database to file.

## Security
Master password is encrypted with salt specific to each user, all other passwords of given user are encrypted with salt used for master password and second salt generated for each entry.
