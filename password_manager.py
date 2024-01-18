import json, hashlib, getpass, os, pyperclip, sys # Importing the required modules.
import tkinter as tk # Importing tkinter for GUI.
from tkinter import messagebox
from helpers.texts import texts
from helpers.colors import colors
from helpers.password_generator import generate_password
from cryptography.fernet import Fernet # Importing Fernet from cryptography.fernet for encryption and decryption.

def hash_password(password):
   sha256 = hashlib.sha256()
   sha256.update(password.encode())
   return sha256.hexdigest()


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



# Function to add (save password).
def add_password(website, username, password, confirm_password):
    try:
        # Check if the password and confirm password are the same.
        if password != confirm_password:
                raise ValueError("Passwords do not match!")
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
        password_entry = {'website': website, 'username':username,  'password': encrypted_password}
        data.append(password_entry)
        # Save the updated list back to passwords.json
        with open('passwords.json', 'w') as file:
            # Indent the json data for readability.
            json.dump(data, file, indent=4)
    except (Exception, json.JSONDecodeError) as err:
        print(f"An error occurred while adding password: {err}")
        raise err


# Function to retrieve a saved password.
def get_password(website):
    try :
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
                username = entry['username']
                decrypted_password = decrypt_password(cipher, entry['password'])
                return [username, decrypted_password]
    except Exception as err:
        print(f"An error occurred while getting password: {err}")
        raise err



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
        elif context == texts.welcome_view:
            show_view(center_frame, texts, texts.welcome_view)
        elif context == texts.add_password:
            show_view(center_frame, texts, texts.add_password)
        elif context == texts.get_password:
            show_view(center_frame, texts, texts.get_password)

    # Rest of the code
    pass


# Function to handle the quit choice
def handle_quit():
    # Add your code here to handle the quit choice
    window.destroy()
    sys.exit()


# Function to handle the submit button click
def handle_submit(center_frame, entry1, entry2, entry3, entry4,  context, texts):
    print("User clicked button:", context)
    
    # Add your code here to handle the submit button click
    file = 'user_data.json'
    if context == texts.login and os.path.exists(file):
        # here there are only two entries
        # The third one is fictive
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
        # Here there are three entries
        while continue_adding_passwords:
            website = entry1.get()
            username = entry2.get()
            password = entry3.get()
            confirm_password = entry4.get()
            try:
                add_password(website,username, password, confirm_password)
                messagebox.showinfo(texts.title, "Password added successfully!")
            except (Exception, ValueError) as err:
                print(f"An error occurred while adding password: {err}")
                if isinstance(err, ValueError):
                    messagebox.showerror(texts.title, "Passwords do not match!")
                else:
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
        try:
            show_view(center_frame, texts, texts.password, website)
        except Exception:
            messagebox.showerror(texts.title, "An error occurred while getting password!")


# Function to handle the back button click
def handle_back(center_frame, texts):
    # Add your code here to handle the back button click
    remove_widgets(center_frame)
    show_view(center_frame, texts, texts.welcome)


def remove_widgets(frame):
    # Remove all widgets from the frame
    for widget in frame.winfo_children():
        widget.destroy()


def copyPasswordToClipboard(password):
    try:
        pyperclip.copy(password)
        messagebox.showinfo(texts.title, "Password copied to clipboard!")
    except Exception:
        messagebox.showerror(texts.title, "An error occurred while copying password!")

