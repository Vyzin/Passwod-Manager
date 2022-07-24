from email import message
from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def gen_pass():
    pass_input.delete(0,END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = []

    password_letters = [random.choice(letters) for char in range(random.randint(8, 10))]
    password_list.extend(password_letters)

    password_symbols = [random.choice(symbols) for char in range(random.randint(2, 4))]
    password_list.extend(password_symbols)

    password_numbers = [random.choice(numbers) for char in range(random.randint(2, 4))]
    password_list.extend(password_numbers)

    random.shuffle(password_list)

    password = "".join(password_list)
    pass_input.insert(0,password)
    pyperclip.copy(password)
# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():

    website = website_input.get()
    email_user = email_user_input.get()
    password = pass_input.get()
    new_data = {
        website: {
            "email": email_user,
            "password": password,
        }
    }

    if len(website) == 0 or len(email_user) == 0 or len(password) == 0:
        messagebox.showwarning(title="Fields Empty", message="Please do not leave any fields empty!")
    else:
        try:
            with open("passwords.json", "r") as f:
                #Reading old data
                passwords = json.load(f)
        except FileNotFoundError:
            with open("passwords.json", "w") as f:
                json.dump(new_data, f, indent=4)
        else:
            #Updating old data with new data
            passwords.update(new_data)
            
            with open("passwords.json", "w") as f:
                #Saving updated data
                json.dump(passwords, f, indent=4)
        finally:
            website_input.delete(0,END)
            pass_input.delete(0,END)
            website_input.focus()


# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website = website_input.get()
    try:
        with open("passwords.json", "r") as f:
            passwords = json.load(f)
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="Passwords File Does Not Exist")
    else:
        try:
            email_user = passwords[website]["email"]
            password = passwords[website]["password"]
            messagebox.showinfo(title=f"{website} Account Info", message=f"Email/User: {email_user}\nPassword: {password}")
        except KeyError:
            messagebox.showerror(title=f"Error", message=f"'{website}' Details Does Not Exist")

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50,pady=50)

canvas = Canvas(height=205,width=205)
logo = PhotoImage(file="lock.png")
canvas.create_image(105,105, image=logo)
canvas.grid(column=1,row=0)

#Label

website_label = Label(text="Website:")
website_label.grid(column=0,row=1)

email_user_label = Label(text="Email/Username:")
email_user_label.grid(column=0,row=2)

pass_label = Label(text="Password:")
pass_label.grid(column=0,row=3)

#Entrys/Inputs

website_input = Entry(width=17)
website_input.grid(column=1,row=1)
website_input.focus()

email_user_input = Entry(width=35)
email_user_input.grid(column=1,row=2, columnspan=2)
#If you want your email/username to be automatically there, put your email/username inside the quotations!
email_user_input.insert(0, "")

pass_input = Entry(width=17)
pass_input.grid(column=1,row=3)

#Buttons

generate_button = Button(text="Generate Password", command = gen_pass)
generate_button.grid(column=2,row=3)

add_button = Button(text="Add", width=36, command = save)
add_button.grid(column=1,row=4,columnspan=2)

search_button = Button(text="Search", command = find_password)
search_button.grid(column=2,row=1)

window.mainloop()