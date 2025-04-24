import os
import json
import tkinter
import customtkinter
from datetime import datetime
import importlib.util
import sys

# Переклади для української та англійської мов  
TRANSLATIONS = {
    'uk': {
        'welcome': 'Ласкаво просимо!',
        'enter_help': 'Введіть help для додаткової інформації',
        'goodbye': 'Дякуємо що використовуєте FastCalculator!',
        'save_success': 'Історію збережено у: {}',
        'save_error': 'Помилка: Вкажіть назву для збереження',
        'load_success': 'Завантажено історію з: {}',
        'load_error': 'Помилка: Файл не знайдено',
        'calc_error': 'Помилка: Неправильний вираз або команда',
        'available_commands': 'Доступні команди:',
        'available_operations': 'Доступні операції:',
        'example': 'Приклад: ',
        'language_changed': 'Мову змінено на українську',
        'help_show': 'показати це повідомлення',
        'help_clear': 'очистити екран',
        'help_exit': 'вийти з програми',
        'help_info': 'інформація про калькулятор',
        'help_save': 'зберегти історію',
        'help_load': 'завантажити історію',
        'help_lang': 'змінити мову',
        'help_rungui': 'запустити графічний інтерфейс',
        'op_add': 'Додавання',
        'op_sub': 'Віднімання',
        'op_mul': 'Множення',
        'op_div': 'Ділення',
        'op_brackets': 'Дужки',
        'help_recover': 'відновити FastCalculator',
        'recovered': 'Відновлено FastCalculator 0.1.3 ♻︎',
        'help_addons': 'показати список встановлених аддонів',
        'no_addons': 'Аддони не знайдено',
        'addons_list': 'Встановлені аддони:',
        'addon_info': '• {name} v{version} від {author}',
        'lang_error': 'Доступні мови: uk, en, pl',
    },
    'en': {
        'welcome': 'Welcome!',
        'enter_help': 'Type help for more information',
        'goodbye': 'Thank you for using FastCalculator!',
        'save_success': 'History saved to: {}',
        'save_error': 'Error: Please specify save name',
        'load_success': 'Loaded history from: {}',
        'load_error': 'Error: File not found',
        'calc_error': 'Error: Invalid expression or command',
        'available_commands': 'Available commands:',
        'available_operations': 'Available operations:',
        'example': 'Example: ',
        'language_changed': 'Language changed to English',
        'help_show': 'show this message',
        'help_clear': 'clear screen',
        'help_exit': 'exit program',
        'help_info': 'calculator information',
        'help_save': 'save history',
        'help_load': 'load history',
        'help_lang': 'change language',
        'help_rungui': 'run graphical interface',
        'op_add': 'Addition',
        'op_sub': 'Subtraction',
        'op_mul': 'Multiplication',
        'op_div': 'Division',
        'op_brackets': 'Brackets',
        'help_recover': 'recover FastCalculator',
        'recovered': 'Recovered FastCalculator 0.1.3 ♻︎',
        'help_addons': 'show installed addons list',
        'no_addons': 'No addons found',
        'addons_list': 'Installed addons:',
        'addon_info': '• {name} v{version} by {author}',
        'lang_error': 'Available languages: uk, en, pl',
    },
    'pl': {
        'welcome': 'Powitanie!',
        'enter_help': 'Wpisz help, aby uzyskać więcej informacji',
        'goodbye': 'Dziękujemy za skorzystanie FastCalculator!',
        'save_success': 'Historia zapisana w: {}',
        'save_error': 'Błąd: Proszę podać nazwę zapisu',
        'load_success': 'Załadowano historię z: {}',
        'load_error': 'Błąd: Nie znaleziono pliku',
        'calc_error': 'Błąd: Nieprawidłowe wyrażenie lub polecenie',
        'available_commands': 'Dostępne polecenia:',
        'available_operations': 'Dostępne operacje:',
        'example': 'Przykład: ',
        'language_changed': 'Język zmieniony na polski',
        'help_show': 'pokaż tę wiadomość',
        'help_clear': 'wyczyść ekran',
        'help_exit': 'zakończ program',
        'help_info': 'informacje o kalkulatorze',
        'help_save': 'zapisz historię',
        'help_load': 'wczytaj historię',
        'help_lang': 'zmień język',
        'help_rungui': 'uruchom interfejs graficzny',
        'op_add': 'Dodawanie',
        'op_sub': 'Odejmowanie',
        'op_mul': 'Mnożenie',
        'op_div': 'Dzielenie',
        'op_brackets': 'Nawiasy',
        'help_recover': 'przywróć FastCalculator',
        'recovered': 'Przywrócono FastCalculator 0.1.3 ♻︎',
        'help_addons': 'pokaż listę zainstalowanych dodatków',
        'no_addons': 'Nie znaleziono dodatków',
        'addons_list': 'Zainstalowane dodatki:',
        'addon_info': '• {name} v{version} od {author}',
        'lang_error': 'Dostępne języki: uk, en, pl',
    }
}

