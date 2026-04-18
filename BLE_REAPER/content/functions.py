from bleak import BleakScanner, BleakClient
import asyncio
import winreg
import pygame
import ctypes
import sys
import os
import winsound
import subprocess
import random
import time
from content.variables import GREEN, YELLOW, CYAN, RED, MAGENTA, BOLD, RESET, TITLE, big_banner
from content.paths import LOCATION, WARN_SPEECH, ERROR, SYNTAX_ERROR, CRITICAL_ERROR, T1, T2, T3, T4, T5, T6, T7, T8, T9, T10

from config import TTS, SOUND, CAN_SAVE, COLORS, EFFECTS, ANIMS

intro = True
Help = True
startup_animation = True
found_devices = []
there_is_updates = False

def CHECK_UPDATES():
    pass

def error_sound(level=None):
    if SOUND == True:
        winsound.Beep(200, 100)
    if TTS == True:
        if level == "1":
            winsound.PlaySound(ERROR, winsound.SND_FILENAME)
        elif level == "2":
            winsound.PlaySound(SYNTAX_ERROR, winsound.SND_FILENAME)
        elif level == "3":
            winsound.PlaySound(CRITICAL_ERROR, winsound.SND_FILENAME)
        else:
            winsound.PlaySound(ERROR, winsound.SND_FILENAME)
        
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
    found_devices.clear()

async def connect_and_play(device):
    print(f"{CYAN}[CONNECTING]: Opening Windows Bluetooth pairing for {device.address}...{RESET}")
    try:
        async with BleakClient(device.address) as client:
            await client.connect()
            if client.is_connected:
                print(f"{GREEN}[SUCCESS]: BLE connection established!{RESET}")
                print(f"{YELLOW}[INFO]: To pair this device with Windows, you must do it manually.{RESET}")
                print(f"{CYAN}[ACTION]: Opening Bluetooth settings...{RESET}")
                os.system("start ms-settings:bluetooth")
                input(f"{YELLOW}Press Enter after you've paired the device in Windows...{RESET}")
                troll_sounds = [T1, T2, T3, T4, T5, T6, T7, T8, T9, T10]
                available_sounds = [s for s in troll_sounds if os.path.exists(s)]
                if available_sounds:
                    print(f"{MAGENTA}[PLAYING]: Initializing Audio Sequence...{RESET}")
                    pygame.mixer.init()
                    print(f"{MAGENTA}[PLAY]: Playing {len(available_sounds)} sounds. Press Ctrl+C to stop.{RESET}")
                    try:
                        for i, sound in enumerate(available_sounds):
                            print(f"{CYAN}[SOUND {i+1}/{len(available_sounds)}]: {os.path.basename(sound)}{RESET}")
                            pygame.mixer.music.load(sound)
                            pygame.mixer.music.play()
                            while pygame.mixer.music.get_busy():
                                await asyncio.sleep(0.5)
                        print(f"{GREEN}[DONE]: Audio sequence completed!{RESET}")
                    except KeyboardInterrupt:
                        print(f"\n{YELLOW}[INTERRUPTED]: Playback stopped by user.{RESET}")
                        pygame.mixer.music.stop()
                else:
                    print(f"{RED}[WARN]: No troll sounds found!{RESET}")
                    error_sound(2)
            else:
                print(f"{RED}[ERROR]: Failed to establish BLE connection.{RESET}")
                error_sound(1)
    except KeyboardInterrupt:
        print(f"\n{YELLOW}[ABORTED]: Connection attempt interrupted.{RESET}")
    except Exception as e:
        print(f"{RED}[ERROR]: Connection failed - {e}{RESET}")
        error_sound(1)
    finally:
        try:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
        except:
            pass
        print(f"{YELLOW}[DISCONNECTED]: BLE session with {device.address} closed.{RESET}")

