from Aserver import Aserver, DeviceTimeoutError
from Adata import Adata

def display_help():
    print "\nCommands:"
    print "  help		Display this information"
    print "  speed		View and/or change speed of sound"
    print "  path		View and/or change data path for log file"
    print "  measure	Trigger a measurement"


data = Adata('ruler.cfg')

input = ""

while (input != "quit"):
    input = raw_input(">")
    if input == "help":
        display_help()
    elif input == "speed":
        print "speed of sound is %f m/s" % data.speed
        change = raw_input("Change? (y/n): ")
        if change == "y":
            while True:
                try:
                    newspeed = raw_input("Please enter speed of sound (m/s): ")
                    data.changespeed(newspeed)
                    break
                except ValueError:
                    print "It needs to be a number..."
        else:
            pass
    elif input == "path":
        print "log path is %s" % data.path
        change = raw_input("Change? (y/n): ")
        if change == "y":
            newpath = raw_input("Please enter data path for log file: ")
            data.changepath(newpath)
        else:
            pass
    elif input == "measure":
        try:
            distance = data.measure()
            print distance
        except DeviceTimeoutError:
            print "Device Not Found."
    elif input == "quit":
        pass
    else:
        display_help()

data.quit()