# Доступні кольори для виводу в терміналі
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Функції для очищення екрану та зміни мови
def clear_screen():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

def change_language(lang_code):
    if lang_code not in TRANSLATIONS:
        return False
    return lang_code

# Початковий екран, банер
def print_banner(lang='uk'):
    banner = f"""
{bcolors.HEADER}╔══════════════════════════════════╗
║     FastCalculator v0.1.3        ║
║     Welcome ☺︎                    ║
╚══════════════════════════════════╝{bcolors.ENDC}"""
    print(banner)

def get_save_directory():
    base_dir = os.path.join(os.path.expanduser("~"), "OneDrive", "Документи", "FastCalculator", "saves")
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    return base_dir

# Функція збереження та завантаження історії 
def save_history(history, save_name):
    save_dir = get_save_directory()
    file_path = os.path.join(save_dir, f"{save_name}.json")
    
    save_data = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "history": history
    }
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(save_data, f, ensure_ascii=False, indent=2)
    
    return file_path

def load_history(save_name):
    save_dir = get_save_directory()
    file_path = os.path.join(save_dir, f"{save_name}.json")
    
    if not os.path.exists(file_path):
        return None
        
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

# Вивід команди help (Додаткова інформація)
def print_help(lang='uk'):
    help_text = f"""
{bcolors.WARNING}{TRANSLATIONS[lang]['available_commands']}
• help  - {TRANSLATIONS[lang]['help_show']}
• clear - {TRANSLATIONS[lang]['help_clear']}
• exit  - {TRANSLATIONS[lang]['help_exit']}
• info  - {TRANSLATIONS[lang]['help_info']}
• save name - {TRANSLATIONS[lang]['help_save']}
• load name - {TRANSLATIONS[lang]['help_load']}
• lang uk/en/pl - {TRANSLATIONS[lang]['help_lang']}
• rungui - {TRANSLATIONS[lang]['help_rungui']}
• recover - {TRANSLATIONS[lang]['help_recover']}
• addons - {TRANSLATIONS[lang]['help_addons']}"""

    loaded_addons = load_addons()
    if loaded_addons:
        help_text += "\n\n" + bcolors.WARNING + TRANSLATIONS[lang]['addons_list']
        for addon in loaded_addons:
            for cmd, desc in addon['commands'].items():
                help_text += f"\n• {cmd} - {desc}"

    help_text += f"""

{TRANSLATIONS[lang]['available_operations']}
• {TRANSLATIONS[lang]['op_add']} (+)
• {TRANSLATIONS[lang]['op_sub']} (-)
• {TRANSLATIONS[lang]['op_mul']} (*)
• {TRANSLATIONS[lang]['op_div']} (/)
• {TRANSLATIONS[lang]['op_brackets']} ()

{TRANSLATIONS[lang]['example']}2 * (3 + 4){bcolors.ENDC}
"""
    print(help_text)

