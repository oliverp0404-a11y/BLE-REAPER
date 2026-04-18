# BLE_REAPER 🔧💀

A Bluetooth Low Energy penetration testing and security assessment tool built for Raspberry Pi.

![BLE_REAPER Banner](banner.png)

## 🎯 Features

- 🔍 **BLE Device Scanning** - Discover nearby Bluetooth Low Energy devices
- 🔌 **Automated Pairing** - Connect to devices using system-level Bluetooth
- 📡 **Signal Tracking** - Monitor RSSI strength in real-time
- 🔋 **Battery Probing** - Extract battery levels from compatible devices
- 🎭 **Name Spoofing** - Change your adapter's broadcast name
- 🎵 **Audio Playback** - Play sound sequences upon connection
- 🕵️ **Shadow MITM** - Intercept BLE notifications and data streams
- 🧬 **GATT Fuzzing** - Test writable characteristics for vulnerabilities
- 💣 **DoS Testing** - Connection parameter manipulation attacks

## 📋 Requirements

- Raspberry Pi 3 or higher (built-in Bluetooth required)
- Raspberry Pi OS (or any Debian-based Linux)
- Python 3.7+

## 🚀 Installation

```bash
git clone https://github.com/oliverp0404-a11y/BLE-REAPER.git && cd BLE-REAPER/BLE_REAPER && sudo apt-get update && sudo apt-get install -y bluetooth bluez python3-pip && pip3 install -r requirements.txt && chmod +x main.py
