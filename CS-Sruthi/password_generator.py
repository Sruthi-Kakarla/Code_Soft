import random
import string

def generate_password(length, include_uppercase=True, include_lowercase=True, 
                      include_numbers=True, include_special=True):
    
    
    uppercase_chars = string.ascii_uppercase
    lowercase_chars = string.ascii_lowercase
    number_chars = string.digits
    special_chars = string.punctuation
    
   
    allowed_chars = ""
    if include_uppercase:
        allowed_chars += uppercase_chars
    if include_lowercase:
        allowed_chars += lowercase_chars
    if include_numbers:
        allowed_chars += number_chars
    if include_special:
        allowed_chars += special_chars
        
    if not allowed_chars:
        print("Error: At least one character type must be selected.")
        return None
    
    password = []
    if include_uppercase:
        password.append(random.choice(uppercase_chars))
    if include_lowercase:
        password.append(random.choice(lowercase_chars))
    if include_numbers:
        password.append(random.choice(number_chars))
    if include_special:
        password.append(random.choice(special_chars))
    
    remaining_length = length - len(password)
    if remaining_length > 0:
        password.extend(random.choices(allowed_chars, k=remaining_length))
    
    random.shuffle(password)
    
    return ''.join(password)

def get_yes_no_input(prompt):
    while True:
        response = input(prompt).lower()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        else:
            print("Please enter 'y' or 'n'.")

def main():
    print("\n===== Password Generator =====\n")
    
    try:
        while True:
            try:
                length = int(input("Enter the desired password length: "))
                if length <= 0:
                    print("Password length must be positive.")
                else:
                    break
            except ValueError:
                print("Please enter a valid number.")
        
        include_uppercase = get_yes_no_input("Include uppercase letters? (y/n): ")
        include_lowercase = get_yes_no_input("Include lowercase letters? (y/n): ")
        include_numbers = get_yes_no_input("Include numbers? (y/n): ")
        include_special = get_yes_no_input("Include special characters? (y/n): ")
        
        if not any([include_uppercase, include_lowercase, include_numbers, include_special]):
            print("Error: You must include at least one character type.")
            return
        
        password = generate_password(
            length, 
            include_uppercase, 
            include_lowercase, 
            include_numbers, 
            include_special
        )
        
        if password:
            print("\n" + "="*40)
            print(f"Generated Password: {password}")
            print("="*40)
            
            strength = "Weak"
            if length >= 12 and sum([include_uppercase, include_lowercase, include_numbers, include_special]) >= 3:
                strength = "Strong"
            elif length >= 8 and sum([include_uppercase, include_lowercase, include_numbers, include_special]) >= 2:
                strength = "Medium"
                
            print(f"Password Strength: {strength}")
            print("="*40)
    
    except KeyboardInterrupt:
        print("\nPassword generation cancelled.")
    
if __name__ == "__main__":
    main()