async def connect_and_troll(device, mode=None):
    print(f"{CYAN}[CONNECTING]: Bridging to {device.address}...{RESET}")
    
    # Define available_sounds in outer scope so 'next' command can access it
    available_sounds = []
    
    try:
        async with BleakClient(device.address) as client:
            if client.is_connected:
                print(f"{GREEN}[SUCCESS]: Target {device.address} has been connected!{RESET}")
                
                if mode == "glitch":
                    if os.path.exists(LOCATION):
                        print(f"{MAGENTA}[PLAYING]: Initializing Glitch Protocol...{RESET}")
                        pygame.mixer.init()
                        pygame.mixer.music.load(LOCATION)
                        pygame.mixer.music.play()
                    else:
                        print(f"{RED}[WARN]: .mp3 not found!{RESET}")
                        error_sound(2)
                        
                elif mode == "troll":
                    # Collect all available troll sounds
                    troll_sounds = [T1, T2, T3, T4, T5, T6, T7, T8, T9, T10]
                    available_sounds = [s for s in troll_sounds if os.path.exists(s)]
                    
                    if available_sounds:
                        print(f"{MAGENTA}[PLAYING]: Initializing Troll Protocol...{RESET}")
                        pygame.mixer.init()
                        
                        # Load the FIRST sound
                        pygame.mixer.music.load(available_sounds[0])
                        
                        # Queue the REST
                        for sound in available_sounds[1:]:
                            pygame.mixer.music.queue(sound)
                        
                        pygame.mixer.music.play()
                        print(f"{MAGENTA}[TROLL]: Queued {len(available_sounds)} sounds{RESET}")
                    else:
                        print(f"{RED}[WARN]: No troll sounds found!{RESET}")
                        error_sound(2)
                        
                elif mode == "glitchtroll":
                    if os.path.exists(LOCATION):
                        troll_sounds = [T1, T2, T3, T4, T5, T6, T7, T8, T9, T10]
                        available_sounds = [s for s in troll_sounds if os.path.exists(s)]
                        
                        pygame.mixer.init()
                        
                        # Load glitch sound first
                        pygame.mixer.music.load(LOCATION)
                        
                        # Queue all troll sounds AFTER
                        for sound in available_sounds:
                            pygame.mixer.music.queue(sound)
                        
                        pygame.mixer.music.play()
                        print(f"{MAGENTA}[GLITCHTROLL]: Maximum chaos engaged! ({1 + len(available_sounds)} sounds queued){RESET}")
                    else:
                        print(f"{RED}[WARN]: Glitch sound missing!{RESET}")
                        error_sound(2)
                
                # Interactive session loop
                while client.is_connected:
                    sub = input(f"{BOLD}CNCT ({device.address}) > {RESET}").strip().lower()
                    
                    if sub == "back":
                        pygame.mixer.music.stop()
                        break
                        
                    elif sub == "pause":
                        pygame.mixer.music.pause()
                        print(f"{YELLOW}[PAUSED]: Music paused{RESET}")
                        
                    elif sub == "resume":
                        pygame.mixer.music.unpause()
                        print(f"{GREEN}[RESUMED]: Music resumed{RESET}")
                        
                    elif sub == "stop":
                        pygame.mixer.music.stop()
                        print(f"{YELLOW}[STOPPED]: Playback stopped{RESET}")
                        
                    elif sub == "next":
                        if mode in ["troll", "glitchtroll"] and available_sounds:
                            chosen = random.choice(available_sounds)
                            pygame.mixer.music.load(chosen)
                            pygame.mixer.music.play()
                            print(f"{MAGENTA}[NEXT]: Now playing {os.path.basename(chosen)}{RESET}")
                        elif mode == "glitch":
                            if os.path.exists(LOCATION):
                                pygame.mixer.music.load(LOCATION)
                                pygame.mixer.music.play()
                                print(f"{MAGENTA}[NEXT]: Replaying glitch sound{RESET}")
                            else:
                                print(f"{RED}[ERROR]: No sounds available{RESET}")
                        else:
                            print(f"{RED}[ERROR]: No sounds available for 'next' command{RESET}")
                            
                    elif sub.startswith("vol "):
                        try:
                            vol = float(sub.split()[1])
                            vol = max(0.0, min(1.0, vol))
                            pygame.mixer.music.set_volume(vol)
                            print(f"{CYAN}[VOLUME]: Set to {int(vol*100)}%{RESET}")
                        except (ValueError, IndexError):
                            print(f"{RED}[ERROR]: Usage: vol 0.0-1.0 (e.g., vol 0.5){RESET}")
                            
                    elif sub == "status":
                        if pygame.mixer.music.get_busy():
                            print(f"{GREEN}[STATUS]: Playing{RESET}")
                        else:
                            print(f"{YELLOW}[STATUS]: Stopped/Paused{RESET}")
                            
                    elif sub == "help":
                        print(f"{CYAN}=== CNCT SESSION COMMANDS ==={RESET}")
                        print(f"  {GREEN}back{RESET}   - Disconnect and return to main menu")
                        print(f"  {GREEN}pause{RESET}  - Pause current playback")
                        print(f"  {GREEN}resume{RESET} - Resume paused playback")
                        print(f"  {GREEN}stop{RESET}   - Stop playback completely")
                        print(f"  {GREEN}next{RESET}   - Skip to next random sound")
                        print(f"  {GREEN}vol{RESET}    - Set volume (0.0 - 1.0)")
                        print(f"  {GREEN}status{RESET} - Show playback status")
                        print(f"  {GREEN}help{RESET}   - Show this message")
                        
                    elif sub == "":
                        # Empty input, just continue
                        pass
                        
                    else:
                        print(f"{RED}[ERROR]: Unknown command '{sub}'. Type 'help' for options.{RESET}")
                    
                    await asyncio.sleep(0.1)
                    
    except Exception as e:
        print(f"{RED}[ERROR]: Connection failed - {e}{RESET}")
        error_sound(1)
        
    finally:
        # Clean up pygame mixer when done
        try:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
        except:
            pass
        print(f"{YELLOW}[DISCONNECTED]: Session with {device.address} closed.{RESET}")

async def shadow_mitm(device):
    print(f"{YELLOW}[SHADOW]: Attempting to intercept data from {device.address}...{RESET}")
    print(f"{CYAN}Searching for readable/notifiable characteristics...{RESET}")

    def notification_handler(sender, data):
        hex_data = data.hex(' ')
        try:
            text_data = data.decode('utf-8', errors='ignore')
        except:
            text_data = "Binary Data"
        print(f"{GREEN}[INTERCEPTED]: {RESET}{hex_data} | {YELLOW}(Text: {text_data}){RESET}")

    try:
        async with BleakClient(device.address) as client:
            print(f"{GREEN}[SUCCESS]: Tunnel established. Monitoring stream...{RESET}")
            started = []
            for service in client.services:
                for char in service.characteristics:
                    if "notify" in char.properties or "indicate" in char.properties:
                        print(f"{CYAN}[LISTEN]: Hooking into {char.uuid[:8]}...{RESET}")
                        await client.start_notify(char.uuid, notification_handler)
                        started.append(char.uuid)
            print(f"{YELLOW}Shadowing active. Press Ctrl+C to bail.{RESET}")
            while True:
                await asyncio.sleep(1.0)
    except KeyboardInterrupt:
        print(f"\n{YELLOW}[STATUS]: Shadow stopped by user.{RESET}")
    except Exception as e:
        print(f"{RED} ⚠︎  Connection failed: {e}{RESET}")
        error_sound()

