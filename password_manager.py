import json, hashlib, getpass, os, pyperclip, sys # Importing the required modules.
import tkinter as tk # Importing tkinter for GUI.
from tkinter import messagebox

from cryptography.fernet import Fernet # Importing Fernet from cryptography.fernet for encryption and decryption.


# json is a library for encoding and decoding JSON (JavaScript Object Notation) data, commonly used for data serialization and interchange.

# hashlib is a library that provides secure hash functions, including SHA-256, for creating hash values from data, often used for password hashing and data integrity verification. You can check this tutorial on how to use it.

# getpass: A library for safely and interactively entering sensitive information like passwords without displaying the input on the screen. Similar to the way the Linux terminals are.

# os: A library for interacting with the operating system, allowing you to perform tasks like file and directory manipulation.


# pyperclip: A library for clipboard operations, enabling you to programmatically copy and paste text to and from the clipboard in a platform-independent way.

# sys: This module is a built-in Python module that provides access to various system-specific parameters and functions.

# cryptography.fernet: Part of the cryptography library, it provides the Fernet symmetric-key encryption method for securely encrypting and decrypting data. You can check this tutorial for more info.
# Function for Hashing the Master Password.
def hash_password(password):
   sha256 = hashlib.sha256()
   sha256.update(password.encode())
   return sha256.hexdigest()

print(hash_password("password"));

# Generate a secret key. This should be done only once as the same key is used for encryption and decryption.
def generate_key():
   return Fernet.generate_key()

# Initialize Fernet cipher with the provided key.
def initialize_cipher(key):
   return Fernet(key)

# Function to encrypt a  password.
def encrypt_password(cipher, password):
   return cipher.encrypt(password.encode()).decode()

# Function to decrypt a  password.
def decrypt_password(cipher, encrypted_password):
   return cipher.decrypt(encrypted_password.encode()).decode()

# Function to register you.
def register(username, master_password):
   # Encrypt the master password before storing it
   hashed_master_password = hash_password(master_password)
   user_data = {'username': username, 'master_password': hashed_master_password}
   file_name = 'user_data.json'
   if os.path.exists(file_name) and os.path.getsize(file_name) == 0:
       with open(file_name, 'w') as file:
           json.dump(user_data, file)
           print("\n[+] Registration complete!!\n")
   else:
       with open(file_name, 'x') as file:
           json.dump(user_data, file)
           print("\n[+] Registration complete!!\n")

# Function to login.
def login(center_frame, username, entered_password,texts):
    try:
        with open('user_data.json', 'r') as file:
            user_data = json.load(file)
        
        stored_password_hash = user_data.get('master_password')
        entered_password_hash = hash_password(entered_password)
        
        if entered_password_hash == stored_password_hash and username == user_data.get('username'):
            print("\n[+] Login Successful..\n")
            print("Show logged view")
            show_view(center_frame, texts, "Logged")
        else:
            print("\n[-] Login Failed..\n")
            raise ValueError("Login Failed")
    except ValueError as err:
        print(f"Login Failed: {err}")
        raise
# Function to view saved websites.
def view_websites():
   try:
       # Open the file in read mode.
       with open('passwords.json', 'r') as data:
           # Load the json data.
           view = json.load(data)
           print("\nWebsites you saved...\n")
           for x in view:
               print(x['website'])
           print('\n')
   except FileNotFoundError:
       print("\n[-] You have not saved any passwords!\n")

# Load or generate the encryption key.
key_filename = 'encryption_key.key'
# Check if the key already exists.
if os.path.exists(key_filename):
   # Load the key if it already exists.
   with open(key_filename, 'rb') as key_file:
       key = key_file.read()
else:
   # Generate the key if it does not exist.
   key = generate_key()
   with open(key_filename, 'wb') as key_file:
       key_file.write(key)
# Initialize the cipher.xs
cipher = initialize_cipher(key)


# Function to add (save password).
def add_password(website, password):
   # Check if passwords.json exists
   if not os.path.exists('passwords.json'):
       # If passwords.json doesn't exist, initialize it with an empty list
       data = []
   else:
       # Load existing data from passwords.json
       try:
           with open('passwords.json', 'r') as file:
               data = json.load(file)
       except json.JSONDecodeError:
           # Handle the case where passwords.json is empty or invalid JSON.
           data = []
   # Encrypt the password
   encrypted_password = encrypt_password(cipher, password)
   # Create a dictionary to store the website and password
   password_entry = {'website': website, 'password': encrypted_password}
   data.append(password_entry)
   # Save the updated list back to passwords.json
   with open('passwords.json', 'w') as file:
       # Indent the json data for readability.
       json.dump(data, file, indent=4)

# Function to retrieve a saved password.
def get_password(website):
   # Check if passwords.json exists
   if not os.path.exists('passwords.json'):
       return None
   # Load existing data from passwords.json
   try:
       with open('passwords.json', 'r') as file:
           data = json.load(file)
   except json.JSONDecodeError:
       data = []
   # Loop through all the websites and check if the requested website exists.
   for entry in data:
       if entry['website'] == website:
           # Decrypt and return the password
           decrypted_password = decrypt_password(cipher, entry['password'])
           return decrypted_password
    # Return None if the website was not found.
   return None


