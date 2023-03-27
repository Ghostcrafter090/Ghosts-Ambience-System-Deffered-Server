import modules.pytools as pytools

def main():
    pytools.IO.unpack(".\\working\\clocks\\running\\running.zip", ".\\working\\clocks\\running")
    pytools.IO.unpack(".\\working\\sound\\clock\\clock.zip", ".\\working\\sound\\clock")
    pytools.net.download("https://gsweathermore.ddns.net/files/ambience_py_fire.zip", ".\\working\\sound\\fire\\fire.zip", 1)
    pytools.IO.unpack(".\\working\\sound\\fire\\fire.zip", ".\\working\\sound\\fire")
    pytools.net.download("https://gsweathermore.ddns.net/files/ambience_py_assets.zip", ".\\working\\sound\\assets\\assets.zip", 1)
    pytools.IO.unpack(".\\working\\sound\\assets\\assets.zip", ".\\working\\sound\\assets")
    print("Installed Successfully.")

main()