def spoof_name(new_name):
    if sys.platform != "win32":
        print(f"{RED}[ERROR]: Name spoofing is only supported on Windows.{RESET}")
        error_sound()
        return
    print(f"{YELLOW}[SPOOF]: Changing Bluetooth adapter name to: {new_name}...{RESET}")
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print(f"{RED}[ERROR]: Administrator privileges required. Run as admin and try again.{RESET}")
        error_sound()
        return
    key_path = r"SYSTEM\CurrentControlSet\Services\BTHPORT\Parameters\Device"
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "FriendlyName", 0, winreg.REG_SZ, new_name)
        winreg.CloseKey(key)
        print(f"{GREEN}[SUCCESS]: Registry updated with new name: {new_name}{RESET}")
        print(f"{CYAN}[INFO]: Restarting Bluetooth service...{RESET}")
        os.system('net stop BthServ > nul 2>&1')
        os.system('net start BthServ > nul 2>&1')
        print(f"{GREEN}[SUCCESS]: Bluetooth adapter name changed to '{new_name}'.{RESET}")
        print(f"{YELLOW}[NOTE]: Some devices may need to rediscover you.{RESET}")
    except FileNotFoundError:
        print(f"{RED}[ERROR]: Bluetooth registry key not found. Is Bluetooth enabled?{RESET}")
        error_sound()
    except PermissionError:
        print(f"{RED}[ERROR]: Permission denied. Run as administrator.{RESET}")
        error_sound()
    except Exception as e:
        print(f"{RED}[ERROR]: Failed to change name: {e}{RESET}")
        error_sound()

def save_device(device):
    path = fr"C:\Users\olive\OneDrive\Desktop\Bluetooth Tools\saves\saved_devices.txt"
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "a") as f:
            f.write(f"NAME: {device.name or 'Unknown'} | MAC: {device.address}\n")
        print(f"{GREEN}[SUCCESS]: Device saved to {path}{RESET}")
    except Exception as e:
        print(f"{RED}[ERROR]: Could not save. {e}{RESET}")
        error_sound()

async def show_adapter():
    print(f"{CYAN}[ADAPTER]: Querying local Bluetooth hardware...{RESET}")
    try:
        ps = """
        $adapters = Get-PnpDevice -Class Bluetooth | Where-Object {$_.FriendlyName -like '*Bluetooth*'}
        foreach ($adapter in $adapters) {
            Write-Host "Name: $($adapter.FriendlyName)"
            Write-Host "Status: $($adapter.Status)"
        }
        """
        result = subprocess.run(["powershell", "-Command", ps], capture_output=True, text=True)
        if result.stdout.strip():
            print(result.stdout)
        else:
            print(f"{RED}[ERROR]: No Bluetooth adapter found.{RESET}")
            error_sound()
    except Exception as e:
        print(f"{RED}[ERROR]: {e}{RESET}")
        error_sound()

async def handshake_knock(device):
    print(f"{YELLOW}[KNOCK]: Handshaking with {device.address}...{RESET}")
    try:
        async with BleakClient(device.address) as client:
            print(f"{GREEN}[SUCCESS]: Handshake Accepted. MTU: {client.mtu_size}{RESET}")
    except Exception as e:
        print(f"{RED}[ERROR]: Knock Wasn't Accepted. {e}{RESET}")
        error_sound()

async def quick_services(device):
    print(f"{CYAN}[SERVICES]: Querying {device.address}...{RESET}")
    try:
        async with BleakClient(device.address) as client:
            for s in client.services:
                print(f"  {GREEN}[+]{RESET} {s.description} ({s.uuid})")
    except Exception as e:
        print(f"{RED}[ERROR]: {e}{RESET}")
        error_sound()

async def get_battery(device):
    print(f"{CYAN}[DETECTIVE]: Probing {device.address} for energy signatures...{RESET}")
    try:
        async with BleakClient(device.address) as client:
            BAS_UUID = "00002a19-0000-1000-8000-00805f9b34fb"
            hidden_battery_uuids = [
                "0000fe50-0000-1000-8000-00805f9b34fb",
                "00002a1b-0000-1000-8000-00805f9b34fb",
            ]
            for uuid in [BAS_UUID] + hidden_battery_uuids:
                try:
                    val = await client.read_gatt_char(uuid)
                    if val:
                        percentage = int(val[0])
                        print(f"{GREEN}[SUCCESS]: Found Level via {uuid[:8]}: {percentage}%{RESET}")
                        return percentage
                except:
                    continue
            print(f"{YELLOW}[SCANNING]: Looking for byte-patterns (0-100)...{RESET}")
            for service in client.services:
                for char in service.characteristics:
                    if "read" in char.properties:
                        try:
                            raw = await client.read_gatt_char(char.uuid)
                            if len(raw) == 1:
                                val = int(raw[0])
                                if 0 <= val <= 100:
                                    desc = char.description or "Unknown Handle"
                                    print(f"{MAGENTA}[MATCH]: {desc} ({char.uuid[:8]}) -> {val}%{RESET}")
                                    return val
                        except:
                            continue
            print(f"{CYAN}[DONE]: Probe finished – no battery level found.{RESET}")
            return None
    except Exception as e:
        print(f"{RED}hell naaaah bro! Connection lost: {e}{RESET}")
        error_sound()
        return None