def remove_buttons(buttons):
    # Hide the choice buttons
    for button in buttons:
        button.grid_forget()
    
# Function to handle the register choice
def handle_click(context, center_frame, texts):
    print("USer clicked button:", context)
    if context == texts.quit:
        handle_quit()
    else:
        remove_widgets(center_frame)
        if context == texts.login:
            show_view(center_frame, texts, texts.login)
        elif context == texts.register:
            show_view(center_frame, texts, texts.register)
        elif context == texts.logged:
            show_view(center_frame, texts, texts.logged)
        elif context == texts.welcome:
            show_view(center_frame, texts, texts.welcome)
        elif context == texts.add_password:
            show_view(center_frame, texts, texts.add_password)
        elif context == texts.getpassword:
            show_view(center_frame, texts, texts.getpassword)
    # Rest of the code
    pass


# Function to handle the quit choice
def handle_quit():
    # Add your code here to handle the quit choice
    window.destroy()
    sys.exit()


# Function to handle the submit button click
def handle_submit(center_frame, entry1, entry2, context, texts):
    print("User clicked button:", context)
    # Add your code here to handle the submit button click
    file = 'user_data.json'
    if context == texts.login and os.path.exists(file):
        print("Logging in...")
        username = entry1.get()
        master_password = entry2.get()
        try:
            login(center_frame, username, master_password, texts)
        except ValueError:
            messagebox.showerror(texts.title, "Login Credentials not good, try again!")
            show_view(center_frame, texts, texts.login)
    elif context == texts.register :
        if os.path.exists(file) and os.path.getsize(file) != 0:
            show_view(center_frame, texts, texts.welcome_view)
            messagebox.showinfo(texts.title, "Master user already exists!!")
        else:
            print("Needs to register")
            username = entry1.get()
            master_password = entry2.get()
            try:
                register(username, master_password)
                messagebox.showinfo(texts.title, "Registration successful!")
                show_view(center_frame, texts, texts.logged)
            except Exception:
                messagebox.showerror("Password Manager", "An error occurred while registering!")
    elif context == texts.add_password:
        # Initialize a variable to control the loop
        continue_adding_passwords = True

        while continue_adding_passwords:
            website = entry1.get()
            password = entry2.get()
            try:
                add_password(website, password)
                messagebox.showinfo(texts.title, "Password added successfully!")
            except Exception:
                messagebox.showerror(texts.title, "An error occurred while adding password!")
            # Existing code for handle_submit() function
            if messagebox.askyesno(texts.title, "Do you want to add another password?"):
                # Show the add password view again
                show_view(center_frame, texts, texts.add_password)
            else:
                # Stop the loop
                continue_adding_passwords = False
                # Show the logged view  
                show_view(center_frame, texts, texts.logged)
    elif context == texts.get_password:
        website = entry1.get()
        password = get_password(website)
        if password:
            pyperclip.copy(password)
            messagebox.showinfo(texts.title, "Password copied to clipboard!")
        else:
            messagebox.showerror(texts.title, "No password found for the website!")            


# Function to handle the back button click
def handle_back(center_frame, texts):
    # Add your code here to handle the back button click
    remove_widgets(center_frame)

    show_view(center_frame, texts, texts.welcome)
def remove_widgets(frame):
    # Remove all widgets from the frame
    for widget in frame.winfo_children():
        widget.destroy()



