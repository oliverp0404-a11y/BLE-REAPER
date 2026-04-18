import asyncio
import sys
import os
import shlex

from content.functions import error_sound, help_message, Intro, execute_command, startup_anim
from content.variables import TITLE, YELLOW, RED, BOLD, RESET

async def main():
    global found_devices
    if sys.platform == "win32":
        os.system(f'title {TITLE}')
        os.system('color')
    found_devices = []

    if len(sys.argv) > 2 and sys.argv[1] == "--exec":
        cmd_line = sys.argv[2]
        tokens = shlex.split(cmd_line)
        print(f"{RED}New window execution not fully supported for commands that need device list.{RESET}")
        print(f"{YELLOW}Please run 'sc' first in the main window before using /w.{RESET}")
        input("Press Enter to close...")
        return

    while True:
        startup_anim()
        Intro()
        help_message()
        user_input = input(f"{BOLD}BT_CMD {YELLOW}>>> {RESET}").strip()
        if not user_input:
            continue
        
        commands = user_input.split("&&")
        continue_flag = True
        for cmd_str in commands:
            cmd_str = cmd_str.strip()
            if not cmd_str:
                continue
            try:
                tokens = shlex.split(cmd_str)
            except:
                tokens = cmd_str.split()
            continue_flag = await execute_command(tokens, found_devices, new_window=False)
            if not continue_flag:
                break
        if not continue_flag:
            break

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{YELLOW}[EXIT]: Interrupted by user.{RESET}")
    except Exception as e:
        print(f"\n{RED}[ ⚠︎  CRITICAL ERROR  ⚠︎ ]: {e}{RESET}")
        print(f"{YELLOW}The script crashed. Read the error above!{RESET}")
        error_sound()
        input("Press Enter to close this window...")