async def rssi_ping(device, once=False):
    print(f"{CYAN}[PING]: Tracking {device.name or 'Unknown'} ({device.address}).{RESET}")
    os.system(f'title {TITLE} pinging')
    if once:
        print(f"{YELLOW}Pausing after first packet (pause mode).{RESET}")
    else:
        print(f"{YELLOW}Hold Ctrl+C to stop the ping. Sniffing Identity Packets... {RESET}")

    def detection_callback(detected_device, advertisement_data):
        if detected_device.address.lower() == device.address.lower():
            rssi = advertisement_data.rssi
            bar_length = max(0, 150 + rssi)
            raw_data = ""
            if advertisement_data.manufacturer_data:
                for company_id, content in advertisement_data.manufacturer_data.items():
                    raw_data += f" [ID:{company_id:04x} DATA:{content.hex().upper()}]"
            print(f"{GREEN}SIGNAL: {rssi:4} dBm {'|' * bar_length}{RESET}{raw_data}")
            if once:
                return True
        return False

    scanner = BleakScanner(detection_callback)
    try:
        await scanner.start()
        if once:
            while True:
                await asyncio.sleep(0.1)
                print(f"{YELLOW}Waiting 5 seconds for first packet...{RESET}")
                await asyncio.sleep(5)
                break
        else:
            while True:
                await asyncio.sleep(0.1)
    except KeyboardInterrupt:
        await scanner.stop()
        print(f"\n{YELLOW}[STATUS]: Ping stopped.{RESET}")
    except Exception as e:
        print(f"{RED}[ERROR]: Ping failed: {e}{RESET}")
        error_sound()
    finally:
        await scanner.stop()

async def live_traffic_logger(device):
    print(f"{CYAN}[LOGGER]: Bridging {device.address}...{RESET}")
    try:
        async with BleakClient(device.address) as client:
            print(f"{GREEN}[SUCCESS]: Sniffing Active. Waiting for commands...{RESET}")
            def callback(handle, data):
                print(f"{YELLOW}[HEX SNIFFED]: Handle({handle}) -> {data.hex().upper()}{RESET}")
            started = []
            for service in client.services:
                for char in service.characteristics:
                    if "notify" in char.properties:
                        try:
                            await client.start_notify(char.uuid, callback)
                            started.append(char.uuid)
                        except:
                            pass
            print(f"{YELLOW}Logging active. Press Ctrl+C to stop.{RESET}")
            while True:
                await asyncio.sleep(1)
    except KeyboardInterrupt:
        print(f"\n{YELLOW}[STATUS]: Logger stopped by user.{RESET}")
    except Exception as e:
        print(f"{RED}[ERROR]: {e}{RESET}")
        error_sound()

async def persistent_session(device):
    try:
        async with BleakClient(device.address) as client:
            print(f"{GREEN}[SUCCESS]: TUNNEL ACTIVE!{RESET}")
            while client.is_connected:
                sub = input(f"{BOLD}SESSION ({device.address}) > {RESET}").strip().lower()
                if sub == "services":
                    for s in client.services:
                        print(f"  -> {s.uuid} ({s.description})")
                elif sub == "back":
                    break
    except Exception as e:
        print(f"{RED}[ERROR]: {e}{RESET}")
        error_sound()

async def function_scan(device):
    print(f"{CYAN}[DEEP SCAN]: Pulling functions...{RESET}")
    try:
        async with BleakClient(device.address) as client:
            for service in client.services:
                print(f"\n{BOLD}Service: {service.description}{RESET}")
                for char in service.characteristics:
                    props = ",".join(char.properties)
                    p_color = GREEN if "write" in props else YELLOW
                    print(f"  [FUNC] {char.uuid[:8]} | PERMS: {p_color}{props}{RESET}")
    except Exception as e:
        print(f"{RED}[ERROR]: {e}{RESET}")
        error_sound()

def print_random_binary():
    print(f"{YELLOW}[SYSTEM]: Initializing T-HACKER terminal...{RESET}")
    for _ in range(24):
        line1 = "".join("1" if i % 2 == 0 else "0" for i in range(64))
        line2 = "".join("#" if e % 2 == 0 else "@" for e in range(64))
        print(f"         {BOLD}{GREEN} {line1} {RESET}")
        print(f"         {BOLD}{GREEN} {line2} {RESET}")
        time.sleep(0.01)