def show_view(center_frame, texts, view):
    # Add your code here to show the initial view
    if view == texts.welcome_view:
        buttons = []
        # Welcome View
        title = tk.Label(center_frame, text=texts.welcome, bg="#d3d3d3")
        title.grid(row=0, column=0, padx=10, pady=5)
        login_button = tk.Button(center_frame, text=texts.login, height=1, width=10)
        login_button.grid(row=1, column=0, padx=10, pady=10)
        buttons.append(login_button)

        file = 'user_data.json'
        # Register button
        if not (os.path.exists(file) and os.path.getsize(file) != 0):
            # Show the register button only if the user has not registered
            register_button = tk.Button(center_frame, text=texts.register, height=1, width=10)
            register_button.grid(row=2, column=0, padx=10, pady=10)
            buttons.append(register_button)
            
         # Quit button
        quit_button = tk.Button(center_frame, text=texts.quit, height=1, width=10)
        quit_button.grid(row=3, column=0, padx=10, pady=10)
        buttons.append(quit_button)
        # Bind the buttons to their respective functions once being loaded
        for button in buttons:
            text = button.cget("text")
            button.configure(command=lambda t=text: handle_click(t, center_frame, texts))

    elif view == texts.login or view == texts.register:
        # Login View
        remove_widgets(center_frame)

        if view == texts.login:
            title = tk.Label(center_frame, text=texts.login, bg="#d3d3d3")
        else:
            # Register View
            title = tk.Label(center_frame, text=texts.register, bg="#d3d3d3")

        title.grid(row=0, column=0, padx=10, pady=5)
        #Username input
        username_label = tk.Label(center_frame, text=texts.username, bg="#d3d3d3")
        username_label.grid(row=2, column=0, padx=10, pady=5)
        username_entry = tk.Entry(center_frame)
        username_entry.grid(row=2, column=1, padx=10, pady=5)
         
        #Password input
        password_label = tk.Label(center_frame, text=texts.password, bg="#d3d3d3")
        password_label.grid(row=3, column=0, padx=10, pady=5)
        password_entry = tk.Entry(center_frame)
        password_entry.grid(row=3, column=1, padx=10, pady=5)
    
        # Create the submit button
        submit_button = tk.Button(center_frame, text=texts.submit, command=lambda: handle_submit(center_frame, username_entry, password_entry, view ,texts))
        submit_button.grid(row=4, column=0, columnspan=2, padx=10, pady=5)
    
        # Quit button
        quit_button = tk.Button(center_frame, text=texts.quit, command=lambda:handle_click( texts.quit, center_frame, texts), height=1, width=10)
        quit_button.grid(row=5, column=0, padx=10, pady=10)


    elif view == texts.logged:
        # Logged View
        # Remove all old widgets from the frame
        remove_widgets(center_frame)
        title = tk.Label(center_frame, text=texts.welcome_back + "\n" + texts.instructions, bg="#d3d3d3")
        title.grid(row=0, column=0, padx=10, pady=5)
        # Add Password button
        add_password_button = tk.Button(center_frame, text=texts.add_password,command=lambda: handle_click(texts.add_password,center_frame, texts), height=1, width=10)
        add_password_button.grid(row=1, column=0, padx=10, pady=10)
        # Get Password button
        get_password_button = tk.Button(center_frame, text=texts.get_password,command=lambda: handle_click(texts.get_password,center_frame, texts), height=1, width=10)
        get_password_button.grid(row=2, column=0, padx=10, pady=10)
        # Quit button
        quit_button = tk.Button(center_frame, text=texts.quit, height=1, width=10)
        quit_button.grid(row=3, column=0, padx=10, pady=10)

        # Save all buttons in a list
        buttons = [add_password_button, get_password_button, quit_button]
        # Bind the buttons to their respective functions once being loaded
        for button in buttons:
                text = button.cget("text")
                button.configure(command=lambda t=text: handle_click(t, center_frame, texts))
    elif view == texts.add_password:
        remove_widgets(center_frame)
        title = tk.Label(center_frame, text=texts.add_password, bg="#d3d3d3")
        title.grid(row=0, column=0, padx=10, pady=5)
        # Website input
        website_label = tk.Label(center_frame, text=texts.website, bg="#d3d3d3")
        website_label.grid(row=1, column=0, padx=10, pady=5)
        website_entry = tk.Entry(center_frame)
        website_entry.grid(row=1, column=1, padx=10, pady=5)
        # Password input
        password_label = tk.Label(center_frame, text=texts.password, bg="#d3d3d3")
        password_label.grid(row=2, column=0, padx=10, pady=5)
        password_entry = tk.Entry(center_frame)
        password_entry.grid(row=2, column=1, padx=10, pady=5)
        # Create the submit button
        submit_button = tk.Button(center_frame, text=texts.submit, command=lambda: handle_submit(center_frame, website_entry, password_entry, texts.add_password, texts))
        submit_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5)
        # Quit button
        quit_button = tk.Button(center_frame, text=texts.quit, height=1, width=10)
        quit_button.grid(row=4, column=0, padx=10, pady=10)
        # Add Password View

    # Center the elements vertically and horizontally within the frame
    center_frame.grid_columnconfigure(0, weight=1)
    center_frame.grid_rowconfigure(0, weight=1)

    
# Initialize the user choice to None

# Infinite loop to keep the program running until the user chooses to quit.
        

class Texts:
    def __init__(self, welcome, welcome_view ,welcome_back, title, username, password ,website,login, register, instructions, signature, add_password, get_password, submit, logged, quit):
        self.welcome = welcome
        self.welcome_view = welcome_view
        self.welcome_back = welcome_back
        self.title = title
        self.username = username
        self.password = password
        self.website = website
        self.login = login
        self.register = register
        self.instructions = instructions
        self.signature = signature
        self.add_password = add_password
        self.get_password = get_password
        self.submit = submit
        self.logged = logged
        self.quit = quit


texts = Texts("Welcome to Password Manager, what do you want to do?" , "Welcome" , "Welcome back !", "Password Manager","Username", "Password", "Website", "Login", "Register" ,'''To add password fill all the fields and press "Add Password"
To view password, enter Account Name and press "Get Password"''', "Developed by André Despouys", "Add Password", "Get Password", "Submit", "Logged", "Quit")


# GUI
print("Opening Password Manager...")
window = tk.Tk()
window.title("Password Manager")
window.configure(bg="orange")
window.resizable(True, True)
center_frame = tk.Frame(window, bg="#d3d3d3")
# Center the frame and make it adapt to the window's dimensions
center_frame.pack(fill="both", expand=True)

show_view(center_frame, texts, texts.welcome_view)

window.mainloop()

