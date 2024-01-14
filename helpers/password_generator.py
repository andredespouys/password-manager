import random
import array
import  pyperclip # Importing the required modules.
from tkinter import messagebox


from helpers.useful_variables import *
def copyPasswordToClipboard(password):
    try:
        pyperclip.copy(password)
        messagebox.showinfo("Generator", "Password copied to clipboard!")
    except Exception:
        messagebox.showerror("Generator", "An error occurred while copying password!")
def generate_password(password_length):
    try:
        # # Combines all the character arrays above to form one array
        COMBINED_LIST = DIGITS + UPCASE_CHARACTERS + LOCASE_CHARACTERS + SYMBOLS

        # Randomly select at least one character from each character set above
        rand_digit = random.choice(DIGITS)
        rand_upper = random.choice(UPCASE_CHARACTERS)
        rand_lower = random.choice(LOCASE_CHARACTERS)
        rand_symbol = random.choice(SYMBOLS)

        # Combine the characters randomly selected above
        # At this stage, the password contains only 4 characters but
        # We want a password with the desired length
        temp_pass = rand_digit + rand_upper + rand_lower + rand_symbol

        # Now that we are sure we have at least one character from each
        # set of characters, we fill the rest of the password length by selecting randomly from the combined
        # list of characters above.
        for x in range(password_length - 4):
            temp_pass += random.choice(COMBINED_LIST)

        # Convert temporary password into an array and shuffle to
        # Prevent it from having a consistent pattern
        # Where the beginning of the password is predictable
        temp_pass_list = array.array('u', temp_pass)
        random.shuffle(temp_pass_list)

        # Traverse the temporary password array and append the characters
        # to form the password
        password = ""
        for x in temp_pass_list:
            password += x
        try:
            copyPasswordToClipboard(password)
        except Exception:
            raise Exception("An error occurred while copying password!")
        return password
    except Exception as e:
        print(e)
        return None

# Example usage:
# generated_password = generate_password(14)
# print(generated_password)