def startup_anim():
    global startup_animation
    if startup_animation == True:
        clear()
        print(f"{YELLOW}[SYSTEM]: checking for updates.{RESET}")
        if there_is_updates == True:
            print(f"{YELLOW}[SYSTEM]: downloading updates.{RESET}")
        time.sleep(0.2)
        clear()
        print(f"{YELLOW}[SYSTEM]: checking for updates [DONE]{RESET}")
        time.sleep(0.2)
        clear()
        print(f"{YELLOW}[SYSTEM]: checking for updates [DONE]{RESET}")
        print(f"{YELLOW}[SYSTEM]: getting content files.{RESET}")
        time.sleep(0.2)
        clear()
        print(f"{YELLOW}[SYSTEM]: checking for updates [DONE]{RESET}")
        print(f"{YELLOW}[SYSTEM]: getting content files..{RESET}")
        time.sleep(0.2)
        clear()
        print(f"{YELLOW}[SYSTEM]: checking for updates [DONE]{RESET}")
        print(f"{YELLOW}[SYSTEM]: getting content files...{RESET}")
        time.sleep(0.2)
        clear()
        print(f"{YELLOW}[SYSTEM]: checking for updates [DONE]{RESET}")
        print(f"{YELLOW}[SYSTEM]: getting content files.{RESET}")
        time.sleep(0.2)
        clear()
        print(f"{YELLOW}[SYSTEM]: checking for updates [DONE]{RESET}")
        print(f"{YELLOW}[SYSTEM]: getting content files..{RESET}")
        time.sleep(0.2)
        clear()
        print(f"{YELLOW}[SYSTEM]: checking for updates [DONE]{RESET}")
        print(f"{YELLOW}[SYSTEM]: getting content files...{RESET}")
        time.sleep(0.2)
        clear()
        print(f"{YELLOW}[SYSTEM]: checking for updates [DONE]{RESET}")
        print(f"{YELLOW}[SYSTEM]: getting content files.{RESET}")
        time.sleep(0.2)
        clear()
        print(f"{YELLOW}[SYSTEM]: checking for updates [DONE]{RESET}")
        print(f"{YELLOW}[SYSTEM]: getting content files..{RESET}")
        time.sleep(0.2)
        clear()
        print(f"{YELLOW}[SYSTEM]: checking for updates [DONE]{RESET}")
        print(f"{YELLOW}[SYSTEM]: getting content files [DONE]{RESET}")
        time.sleep(0.2)
        clear()
        print(f"{YELLOW}[SYSTEM]: checking for updates [DONE]{RESET}")
        print(f"{YELLOW}[SYSTEM]: getting content files [DONE]{RESET}")
        print(f"{YELLOW}[SYSTEM]: getting Command files.{RESET}")
        time.sleep(0.2)
        clear()
        print(f"{YELLOW}[SYSTEM]: checking for updates [DONE]{RESET}")
        print(f"{YELLOW}[SYSTEM]: getting content files [DONE]{RESET}")
        print(f"{YELLOW}[SYSTEM]: getting Command files..{RESET}")
        time.sleep(0.2)
        clear()
        print(f"{YELLOW}[SYSTEM]: checking for updates [DONE]{RESET}")
        print(f"{YELLOW}[SYSTEM]: getting content files [DONE]{RESET}")
        print(f"{YELLOW}[SYSTEM]: getting Command files...{RESET}")
        time.sleep(1.3)
        clear()
        print(f"{YELLOW}[SYSTEM]: checking for updates [DONE]{RESET}")
        print(f"{YELLOW}[SYSTEM]: getting content files [DONE]{RESET}")
        print(f"{YELLOW}[SYSTEM]: getting Command files.{RESET}")
        time.sleep(0.2)
        clear()
        print(f"{YELLOW}[SYSTEM]: checking for updates [DONE]{RESET}")
        print(f"{YELLOW}[SYSTEM]: getting content files [DONE]{RESET}")
        print(f"{YELLOW}[SYSTEM]: getting Command files..{RESET}")
        time.sleep(0.2)
        clear()
        print(f"{YELLOW}[SYSTEM]: checking for updates [DONE]{RESET}")
        print(f"{YELLOW}[SYSTEM]: getting content files [DONE]{RESET}")
        print(f"{YELLOW}[SYSTEM]: getting Command files...{RESET}")
        time.sleep(0.4)
        clear()
        print(f"{YELLOW}[SYSTEM]: checking for updates [DONE]{RESET}")
        print(f"{YELLOW}[SYSTEM]: getting content files [DONE]{RESET}")
        print(f"{YELLOW}[SYSTEM]: getting Command files.{RESET}")
        time.sleep(0.2)
        clear()
        print(f"{YELLOW}[SYSTEM]: checking for updates [DONE]{RESET}")
        print(f"{YELLOW}[SYSTEM]: getting content files [DONE]{RESET}")
        print(f"{YELLOW}[SYSTEM]: getting Command files..{RESET}")
        time.sleep(1)
        clear()
        print(f"{YELLOW}[SYSTEM]: checking for updates [DONE]{RESET}")
        print(f"{YELLOW}[SYSTEM]: getting content files [DONE]{RESET}")
        print(f"{YELLOW}[SYSTEM]: getting Command files [DONE]{RESET}")
        time.sleep(0.2)
        clear()
        print(f"{YELLOW}[SYSTEM]: checking for updates [DONE]{RESET}")
        print(f"{YELLOW}[SYSTEM]: getting content files [DONE]{RESET}")
        print(f"{YELLOW}[SYSTEM]: getting Command files [DONE]{RESET}")
        print(f"{YELLOW}[SYSTEM]: getting Device files.{RESET}")
        time.sleep(0.2)
        clear()
        print(f"{YELLOW}[SYSTEM]: checking for updates [DONE]{RESET}")
        print(f"{YELLOW}[SYSTEM]: getting content files [DONE]{RESET}")
        print(f"{YELLOW}[SYSTEM]: getting Command files [DONE]{RESET}")
        print(f"{YELLOW}[SYSTEM]: getting Device files..{RESET}")
        time.sleep(0.2)
        clear()
        print(f"{YELLOW}[SYSTEM]: checking for updates [DONE]{RESET}")
        print(f"{YELLOW}[SYSTEM]: getting content files [DONE]{RESET}")
        print(f"{YELLOW}[SYSTEM]: getting Command files [DONE]{RESET}")
        print(f"{YELLOW}[SYSTEM]: getting Device files...{RESET}")
        time.sleep(0.2)
        clear()
        print(f"{YELLOW}[SYSTEM]: checking for updates [DONE]{RESET}")
        print(f"{YELLOW}[SYSTEM]: getting content files [DONE]{RESET}")
        print(f"{YELLOW}[SYSTEM]: getting Command files [DONE]{RESET}")
        print(f"{YELLOW}[SYSTEM]: getting Device files [DONE]{RESET}")
        time.sleep(0.2)
        clear()
        print(f"{YELLOW}[SYSTEM]: checking for updates [DONE]{RESET}")
        print(f"{YELLOW}[SYSTEM]: getting content files [DONE]{RESET}")
        print(f"{YELLOW}[SYSTEM]: getting Command files [DONE]{RESET}")
        print(f"{YELLOW}[SYSTEM]: getting Device files [DONE]{RESET}")
        print(f"{YELLOW}[SYSTEM]: getting Sound files.{RESET}")
        time.sleep(0.2)
        clear()
        print(f"{YELLOW}[SYSTEM]: checking for updates [DONE]{RESET}")
        print(f"{YELLOW}[SYSTEM]: getting content files [DONE]{RESET}")
        print(f"{YELLOW}[SYSTEM]: getting Command files [DONE]{RESET}")
        print(f"{YELLOW}[SYSTEM]: getting Device files [DONE]{RESET}")
        print(f"{YELLOW}[SYSTEM]: getting Sound files..{RESET}")
        time.sleep(0.2)
        clear()
        print(f"{YELLOW}[SYSTEM]: checking for updates [DONE]{RESET}")
        print(f"{YELLOW}[SYSTEM]: getting content files [DONE]{RESET}")
        print(f"{YELLOW}[SYSTEM]: getting Command files [DONE]{RESET}")
        print(f"{YELLOW}[SYSTEM]: getting Device files [DONE]{RESET}")
        print(f"{YELLOW}[SYSTEM]: getting Sound files...{RESET}")
        time.sleep(0.2)
        clear()
        print(f"{YELLOW}[SYSTEM]: checking for updates [DONE]{RESET}")
        print(f"{YELLOW}[SYSTEM]: getting content files [DONE]{RESET}")
        print(f"{YELLOW}[SYSTEM]: getting Command files [DONE]{RESET}")
        print(f"{YELLOW}[SYSTEM]: getting Device files [DONE]{RESET}")
        print(f"{YELLOW}[SYSTEM]: getting Sound files [DONE]{RESET}")
        time.sleep(0.5)
        clear()
    startup_animation = False

