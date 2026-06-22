# OculusDash-ODTKRA_Switcher

This tool lets you easely switch between the original Oculus Dash and ODTKRA.

I made this tool as I need sometimes the original Oculus Dash to set the floor level and it was annoying to do it manually.

## Usage

Download the latest release and run it. It will automatically switch between OculusDash and ODTKRA.

## Build

Use pyinstaller (``pip install pyinstaller``) :

```bash
pyinstaller --onefile --uac-admin --add-data "ODTKRA.exe;." --name "OculusDash-ODTKRA Switcher" main.py
```

## Attribution

Thanks to :
- DeltaNeverUsed for ODTKRA
