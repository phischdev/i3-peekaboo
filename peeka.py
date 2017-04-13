import i3ipc
import subprocess
import sh

def sendsignal(signal, pid):
    process = subprocess.Popen(["kill", "-" + signal, pid])

def getfirefox():
    get = sh.grep(sh.ps("x", _piped=True), 'firefox')
    id = get.split()[0]
    return id;

def entered():
    #signal
    id = getfirefox()
    sendsignal("18", id)
    print("resumed firefox")

def left():
    # wait 10 seconds
    # signal
    id = getfirefox()
    sendsignal("19", id)
    print("stopped firefox")


def in_firefox():
    focused = i3.get_tree().find_focused()

    #print (focused)
    # print('focused window class: ', focused.window_class)
    return focused.window_class == "Firefox"


i3 = i3ipc.Connection();

# Dynamically name your workspaces after the current window class
def on_window_focus(i3, e):
    global infirefox

    if not infirefox and in_firefox():
        print('entered')
        infirefox = True
        entered()

    elif infirefox and not in_firefox():
        print('left')
        infirefox = False
        left()


    #i3.command('rename workspace to "%s"' % ws_name)

infirefox = in_firefox();


# Subscribe to events
# i3.on('workspace::focus', on_workspace_focus)
i3.on("window::focus", on_window_focus)

# Start the main loop and wait for events to come in.
i3.main()