def Intro():
    global intro
    if intro:
        print(big_banner)
        intro = False

def help_message():
    global Help
    if Help:
        print(f"{CYAN} =|=||===============================================================================||=|={RESET}")
        print(fr"{BOLD}{CYAN}  | ||{RESET} {BOLD}COMMANDS:{RESET}       | \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/                   {CYAN}|| |{RESET}")
        print(f"{BOLD}{CYAN}  | ||{RESET} {GREEN}Sc{RESET}              | Scans for devices nearby                                    {CYAN}|| |{RESET}")
        print(f"{BOLD}{CYAN}  | ||{RESET} {GREEN}Cnt [ID] glitch{RESET} | Connects to device and plays sound                          {CYAN}|| |{RESET}")
        print(f"{BOLD}{CYAN}  | ||{RESET} {GREEN}Save [ID]{RESET}       | Saves the [ID] To temp file File                            {CYAN}|| |{RESET}")
        print(f"{BOLD}{CYAN}  | ||{RESET} {GREEN}Cd [ID]{RESET}         | Opens a tunnel or runs analysis                             {CYAN}|| |{RESET}")
        print(f"{BOLD}{CYAN}  | ||{RESET} {GREEN}Adapter{RESET}         | Shows Radio Status                                          {CYAN}|| |{RESET}")
        print(f"{BOLD}{CYAN}  | ||{RESET} {GREEN}Window{RESET}          | Opens this help in new window                               {CYAN}|| |{RESET}")
        print(f"{BOLD}{CYAN}  | ||{RESET} {GREEN}Clear{RESET}           | Clears the screen and device list                           {CYAN}|| |{RESET}")
        print(f"{BOLD}{CYAN}  | ||{RESET} {GREEN}Intro{RESET}           | Shows Banner again...                                       {CYAN}|| |{RESET}")
        print(f"{BOLD}{CYAN}  | ||{RESET} {GREEN}Sleep <sec>{RESET}     | Waits for seconds (can be used in chains)                   {CYAN}|| |{RESET}")
        print(f"{BOLD}{CYAN}  | ||{RESET} {GREEN}Help{RESET}            | Shows this message again...                                 {CYAN}|| |{RESET}")
        print(f"{BOLD}{CYAN}  | ||{RESET} {GREEN}Info{RESET}            | Shows information about the tool                            {CYAN}|| |{RESET}")
        print(f"{BOLD}{CYAN}  | ||{RESET} {RED}Exit{RESET}            | Quit...{RESET}                                                     {CYAN}|| |{RESET}")
        print(f"{BOLD}{CYAN} =|=||===============================================================================||=|={RESET}")
        print(f"{BOLD}{CYAN}  | ||{RESET} {BOLD}FLAGS (Use with Cd [ID]):      {CYAN}|| | ||{RESET} {BOLD}STATEMENTS:{RESET}     |                      {CYAN}|| |{RESET}")           
        print(f"{BOLD}{CYAN}  | ||{RESET} {YELLOW}-r{RESET}        | (Knock/MTU)        {CYAN}|| | ||{RESET} {YELLOW}&&{RESET}              | (Chain commands)     {CYAN}|| |{RESET}")
        print(f"{BOLD}{CYAN}  | ||{RESET} {YELLOW}-F{RESET}        | Deep Map           {CYAN}|| | ||{RESET} {YELLOW}/a{RESET}              | (All devices)        {CYAN}|| |{RESET}")
        print(f"{BOLD}{CYAN}  | ||{RESET} {YELLOW}-p{RESET}        | RSSI Ping          {CYAN}|| | ||{RESET} {YELLOW}/d<list>{RESET}        | (Exclude IDs)        {CYAN}|| |{RESET}")
        print(f"{BOLD}{CYAN}  | ||{RESET} {YELLOW}-b{RESET}        | Battery            {CYAN}|| | ||{RESET} {YELLOW}/n <list>{RESET}       | (Explicit IDs)       {CYAN}|| |{RESET}")
        print(f"{BOLD}{CYAN}  | ||{RESET} {YELLOW}-s{RESET}        | Services           {CYAN}|| | ||{RESET} {YELLOW}sleep <sec>{RESET}     | (Delay in chains)    {CYAN}|| |{RESET}")
        print(f"{BOLD}{CYAN}  | ||{RESET} {YELLOW}-m{RESET}        | Shadow/MITM        {CYAN}|| | ||{RESET} {YELLOW}/w{RESET}              | (New window output)  {CYAN}|| |{RESET}")
        print(f"{BOLD}{CYAN}  | ||{RESET} {YELLOW}-n [Name]{RESET} | Spoof Adapter Name {CYAN}|| | ||{RESET} {YELLOW}pause{RESET} (with -p) | (Single packet)      {CYAN}|| |{RESET}")
        print(f"{BOLD}{CYAN}  | ||{RESET} {YELLOW}-L{RESET}        | Live Logger        {CYAN}|| | ||{RESET}                                        {CYAN}|| |{RESET}")
        print(f"{BOLD}{CYAN} =|=||===============================================================================||=|={RESET}")
        Help = False

