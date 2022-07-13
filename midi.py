import pygame.midi
import pyautogui
pygame.midi.init()

# SETUP
ONLY_UPPER_C5 = False
USE_LONG_NOTE = False
KEYLIST = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
           'm', 'n', 'o', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']


def getMidiInput():

    global NoInputableMidiDevice

    class NoInputableMidiDevice(Exception):
        pass

    midiList = []
    for n in range(pygame.midi.get_count()):
        midiList.append(f"{n} {pygame.midi.get_device_info(n)[0]} {pygame.midi.get_device_info(n)[1]}"
                        if pygame.midi.get_device_info(n)[2] == 1 else "")

    midiList = list(filter(None, midiList))
    if len(midiList) == 0:
        raise(NoInputableMidiDevice(
            "No inputable MIDI devices found:Try to plug in a MIDI device and restart the program"))
    print()
    print()
    for n in range(len(midiList)):
        print(f"{midiList[n]}")
    print()
    print()

    def intInput(prompt):
        while True:
            try:
                return int(input(prompt))
            except ValueError:
                print("Invalid input, try again")
                return(intInput(prompt))

    global midiDivice
    midiDivice = intInput("Enter Midi Device Number: ")
    midiDivice = pygame.midi.Input(midiDivice)


def main():
    while True:
        if midiDivice.poll():
            event = midiDivice.read(1)[0]
            data = event[0]
            if ((ONLY_UPPER_C5 and (data[1] >= 72 and data[0] == 144)) or (not ONLY_UPPER_C5 and data[0] == 144)):
                if USE_LONG_NOTE:
                    pyautogui.keyDown(KEYLIST[data[1] % len(KEYLIST)])
                    print(
                        f"{event}=>key down \"{KEYLIST[data[1] % len(KEYLIST)]}\"")
                else:
                    pyautogui.press(KEYLIST[data[1] % len(KEYLIST)])
                    print(
                        f"{event}=>key press \"{KEYLIST[data[1] % len(KEYLIST)]}\"")
            elif (USE_LONG_NOTE and ((ONLY_UPPER_C5 and (data[1] >= 72 and data[0] == 128)) or (not ONLY_UPPER_C5 and data[0] == 128))):
                pyautogui.keyUp(KEYLIST[data[1] % len(KEYLIST)])
                print(f"{event}=>key up \"{KEYLIST[data[1] % len(KEYLIST)]}\"")
            else:
                print(f"{event}")


if __name__ == "__main__":
    try:
        getMidiInput()
    except NoInputableMidiDevice as e:
        print()
        print()
        print("*"*80)
        print(e)
        print("*"*80)
        print()
        print()
        exit()
    main()
