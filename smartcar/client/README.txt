Introduction:
	This is Sunfounder Raspberry Pi smart video car client. It is based on Python.

Xbox Controller:
    sudo apt-get install xboxdrv
    sudo apt-get dist-upgrade
    sudo xboxdrv
    sudo xboxdrv --detach-kernel-driver

TODO dataset:
    ssh -Y pi@172.20.10.11
    cd ~/SmartCar/src/server
    python tcp_server.py

    "open new term"
    cd ~/SmartCar/src/client
    "plug xbox cell"
    sudo python client_controller.py
    "turn on controller"

Notice:
	Before you run the client routine, you must first run the server routine.