def show_help(topic=None):
    if topic is None:
        help_message()
    elif topic.lower() == "cd":
        print(f"\n{CYAN}[COMMAND]: Cd [ID] [flag]{RESET}")
        print("Description: Opens a tunnel or runs a specific analysis flag.")
        print(f"Flags: {YELLOW}-r{RESET} (Knock), {YELLOW}-F{RESET} (Map), {YELLOW}-p{RESET} (Ping), {YELLOW}-b{RESET} (Battery),")
        print(f"       {YELLOW}-s{RESET} (Services), {YELLOW}-m{RESET} (Shadow), {YELLOW}-L{RESET} (Log), {YELLOW}-n{RESET} (Name)")
        print(f"Advanced: {YELLOW}/a{RESET} (all), {YELLOW}/d<list>{RESET} (exclude), {YELLOW}/n <list>{RESET} (explicit)")
        print(f"Example: {GREEN}Cd 2 -b{RESET} (Check battery of device #2)")
        print(f"         {GREEN}Cd /a -F{RESET} (Scan all devices)")
    elif topic.lower() == "cnt":
        print(f"\n{CYAN}[COMMAND]: Cnt [ID] [glitch]{RESET}")
        print("Description: Connects to a device. Use 'glitch' for sound alert.")
        print(f"Example: {GREEN}cnt 1 glitch{RESET}")
    elif topic.lower() == "sc":
        print(f"\n{CYAN}[COMMAND]: Sc{RESET}")
        print("Description: Performs a 5-second environment scan for BLE devices.")
        print(f"Example: {GREEN}Sc{RESET}")
    elif topic.lower() == "window":
        print(f"{YELLOW}[SYSTEM]: Spawning persistent help window...{RESET}")
        with open("help_temp.txt", "w") as f:
            f.write("BT_CMD QUICK REFERENCE\n" + "="*25 + "\nSc - Scan\nCd [ID] [flag] - Analyze\nCnt [ID] glitch - Connect\n")
        os.system("start cmd /k type help_temp.txt")
    else:
        print(f"{RED}[ERROR]: idk what the command '{topic}' should be used for here...{RESET}")

# --- play warning_speed.wav when cmd == info ---
def info():
    print(f"{YELLOW}[INFO]: TTS should be talking right now...{RESET}")
    winsound.PlaySound(WARN_SPEECH, winsound.SND_FILENAME)
    print(f"{GREEN}[INFO]: should be done talking now...{RESET}")

def parse_device_targets(args, found_devices):
    """
    Parses /a, /d, /n syntax.
    Returns list of device indices (int) or None if invalid.
    args: list of tokens (e.g., ['/a', '/d3,5', '-F'])
    found_devices: list of scanned devices
    """
    target_spec = args[0] if args else ""
    if target_spec.startswith("/a"):
        all_indices = list(range(len(found_devices)))
        exclude = []
        if "/d" in target_spec:
            part = target_spec.split("/d")[-1]
            for num in part.split(','):
                if num.strip().isdigit():
                    exclude.append(int(num.strip()))
        indices = [i for i in all_indices if i not in exclude]
        return indices
    elif target_spec.startswith("/n"):
        numbers = []
        for token in args[1:]:
            if token.startswith('-'):
                break
            if token.isdigit():
                numbers.append(int(token))
        return numbers
    else:
        if target_spec.isdigit():
            return [int(target_spec)]
    return None