# Початок у графічному інтерфейсі
def create_gui():
    root = customtkinter.CTk()
    root.title("FastCalculator GUI")
    root.geometry("320x500")
    
    # Змінна для зберігання поточного виразу
    expression = tkinter.StringVar()
    expression.set("0")
    
    # Дисплей калькулятора
    display = customtkinter.CTkEntry(
        root,
        textvariable=expression,
        font=("Segoe UI", 24),
        justify="right",
        state="readonly"
    )
    display.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
    
    # Кнопки калькулятора
    buttons = [
        '7', '8', '9', '/',
        '4', '5', '6', '*',
        '1', '2', '3', '-',
        '0', '.', '=', '+',
        'C', '(', ')', 'Del'
    ]
    
    def button_click(symbol):
        current = expression.get()
        if current == "0":
            current = ""
            
        if symbol == "=":
            try:
                result = str(eval(current))
                expression.set(result)
            except:
                expression.set("Error")
        elif symbol == "C":
            expression.set("0")
        elif symbol == "Del":
            expression.set(current[:-1] if len(current) > 1 else "0")
        else:
            expression.set(current + symbol)
    
    # Створення сітки кнопок
    row = 1
    col = 0
    for button in buttons:
        cmd = lambda x=button: button_click(x)
        btn = customtkinter.CTkButton(
            root,
            text=button,
            width=70,
            height=70,
            font=("Segoe UI", 20),
            command=cmd
        )
        btn.grid(row=row, column=col, padx=2, pady=2)
        col += 1
        if col > 3:
            col = 0
            row += 1
    
    for i in range(4):
        root.grid_columnconfigure(i, weight=1)
    for i in range(6):
        root.grid_rowconfigure(i, weight=1)
    
    root.mainloop()

# Завантаження аддонів
def load_addons():
    addons_dir = os.path.join(os.path.expanduser("~"), "OneDrive", "Документи", "FastCalculator", "addons")
    if not os.path.exists(addons_dir):
        os.makedirs(addons_dir)
        
    loaded_addons = []
    
    for file in os.listdir(addons_dir):
        if file.endswith('.py'):
            try:
                spec = importlib.util.spec_from_file_location(
                    file[:-3],
                    os.path.join(addons_dir, file)
                )
                module = importlib.util.module_from_spec(spec)
                sys.modules[file[:-3]] = module
                spec.loader.exec_module(module)
                
                # Перевірка наявності необхідних атрибутів для аддона
                if hasattr(module, 'addon_info'):
                    loaded_addons.append({
                        'name': module.addon_info.get('name', 'Unknown'),
                        'version': module.addon_info.get('version', '0.0'),
                        'author': module.addon_info.get('author', 'Unknown'),
                        'commands': module.addon_info.get('commands', {}),
                        'module': module
                    })
            except Exception as e:
                print(f"{bcolors.FAIL}Помилка завантаження аддону {file}: {str(e)}{bcolors.ENDC}")
    
    return loaded_addons

