#PyNote Version 1.0.0.0.
#Create by BurzooTV in November 2020.
#Simple Terminal Editor For Python3.
#Github repo: https://github.com/BurzooTV/PyNote


import os
import sys
from pygments.lexers.python import Python3Lexer
from pygments.token import Token
from prompt_toolkit import PromptSession
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.bindings.basic import load_basic_bindings
from prompt_toolkit.styles import Style
from prompt_toolkit.styles import style_from_pygments_dict
from prompt_toolkit.shortcuts import input_dialog
from prompt_toolkit.shortcuts import yes_no_dialog
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import InMemoryHistory
from pynput.keyboard import Key, Controller
from rich.console import Console


#globals->
screen = Console()
keyboard = Controller()
bindings = load_basic_bindings()


#styles->
dialog_style = Style.from_dict({
    'dialog': 'bg:#000000',
    'dialog frame.label': 'bg:#000000 #f2f542',
    'dialog.body': 'bg:#000000 #f2f542',
    'dialog text-area': '#000000',
    'dialog shadow': 'bg:#f2f542',})


custom_lexer_style = style_from_pygments_dict({
    Token.Comment: '#949487 bold',
    Token.Keyword:   '#f2f542',
    Token.String: '#8c2807',
    Token.Operator: '#246BCE',
    Token.Operator.Word: '#246BCE',
    Token.Name.Function: '#246BCE italic',
    Token.Name.Builtin: '#246BCE'})


#key bindings->
@bindings.add('c-r')
def _(event) -> None: event.app.exit(result=event.app.current_buffer.text)


@bindings.add('c-o')
def _(event) -> str: event.current_buffer.insert_text(xpycode.strip())


@bindings.add('c-l') 
def _(event) -> str: event.current_buffer.insert_text(read_codes)


@bindings.add('c-k') 
def _(event) -> str: event.current_buffer.insert_text(return_code)


#control line number->
def _prompt_continuation(width, line_number, is_soft_wrap):
    line_number += 1
    if line_number <= 9:
        return ' ' + str(line_number) + '   '
    return str(line_number) + '   '


#start Point->
def startPoint() -> str:
    if len(sys.argv) < 2:
        screen.print("PyNote Error: Choose file's directory for second argument!", style='red')

    elif len(sys.argv) == 2:
        path_list = sys.argv[1].split('/')
        get_dir = ''.join(['/'.join(directory for directory in path_list[0:-1])])

        if os.path.exists(get_dir):
        
            if not os.path.isdir(sys.argv[1]):

                if sys.argv[1][-3:] == '.py':

                    if not os.path.exists(f'{get_dir}/{path_list[-1]}'):
                        return sys.argv[1]

                    else:
                        return (sys.argv[1], 'exists')
                else:
                    screen.print("PyNote Error: Only Python's file is valid!", style='red')
            else:
                screen.print("PyNote Error: You cant pick a directory!", style='red')
        else:
            screen.print("PyNote Error: Path does not exists!", style='red')

    else:
        screen.print("PyNote Error: Too many arguments!", style='red')


#main func->
def main() -> None:
    files_directory = startPoint()

    if files_directory:
        if type(files_directory) is tuple:

            files_directory = files_directory[0]

            with open(files_directory, 'r') as open_script:
                global read_codes
                read_codes = open_script.read()

            keyboard.press(Key.ctrl.value)
            keyboard.press('l')


        global session
        session = PromptSession()

        python_codes = list()

        os.system('clear')
        
        #editor loop->
        while True:
            text = session.prompt(' 1   ', auto_suggest=AutoSuggestFromHistory(),
                                        prompt_continuation=_prompt_continuation,
                                        lexer=PygmentsLexer(Python3Lexer),
                                        bottom_toolbar='Ready To Code...',
                                        enable_history_search=True,
                                        key_bindings=bindings,
                                        mouse_support=True,
                                        multiline=True,
                                        vi_mode=True,
                                        style=custom_lexer_style)

            python_codes.append(text)

            command_dialog = input_dialog(title='Command Window',
                                            text='Enter Commands:',
                                            style=dialog_style).run()

            if command_dialog is None: command_dialog = 'catch_me'

            if command_dialog == 'save':
                if len(python_codes) > 0:
                    with open(files_directory, 'w+') as save_soruce_code:
                        for codes in python_codes:
                            save_soruce_code.write('\n' + codes)

                    with open(files_directory, 'r') as open_source_code:
                        global xpycode
                        xpycode = open_source_code.read()

                    python_codes = list()
                    os.system('clear')

                    keyboard.press(Key.ctrl.value)
                    keyboard.press('o')

            elif command_dialog == 'exit':
                if len(python_codes) > 0:
                    ask_to_save = yes_no_dialog(
                                    title='Exit From PyNote',
                                    text='Do you want to save file?',
                                    style=dialog_style).run()

                    if ask_to_save:
                        with open(files_directory, 'w+') as save_soruce_code:
                            for codes in python_codes:
                                save_soruce_code.write('\n' + codes)

                        python_codes = list()
                        os.system('clear')
                        break

                    else:
                        python_codes = list()
                        os.system('clear')
                        break
                else:
                    python_codes = list()
                    os.system('clear')
                    break

            elif command_dialog == 'sexit':
                if len(python_codes) > 0:
                    with open(files_directory, 'w+') as save_soruce_code:
                        for codes in python_codes:
                            save_soruce_code.write('\n' + codes)

                    python_codes = list()
                    os.system('clear')
                    break

            else:
                global return_code
                return_code = str()
                for code in python_codes:
                    return_code += code

                python_codes = list()
                os.system('clear')

                keyboard.press(Key.ctrl.value)
                keyboard.press('k')
    else:
        pass     


if __name__ == "__main__":
    main()