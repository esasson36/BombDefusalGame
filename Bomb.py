from collections import Counter
import random
import string
import time

while True:
    serial_length = random.randint(5,9)
    serial_chars = string.ascii_uppercase + string.digits
    serial_number = ''.join(random.choice(serial_chars) for _ in range(serial_length))
    completed_modules = []
    time_limit = 180
    start_time = time.time()
    chosen_wire_num = None
    all_modules = [ "wires", "keypad", "morse", "password"]
    game_over = False
    
    
    print("You're trying to defuse a bomb, solve all 4 modules to defuse it")
    print(f"Serial Number: {serial_number}")
    
    while True:
        elapsed = time.time() - start_time
        remaining_time = int(time_limit - elapsed)
        
        if remaining_time <= 0:
            print("\nTime's up! The bomb exploded!")
            game_over = True
            break
        
        print(f"Time left: {remaining_time} seconds")
        
        if set(completed_modules) == set(all_modules):
            print("\nYou've completed all the modules! The Bomb has been defused!")
            break
        
        available_modules = [m.capitalize() for m in all_modules if m not in completed_modules]
        print("\nThe modules are:",",".join(available_modules))
        module_choice = input("Choose a module to start or type 'Manual' for help. \n").lower()
        
        if module_choice == "wires":
            if "wires" in completed_modules:
                print("You've already done this module.")
                continue
            
            print("Starting Wires module...")
            colors = ["red", "blue", "green", "yellow", "black"]
            wires = []
            color_counts = Counter()
        
            while len(wires) < 5:
                color = random.choice(colors)
                if color_counts[color] < 2:
                    wires.append(color)
                    color_counts[color] += 1
                
            for i, color in enumerate(wires, start=1):
                print(f"{i}. {color}")
            most_common_colors = color_counts.most_common()
            highest_freq = most_common_colors[0][1]
            top_colors = [color for color, count in most_common_colors if count == highest_freq]
        
            priority = ["blue", "red", "black", "yellow", "green"]
            top_colors.sort(key=lambda c: priority.index(c))
        
            vowels = [ 'A', 'E', 'I', 'O', 'U']
            last_char = serial_number[-1]
            length_even = (len(serial_number) % 2 == 0)
        
            if last_char.isdigit():
                correct_index = 4
            elif length_even and last_char in vowels:
                correct_index = 0
            elif length_even and last_char not in vowels:
                correct_index = 1
            elif not length_even and last_char in vowels:
                correct_index = 2
            else:
                correct_index = 3
            wire_choice = input("Which wire do you want to cut? (Enter a number 1-5)\n").lower()
            if not wire_choice.isdigit() or not (1 <= int(wire_choice) <= 5):
                print("Invalid choice.")
            else:
                chosen_index = int(wire_choice) - 1 
                if chosen_index == correct_index:
                    print("You cut the right wire! Module completed. ")
                    completed_modules.append("wires")
                    chosen_wire_num = chosen_index + 1
                else:
                    print("You cut the wrong wire. You Died.")
                    game_over = True
                    break
                
        elif module_choice == "keypad":
            if "keypad" in completed_modules:
                print("You've already done this module.")
                continue
            print("Starting Keypad module...")
            first_digit = None
            for ch in serial_number:
                if ch.isdigit():
                    first_digit = int(ch)
                    break
                if first_digit is None:
                    first_digit = 0
            second_digit = chosen_wire_num if "wires" in completed_modules  else 0
            
            third_digit = len([m for m in completed_modules if m != "keypad"])
            
            fourth_digit = len(serial_number)
            
            code = f"{first_digit}{second_digit}{third_digit}{fourth_digit}"
            
            user_input = input("Enter the 4 digit code:  ")
            if user_input == code:
                print("Correct code! Module completed.")
                completed_modules.append("keypad")
            else:
                print("Incorrect code. You Died")
                game_over = True
                break
        
        elif module_choice == "morse":
            print("Starting Morse code module...")
            
            morse_dict = { 
                'A': '.-',    'B': '-...',  'C': '-.-.',
        'D': '-..',   'E': '.',     'F': '..-.',
        'G': '--.',   'H': '....',  'I': '..',
        'J': '.---',  'K': '-.-',   'L': '.-..',
        'M': '--',    'N': '-.',    'O': '---',
        'P': '.--.',  'Q': '--.-',  'R': '.-.',
        'S': '...',   'T': '-',     'U': '..-',
        'V': '...-',  'W': '.--',   'X': '-..-',
        'Y': '-.--',  'Z': '--..'
    }
            word_list = ["CODE", "CRACKED", "DEFUSE", "BACKPACK", "EXPLODE", "PHONE", "PLANE", "LOCKHEED", "NAVY", "MACHINE"]
            selected_word = random.choice(word_list)
            morse_code = ""
            for letter in selected_word:
                morse_code += morse_dict[letter] + " "
                
            print(morse_code.strip())
            guess = input("Decode this to complete the module\n").strip().upper()
                
            if guess == selected_word:
                print("Correct! Module completed.")
                completed_modules.append("morse")
            else:
                print("Wrong word, You Died")
                game_over = True
                break
            
        elif module_choice == "password":
            print("Starting Password module...")
            password_options = ["PASSWORD", "EXPLOSIVE", "RANGER", "FIGHTER", "TRIGGER", "CIRCUIT", "TIMER", "COMPUTER", "PYTHON"]
            key_options = ["MODULE", "MORSE", "VIGENERE", "SERIAL", "NUMBER", "KEYPAD", "WIRES", "CIPHER"]
            password = random.choice(password_options).upper()
            key = random.choice(key_options).upper()
            
            encrypted_password = ""
            key_index = 0
            
            for letter in password:
                if letter.isalpha():
                    shift = ord(key[key_index % len(key)]) - ord('A')
                    encrypted_char = chr((ord(letter) - ord('A') + shift) % 26 + ord('A'))
                    encrypted_password += encrypted_char
                    key_index += 1
                else:
                    encrypted_password += letter
            print("Find the key and decrypt the password below")
            print("Encrypted password:", encrypted_password)
            user_decrypted = input("Enter the decrypted password:  ").strip().upper()
            if user_decrypted == password:
                print("Correct! Module completed.")
                completed_modules.append("password")
            else:
                print("Wrong password. You Died.")
                game_over = True
                break
        
        elif module_choice == "manual":
             print("""
Wires - Rule 1: If the number of characters in the serial number is even and ends in a vowel, cut the 1st wire.
Rule 2: If the number of characters is even and ends with a consonant, cut the 2nd wire.
Rule 3: If the number of characters is odd and it ends with a vowel, cut the 3rd wire.
Rule 4: If the number of characters is odd and ends with a consonant, cut the 4th wire.
Rule 5: If the serial number ends with a number, cut the 5th wire.

Keypad - First digit: The first digit that shows up in the serial number (if no numbers then it's 0).
Second digit: The wire number you cut (If you didn't do that module yet put 0).
Third digit: The number of modules you've already completed.
Fourth digit: The length of the serial number.

Morse - A word is randomly chosen from a preset list and you must decode it:
A: .-    B: -...    C: -.-.    D: -..    E: .    F: ..-.
G: --.   H: ....    I: ..      J: .---   K: -.-  L: .-..
M: --    N: -.      O: ---     P: .--.   Q: --.- R: .-.
S: ...   T: -       U: ..-     V: ...-   W: .--  X: -..-
Y: -.--  Z: --..

Password - A password is randomly chosen from ["PASSWORD", "EXPLOSIVE", "RANGER", "FIGHTER", "TRIGGER", "CIRCUIT", "TIMER", "COMPUTER", "PYTHON"]
and a key is randomly chosen from ["MODULE", "MORSE", "VIGENERE", "SERIAL", "NUMBER", "KEYPAD", "WIRES", "CIPHER"].
The password is then encrypted using a Vigenère cipher, and the player must correctly decrypt it.
""")
        
        else:
            print("Invalid choice.")
    play_again = input("\nPlay again? (Yes/No)").lower()
    if play_again != "yes": 
        print("Thanks for playing!")
        break