def show_view(center_frame, texts, view, website=None):
    # Remove all widgets from the frame
    remove_widgets(center_frame)
    # Add your code here to show the initial view
    if view == texts.welcome_view:
        buttons = []
        # Welcome View
        title = tk.Label(center_frame, text=texts.welcome, bg=colors.BLACK, fg=colors.GREEN)
        title.grid(row=0, column=0, padx=10, pady=10)
        login_button = tk.Button(center_frame, text=texts.login, height=2, width=10, bg=colors.BLACK, fg=colors.BLACK, cursor="hand2")
        login_button.grid(row=1, column=0)        
        buttons.append(login_button)

        file = 'user_data.json'
        # Register button
        if not (os.path.exists(file) and os.path.getsize(file) != 0):
            # Show the register button only if the user has not registered
            register_button = tk.Button(center_frame, text=texts.register, height=2, width=10, bg=colors.GREEN, cursor="hand2")
            register_button.grid(row=2, column=0,padx=10, pady=5)
            buttons.append(register_button)
            # Quit button
            quit_button = tk.Button(center_frame, text=texts.quit, height=2, width=10, bg=colors.GREEN, cursor="hand2", foreground=colors.RED)
            quit_button.grid(row=3, column=0, padx=10, pady=5)
        else:
            # Quit button
            quit_button = tk.Button(center_frame, text=texts.quit, height=2, width=10, bg=colors.BLACK, cursor="hand2", )
            quit_button.grid(row=2, column=0, padx=10, pady=5)

        buttons.append(quit_button)
        # Bind the buttons to their respective functions once being loaded
        for button in buttons:
            text = button.cget("text")
            button.configure(command=lambda t=text: handle_click(t, center_frame, texts))

    elif view == texts.login or view == texts.register:
        # Login View
        if view == texts.login:
            title = tk.Label(center_frame, text=texts.login, bg=colors.BLACK, fg=colors.GREEN)
        else:
            # Register View
            title = tk.Label(center_frame, text=texts.register, bg=colors.BLACK, fg=colors.GREEN)

        title.grid(row=0, column=0, padx=10, pady=10)
        #Username input
        username_label = tk.Label(center_frame, text=texts.username, bg=colors.BLACK, fg=colors.GREEN)
        username_label.grid(row=2, column=0, padx=10, pady=5)
        username_entry = tk.Entry(center_frame, relief="solid", bg=colors.BLACK, fg=colors.GREEN, border=1)
        username_entry.grid(row=2, column=1, padx=10, pady=5)
         
        #Password input
        password_label = tk.Label(center_frame, text=texts.password, bg=colors.BLACK, fg=colors.GREEN, border=1)
        password_label.grid(row=3, column=0, padx=10, pady=5)
        password_entry = tk.Entry(center_frame, show="•",  bg=colors.BLACK, fg=colors.GREEN, border=1, relief="solid")
        password_entry.grid(row=3, column=1, padx=10, pady=5)

    
        # Create the submit button
        submit_button = tk.Button(center_frame, text=texts.submit,height=2, width=10, command=lambda: handle_submit(center_frame, username_entry, password_entry,None,None,  view ,texts), cursor="hand2")
        submit_button.grid(row=4, column=0, columnspan=2, padx=10, pady=5)
    
        # Quit button
        quit_button = tk.Button(center_frame, text=texts.quit, height=2, width=10,command=lambda:handle_click( texts.quit, center_frame, texts), cursor="hand2")
        quit_button.grid(row=5, column=0)

        # Back button  / Show welcome view
        back_button = tk.Button(center_frame, text=texts.back,height=2, width=10, command=lambda: handle_click(texts.welcome_view, center_frame, texts), cursor="hand2")
        back_button.grid(row=5, column=1)

    elif view == texts.logged:
        # Logged View
        title = tk.Label(center_frame, text=texts.welcome_back + "\n" + texts.instructions, bg=colors.BLACK, fg=colors.GREEN)
        title.grid(row=0, column=0, padx=10, pady=5)
        # Add Password button
        add_password_button = tk.Button(center_frame, text=texts.add_password,command=lambda: handle_click(texts.add_password,center_frame, texts), height=2, width=10, cursor="hand2")
        add_password_button.grid(row=1, column=0)
        # Get Password button
        get_password_button = tk.Button(center_frame, text=texts.get_password,command=lambda: handle_click(texts.get_password,center_frame, texts), height=2, width=10, cursor="hand2")
        get_password_button.grid(row=2, column=0)
        # Quit button
        quit_button = tk.Button(center_frame, text=texts.quit, height=2, width=10, cursor="hand2")
        quit_button.grid(row=3, column=0)

        # Save all buttons in a list
        buttons = [add_password_button, get_password_button, quit_button]
        # Bind the buttons to their respective functions once being loaded
        for button in buttons:
                text = button.cget("text")
                button.configure(command=lambda t=text: handle_click(t, center_frame, texts))
    elif view == texts.add_password:
        
        title = tk.Label(center_frame, text=texts.add_password, bg="#d3d3d3")
        title.grid(row=0, column=0, padx=10, pady=5)
        # Website input
        website_label = tk.Label(center_frame,relief="solid",border=1, text=texts.website, bg=colors.BLACK, fg=colors.GREEN)
        website_label.grid(row=1, column=0, padx=10, pady=5)
        website_entry = tk.Entry(center_frame)
        website_entry.grid(row=1, column=1, padx=10, pady=5)
        # Username input
        username_label = tk.Label(center_frame, relief="solid",border=1,text=texts.username, bg=colors.BLACK, fg=colors.GREEN)
        username_label.grid(row=2, column=0, padx=10, pady=5)
        username_entry = tk.Entry(center_frame)
        username_entry.grid(row=2, column=1, padx=10, pady=5)

        # Password input
        password_label = tk.Label(center_frame, relief="solid",border=1, text=texts.password, bg=colors.BLACK, fg=colors.GREEN)
        password_label.grid(row=2, column=0, padx=10, pady=10)
        password_entry = tk.Entry(center_frame, show="•")
        password_entry.grid(row=2, column=1, padx=10, pady=10)

        #Generate password button
        generate_password_button = tk.Button(center_frame, text="Generate Password", command=lambda: generate_password(16), height=1, width=10)
        generate_password_button.grid(row=2, column=2, padx=10, pady=10)


        #See password button
        see_password_button = tk.Button(center_frame, text="See Password", command=lambda: password_entry.config(show=""), height=1, width=10)
        see_password_button.grid(row=2, column=3, padx=10, pady=10)

        # Copy the password to the clipboard
        clipboard_button = tk.Button(center_frame, text="Copy to clipboard", command=lambda: copyPasswordToClipboard(password_entry.get()), height=1, width=10)
        # Confirm Password input
        confirm_password_label = tk.Label(center_frame, text="Confirm Password", relief="solid",border=1, bg=colors.BLACK, fg=colors.GREEN)
        confirm_password_label.grid(row=3, column=0, padx=10, pady=5)
        confirm_password_entry = tk.Entry(center_frame, show="•")
        confirm_password_entry.grid(row=3, column=1, padx=10, pady=10)

        # back button/ show logged view
        back_button = tk.Button(center_frame, text=texts.back, command=lambda: handle_click(texts.logged, center_frame, texts), height=1, width=10)
        back_button.grid(row=4, column=0, padx=10, pady=10)

        # Create the submit button
        submit_button = tk.Button(center_frame, text=texts.submit, command=lambda: handle_submit(center_frame, website_entry,username_entry, password_entry, confirm_password_entry, texts.add_password, texts))
        submit_button.grid(row=4, column=1, columnspan=2, padx=10, pady=10)




       

    # get password view
    elif view == texts.get_password:
        title = tk.Label(center_frame, text=texts.get_password, bg=colors.BLACK, fg=colors.GREEN)
        title.grid(row=0, column=0, padx=10, pady=5)

        # Website input
        website_label = tk.Label(center_frame, relief="solid",border=1, text=texts.website, bg=colors.BLACK, fg=colors.GREEN)
        website_label.grid(row=1, column=0, padx=10, pady=5)
        website_entry = tk.Entry(center_frame)
        website_entry.grid(row=1, column=1, padx=10, pady=5)

        # back button/ show logged view
        back_button = tk.Button(center_frame, text=texts.back, command=lambda: handle_click(texts.logged, center_frame, texts), height=1, width=10)
        back_button.grid(row=2, column=0, padx=10, pady=10)
    
        # Create the submit button
        submit_button = tk.Button(center_frame, text=texts.submit, command=lambda: handle_submit(center_frame, website_entry, None, None,None, texts.get_password, texts))
        submit_button.grid(row=2, column=1, padx=10, pady=5)
        
    # Password view
    elif view == texts.password and website is not None:
        # Get the password for the website
        [username, password] = get_password(website)
        # Show the website
        website_label = tk.Label(center_frame,  text="Website:", bg=colors.BLACK, fg=colors.GREEN)
        website_label.grid(row=0, column=0, padx=10, pady=5)
        # Create a StringVar to store the website
        website_var = tk.StringVar()
        website_var.set(website)
        # Create an entry to show the website
        website_entry = tk.Entry(center_frame,relief="solid",border=1,  textvariable=website_var, state="readonly")
        website_entry.grid(row=0, column=1, padx=10, pady=5)

        # Show the username
        username_label = tk.Label(center_frame, text="Username:", bg=colors.BLACK, fg=colors.GREEN)
        username_label.grid(row=1, column=0, padx=10, pady=5)
        # Create a StringVar to store the username
        username_var = tk.StringVar()
        username_var.set(username)
        # Create an entry to show the username

        username_entry = tk.Entry(center_frame, textvariable=username_var, state="readonly", relief="solid",border=1, )
        username_entry.grid(row=1, column=1, padx=10, pady=5)
                # Copy the password to the clipboard
        clipboard_button = tk.Button(center_frame, text="Copy to clipboard", command=lambda: copyPasswordToClipboard(username), height=1, width=10)
        clipboard_button.grid(row=1, column=2, padx=10, pady=5)

        # Show the password
        password_label = tk.Label(center_frame, text="Password", bg=colors.BLACK, fg=colors.GREEN)
        password_label.grid(row=2, column=0, padx=10, pady=5)

        # Create a StringVar to store the password
        password_var = tk.StringVar()
        password_var.set(password)
        # Create an entry to show the password
        password_entry = tk.Entry(center_frame, textvariable=password_var, state="readonly", )
        password_entry.grid(row=2, column=1, padx=10, pady=5)
        # Copy the password to the clipboard
        clipboard_button = tk.Button(center_frame, text="Copy to clipboard", command=lambda: copyPasswordToClipboard(password), height=1, width=10)
        clipboard_button.grid(row=2, column=2, padx=10, pady=5)

        # back button/ show logged view
        back_button = tk.Button(center_frame, text=texts.back, command=lambda: handle_click(texts.logged, center_frame, texts), height=1, width=10)
        back_button.grid(row=3, column=0, padx=10, pady=10)
        #  Show the logged view
        # show_view(center_frame, texts, texts.logged)
    # Center the elements vertically and horizontally within the frame
    center_frame.grid_columnconfigure(0, weight=1)
    center_frame.grid_rowconfigure(1, weight=1)


# Generate a secret key
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

# GUI
print("Opening Password Manager...")
window = tk.Tk()
window.title("Password Manager")
window.configure(bg="orange", width=1000, height=1000)
window.resizable(True, True)
center_frame = tk.Frame(window, bg=colors.BLACK, width=1000, height=1000)
# Center the frame and make it adapt to the window's dimensions
center_frame.pack(fill="both", expand=True)

show_view(center_frame, texts, texts.welcome_view)

window.mainloop()

