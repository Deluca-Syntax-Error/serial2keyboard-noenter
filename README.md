# Que hace este fork
Este fork es una adaptacion del código original creado por Robotto pero adaptado a un proyecto escolar, el proyecto consiste en controlar un sistema windows7-11(esto debido a las hotkeys que se usan pero se podria adaptar según el OS que se use) con un control remoto IR, se agrega un código para un arduino con un receptor IR, este receptor al recibir ciertos código con un control remoto especifico envia ciertos bytes por el serial, el script serial2keyboard.py según el byte que recibe hace una order diferente, por ejemplo hay bytes especiales para que presione la tecla windows, suba/baje el volumen, toque enter, etc.

# serial2keyboard
Python script that listens to serial data and pushes virtual keyboard keys. Baudrate defaults to 9600, but is changeable with the optional second command line agument. 

This works really well with Arduino's 
```Serial.prinln()``` function, as it waits for a newline terminated ASCII string to arrive, so an arduino could go:
```Serial.println("password");``` and this program would type ```password``` and press [ENTER] for you.

# requirements if you want to run it with python
```
pip3 install pynput pyserial
```

# how to run it with python3
Easiest way if you have python installed is to just ```python3 serial2keyboard.py [port] [optional: baudrate]``` 
This shold run on any operating system with the required packages installed.

# Running the precompiled binaries

There's precompiled binaries built with pyinstaller (--onefile) for Windows, OSX and linux.

They shouldn't require you to install anything else... 

On windows type something like: 
```serial2keyboard.exe COM3 9600```

On linux you go:
```./serial2keyboard /dev/ttyUSB0 9600```

Mac users, of course, already know how to do this, but in case you forgot:
```./serial2keyboardOSX /dev/tty.usbserial-1410 9600```

Bonus for Windows users: [installing any program as a service](https://stackoverflow.com/a/26626771) (untested) 
# Waitaminute.. what's my serial port??
Just run the program without any additional arguments to run a scan that results in a list of suitable canditates. Thank you to CalPolyUROV for the nifty serial list function [from here](https://github.com/CalPolyUROV/UROV2019/blob/master/raspi/snr/comms/serial/serial_finder.py) 