def main():
    clear_screen()
    current_lang = 'uk'
    print_banner(current_lang)
    print(f"{bcolors.OKGREEN}{TRANSLATIONS[current_lang]['enter_help']}{bcolors.ENDC}")
    
    history = []
    loaded_addons = load_addons()
    commands = {'help', 'clear', 'exit', 'info', 'save', 'load', 'lang', 'rungui', 'recover', 'addons', 'discord'} # Доступні, основні команди
    
    # Додавання команд з аддонів
    addon_commands = {}
    for addon in loaded_addons:
        addon_commands.update(addon['commands'])
        commands.update(addon['commands'].keys())

    # Логіка та команди
    while True:
        try:
            user_input = input(f"{bcolors.OKCYAN}▸ {bcolors.ENDC}").strip()
            command = user_input.split()[0].lower() if user_input else ''

            if command in commands:
                if command == 'exit':
                    print(f"{bcolors.WARNING}{TRANSLATIONS[current_lang]['goodbye']}{bcolors.ENDC}")
                    break
                elif command == 'clear':
                    clear_screen()
                    print_banner(current_lang)
                elif command == 'help':
                    print_help(current_lang)
                elif command == 'info':
                    print(f"{bcolors.WARNING}FastCalculator v0.1.3 by Coconut153{bcolors.ENDC}")
                elif command == 'discord':
                    print(f"{bcolors.OKBLUE}Our Discord server: https://discord.gg/qwSH6K7ShG{bcolors.ENDC}")
                elif command == 'save':
                    parts = user_input.split(maxsplit=1)
                    if len(parts) > 1:
                        save_name = parts[1].strip()
                        file_path = save_history(history, save_name)
                        print(f"{bcolors.OKGREEN}{TRANSLATIONS[current_lang]['save_success'].format(file_path)}{bcolors.ENDC}")
                    else:
                        print(f"{bcolors.FAIL}{TRANSLATIONS[current_lang]['save_error']}{bcolors.ENDC}")
                elif command == 'load':
                    parts = user_input.split(maxsplit=1)
                    if len(parts) > 1:
                        save_name = parts[1].strip()
                        loaded_data = load_history(save_name)
                        if loaded_data:
                            print(f"{bcolors.OKGREEN}{TRANSLATIONS[current_lang]['load_success'].format(loaded_data['date'])}{bcolors.ENDC}")
                            for item in loaded_data['history']:
                                print(f"{bcolors.OKCYAN}▸ {bcolors.ENDC}{item['expression']}")
                                print(f"{bcolors.OKGREEN}= {bcolors.ENDC}{item['result']}")
                        else:
                            print(f"{bcolors.FAIL}{TRANSLATIONS[current_lang]['load_error']}{bcolors.ENDC}")
                elif command == 'lang':
                    parts = user_input.split(maxsplit=1)
                    if len(parts) > 1:
                        new_lang = parts[1].strip()
                        if new_lang in ['uk', 'en', 'pl']:
                            current_lang = change_language(new_lang)
                            print(f"{bcolors.OKGREEN}{TRANSLATIONS[current_lang]['language_changed']}{bcolors.ENDC}")
                            clear_screen()
                            print_banner(current_lang)
                        else:
                            # Додамо нові ключі перекладу для помилки мови
                            print(f"{bcolors.FAIL}{TRANSLATIONS[current_lang].get('lang_error', 'Available languages: uk, en, pl')}{bcolors.ENDC}")
                elif command == 'rungui':
                    create_gui()
                elif command == 'recover':
                    print(f"{bcolors.OKGREEN}{TRANSLATIONS[current_lang]['recovered']}{bcolors.ENDC}")
                elif command == 'addons':
                    if loaded_addons:
                        print(f"{bcolors.WARNING}{TRANSLATIONS[current_lang]['addons_list']}{bcolors.ENDC}")
                        for addon in loaded_addons:
                            print(f"{bcolors.OKGREEN}{TRANSLATIONS[current_lang]['addon_info'].format(**addon)}{bcolors.ENDC}")
                    else:
                        print(f"{bcolors.WARNING}{TRANSLATIONS[current_lang]['no_addons']}{bcolors.ENDC}")
                elif command in addon_commands:
                    # Команда з аддона
                    try:
                        addon_commands[command](user_input)
                    except Exception as e:
                        print(f"{bcolors.FAIL}{str(e)}{bcolors.ENDC}")
            elif user_input.strip():
                result = eval(user_input)
                history.append({"expression": user_input, "result": result})
                print(f"{bcolors.OKGREEN}={bcolors.ENDC} {result}")
        except Exception as e:
            print(f"{bcolors.FAIL}{TRANSLATIONS[current_lang]['calc_error']}{bcolors.ENDC}")

# Головна функція
if __name__ == "__main__":
    main()