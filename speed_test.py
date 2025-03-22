import time
import random
import sys
from colorama import init, Fore, Back, Style
import os
import msvcrt

init(autoreset=True)

TIME_OPTIONS = {
    "1": 15,
    "2": 30,
    "3": 60,
    "4": 120
}

texts = [
    "the quick brown fox jumps over the lazy dog",
    "programming is the art of telling a computer what to do",
    "practice makes perfect when it comes to typing",
    "speed and accuracy are both important in typing",
    "learning to type faster can save you lots of time"
]

def clear_screen():
    print("\033[H\033[J", end="")

THEMES = {
    "matrix": {
        "correct": Fore.GREEN,
        "incorrect": Fore.RED,
        "cursor": Fore.CYAN,
        "remaining": Fore.WHITE
    }
}

def print_text_to_type(text, typed="", theme=None):
    theme = THEMES["matrix"]
    cursor_pos = len(typed)
    line = []
    for i, char in enumerate(text):
        if i < len(typed):
            color = theme["correct"] if typed[i] == char else theme["incorrect"]
            line.append(color + char)
        elif i == cursor_pos:
            line.append(theme["cursor"] + char)
        else:
            line.append(theme["remaining"] + char)
    print("\r" + "".join(line) + Style.RESET_ALL, end="", flush=True)

def load_words():
    with open("C:\\Users\\ham7a\\Desktop\\test\\1000en", 'r') as file:
        return [line.strip().lower() for line in file]

def get_random_text():
    words = load_words()
    selected_words = [random.choice(words) for _ in range(random.randint(6, 8))]
    return ' '.join(selected_words)

def calculate_wpm(time_taken, text_length):
    words = text_length / 5
    minutes = time_taken / 60
    return round(words / minutes)

def calculate_cpm(time_taken, char_count):
    minutes = time_taken / 60
    return round(char_count / minutes)

def main():
    clear_screen()
    print(Fore.CYAN + "\nSpeed Typing Test" + Style.RESET_ALL)
    print(Fore.YELLOW + "Press 'tab' to restart\n" + Style.RESET_ALL)
    
    text = get_random_text()
    typed = ""
    start_time = None
    
    print_text_to_type(text, typed)
    
    while True:
        if msvcrt.kbhit():
            try:
                char = msvcrt.getch().decode('utf-8', 'ignore')
                if char == '\x08':
                    if len(typed) > 0:
                        typed = typed[:-1]
                        print_text_to_type(text, typed)
                elif ord(char) == 27:
                    sys.exit()
                elif ord(char) == 9:
                    return True
                elif char.isprintable():
                    typed += char
                    print_text_to_type(text, typed)
                    
                    if len(typed) == len(text):
                        end_time = time.time()
                        time_taken = end_time - start_time
                        accuracy = sum(1 for i, j in zip(text, typed) if i == j) / len(text) * 100
                        wpm = calculate_wpm(time_taken, len(typed))
                        cpm = calculate_cpm(time_taken, len(typed))
                        
                        print(f"\n\n{Fore.CYAN}Results:{Style.RESET_ALL}")
                        print(f"{Fore.WHITE}WPM (Words Per Minute): {Fore.GREEN}{wpm}")
                        print(f"{Fore.WHITE}CPM (Characters Per Minute): {Fore.GREEN}{cpm}")
                        print(f"{Fore.WHITE}Accuracy: {Fore.GREEN}{accuracy:.1f}%")
                        print(f"{Fore.WHITE}Time: {Fore.GREEN}{time_taken:.1f}s")
                        input("\nPress Enter to continue...")
                        return True
            except Exception as e:
                pass

        if not start_time and typed:
            start_time = time.time()

if __name__ == "__main__":
    try:
        restart = True
        while restart:
            restart = main()
    except KeyboardInterrupt:
        sys.exit()
