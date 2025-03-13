import random
import string
import sys

def get_password_length():
    while True:
        try:
            length = int(input("Enter desired password length (minimum 8 characters): "))
            if length < 8:
                print("Password length must be at least 8 characters!")
                continue
            return length
        except ValueError:
            print("Please enter a valid number!")

def get_complexity_preferences():
    print("\nPassword complexity options:")
    print("1. Letters only (a-z, A-Z)")
    print("2. Letters and numbers")
    print("3. Letters, numbers, and special characters")
    print("4. Custom character set")
    
    while True:
        try:
            choice = int(input("Choose complexity level (1-4): "))
            if 1 <= choice <= 4:
                return choice
            print("Please enter a number between 1 and 4!")
        except ValueError:
            print("Please enter a valid number!")

def get_custom_characters():
    print("\nEnter Y/N for each character type:")
    chars = ""
    if input("Include lowercase letters? (Y/N): ").upper() == 'Y':
        chars += string.ascii_lowercase
    if input("Include uppercase letters? (Y/N): ").upper() == 'Y':
        chars += string.ascii_uppercase
    if input("Include numbers? (Y/N): ").upper() == 'Y':
        chars += string.digits
    if input("Include special characters? (Y/N): ").upper() == 'Y':
        chars += string.punctuation
    
    if not chars:
        print("You must select at least one character type! Using lowercase letters by default.")
        chars = string.ascii_lowercase
    return chars

def generate_password(length, complexity):
    if complexity == 1:
        chars = string.ascii_letters
    elif complexity == 2:
        chars = string.ascii_letters + string.digits
    elif complexity == 3:
        chars = string.ascii_letters + string.digits + string.punctuation
    else:
        chars = get_custom_characters()
    
    # Ensure password has at least one character from each selected type
    password = []
    if string.ascii_lowercase in chars:
        password.append(random.choice(string.ascii_lowercase))
    if string.ascii_uppercase in chars:
        password.append(random.choice(string.ascii_uppercase))
    if string.digits in chars:
        password.append(random.choice(string.digits))
    if string.punctuation in chars:
        password.append(random.choice(string.punctuation))
    
    # Fill the rest of the password length with random characters
    while len(password) < length:
        password.append(random.choice(chars))
    
    # Shuffle the password
    random.shuffle(password)
    return ''.join(password)

def check_password_strength(password):
    strength = 0
    if any(c.islower() for c in password): strength += 1
    if any(c.isupper() for c in password): strength += 1
    if any(c.isdigit() for c in password): strength += 1
    if any(c in string.punctuation for c in password): strength += 1
    
    if strength == 1: return "Weak"
    elif strength == 2: return "Moderate"
    elif strength == 3: return "Strong"
    else: return "Very Strong"

def main():
    while True:
        print("\n=== Password Generator ===")
        length = get_password_length()
        complexity = get_complexity_preferences()
        
        password = generate_password(length, complexity)
        strength = check_password_strength(password)
        
        print("\nGenerated Password:", password)
        print("Password Strength:", strength)
        print("Password Length:", len(password))
        
        if input("\nGenerate another password? (Y/N): ").upper() != 'Y':
            print("Thank you for using the Password Generator!")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
        sys.exit(0)