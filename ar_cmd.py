from data_ar import AData, NoDeviceError, StoppableThread

def display_help():
    print "\nCommands:"
    print "  help		Display this information"
    print "  speed		View and/or change speed of sound"
    print "  path		View and/or change data path for log file"
    print "  measure	Trigger a measurement"

data = AData('ruler.cfg')

input = ""

while (input != "quit"):
    input = raw_input("> ")

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
            distance, delay = data.measure('m')
            print str(distance)+" m\n"
            print str(delay)+" s\n"
        except NoDeviceError:
            print "Device Not Found."

    elif input == "repeat":
        rep_thread = StoppableThread(data)
        rep_thread.start()

    elif input == "stop":
        rep_thread.stop()
        print rep_thread.stopped()

    elif input == "networks":
        ss_list = data.get_networks()
        print ss_list

    elif input == "quit":
        pass

    else:
        display_help()

data.quit()