async def execute_command(cmd_tokens, found_devices, new_window=False):
    """
    Execute a single command (without && chaining).
    Returns True if should continue, False if exit requested.
    """
    if not cmd_tokens:
        return True
    cmd = cmd_tokens[0].lower()

    if cmd == "sleep":
        if len(cmd_tokens) > 1:
            try:
                sec = float(cmd_tokens[1])
                print(f"{CYAN}[SLEEP]: Waiting {sec} seconds...{RESET}")
                await asyncio.sleep(sec)
            except:
                print(f"{RED}[ERROR]: Invalid sleep time.{RESET}")
        else:
            print(f"{RED}Usage: sleep <seconds>{RESET}")
        return True
    
    if cmd == "cd":
        if len(cmd_tokens) < 2:
            print(f"{RED}Usage: Cd [target] [flag]{RESET}")
            return True
        
        target_indices = parse_device_targets(cmd_tokens[1:], found_devices)
        if target_indices is None:
            print(f"{RED}[ERROR]: Invalid target specification.{RESET}")
            error_sound()
            return True
        
        flag = None
        extra = None
        for token in cmd_tokens[2:]:
            if token.startswith('-'):
                flag = token
            elif token.lower() == "pause":
                extra = "pause"
            elif token == "/w":
                extra = "newwindow"
        
        if extra == "newwindow":
            filtered_tokens = [t for t in cmd_tokens if t != "/w"]
            cmd_line = " ".join(filtered_tokens)
            script_path = sys.argv[0]
            temp_bat = "temp_cmd.bat"
            with open(temp_bat, "w") as f:
                f.write(f'@echo off\npython "{script_path}" --exec "{cmd_line}"\npause\n')
            os.system(f'start cmd /k "{temp_bat}"')
            return True
        
        for idx in target_indices:
            if idx < 0 or idx >= len(found_devices):
                print(f"{RED}[ERROR]: Invalid ID {idx}{RESET}")
                continue
            device = found_devices[idx]
            print(f"{CYAN}--- Targeting device {idx}: {device.name or 'Unknown'} ---{RESET}")
            if flag == "-r":
                await handshake_knock(device)
            elif flag == "-F":
                await function_scan(device)
            elif flag == "-p":
                once = (extra == "pause")
                await rssi_ping(device, once=once)
            elif flag == "-b":
                await get_battery(device)
            elif flag == "-s":
                await quick_services(device)
            elif flag == "-m":
                await shadow_mitm(device)
            elif flag == "-L":
                await live_traffic_logger(device)
            elif flag == "-n":
                name_start = cmd_tokens.index("-n") + 1
                if name_start < len(cmd_tokens):
                    new_name = " ".join(cmd_tokens[name_start:])
                    spoof_name(new_name)
                else:
                    print(f"{RED}[ERROR]: Missing name for -n flag.{RESET}")
            else:
                await persistent_session(device)
        return True

    if cmd == "sc":
        print(f"{YELLOW}[RUNNING]: Scanning For Active Devices (5s)... {RESET}")
        new_devices = await BleakScanner.discover(timeout=5.0)
        found_devices.clear()
        found_devices.extend(new_devices)
        print(f"\n{BOLD}ID | NAME                 | MAC ADDRESS{RESET}")
        for i, d in enumerate(found_devices):
            print(f"[{GREEN}{i}{RESET}] {d.name or 'Hidden':<20} | {d.address}")
        return True
    elif cmd == "help":
        show_help(cmd_tokens[1] if len(cmd_tokens) > 1 else None)
        return True
    elif cmd == "info":
        info()
        return True
    elif cmd == "play":
        if len(cmd_tokens) < 2:
            print(f"{RED}Usage: Play [ID]{RESET}")
            return True
        try:
            idx = int(cmd_tokens[1])
            if 0 <= idx < len(found_devices):
                await connect_and_play(found_devices[idx])
            else:
                print(f"{RED}[ERROR]: Invalid ID.{RESET}")
        except:
            print(f"{RED}[ERROR]: Invalid ID.{RESET}")
        return True
    elif cmd == "save":
        if len(cmd_tokens) < 2:
            print(f"{RED}Usage: Save [ID]{RESET}")
            return True
        try:
            idx = int(cmd_tokens[1])
            if 0 <= idx < len(found_devices):
                save_device(found_devices[idx])
            else:
                print(f"{RED}[ERROR]: Invalid ID.{RESET}")
        except:
            print(f"{RED}[ERROR]: Invalid ID.{RESET}")
        return True
    elif cmd == "clear":
        clear()
        return True
    elif cmd == "adapter":
        await show_adapter()
        return True
    elif cmd == "intro":
        global intro
        intro = True
        return True
    elif cmd == "exit":
        return False
    elif cmd == "cnt":
        if len(cmd_tokens) < 2:
            print(f"{RED}Usage: Cnt [ID] [glitch]{RESET}")
            return True
        try:
            idx = int(cmd_tokens[1])
            if 0 <= idx < len(found_devices):
                glitch = (len(cmd_tokens) > 2 and cmd_tokens[2].lower() == "glitch")
                await connect_and_troll(found_devices[idx], mode="glitch" if glitch else None)
            else:
                print(f"{RED}[ERROR]: Invalid ID.{RESET}")
        except:
            print(f"{RED}[ERROR]: Invalid ID.{RESET}")
        return True
    elif cmd == "window":
        show_help("window")
        return True
    else:
        print(f"{RED} ⚠︎  Unknown command ({cmd})!{RESET} {BOLD}{YELLOW}Type 'Help' for options.{RESET}")
        error_sound()
        return True
