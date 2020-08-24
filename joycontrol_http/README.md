# joycontrol-http

使用 `FastApi` 对 `joycontrol` 项目进行了封装。

## Installation
- Install dependencies

Ubuntu: Install the `dbus-python` and `libhidapi-hidraw0` packages
```bash
sudo apt install python3-dbus libhidapi-hidraw0
```

Arch Linux Derivatives: Install the `hidapi` and `bluez-utils-compat`(AUR) packages


- Clone the repository and install the joycontrol package to get missing dependencies (Note: Controller script needs super user rights, so python packages must be installed as root). In the joycontrol folder run:
```bash
cd http
sudo pip3 install .
```
- Consider to disable the bluez "input" plugin, see [#8](https://github.com/mart1nro/joycontrol/issues/8)

## Use `Uvicorn` to start up a FastApi http server.
- Run the script
```bash
sudo python3 run_http_server.py
```
This will create a PRO_CONTROLLER instance waiting for the Switch to connect.

- Open the "Change Grip/Order" menu of the Switch

The Switch only pairs with new controllers in the "Change Grip/Order" menu.

Note: If you already connected an emulated controller once, you can use the reconnect option of the script (-r "\<Switch Bluetooth Mac address>").
This does not require the "Change Grip/Order" menu to be opened. You can find out a paired mac address using the "bluetoothctl" system command.

- After connecting, a command line interface is opened. Note: Press \<enter> if you don't see a prompt.

Call "help" to see a list of available commands.

- If you call "test_buttons", the emulated controller automatically navigates to the "Test Controller Buttons" menu. 
