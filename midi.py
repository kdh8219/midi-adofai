import pygame.midi
import pyautogui
pygame.midi.init()
KEYLIST = [' ', "'", ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ';', '=', '[', '\\', ']', '`', 'a',
           'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

# SETUP
ONLY_UPPER_C5 = False
USE_LONG_NOTE = False


for n in range(pygame.midi.get_count()):
    print(n, pygame.midi.get_device_info(n))


def intInput(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input, try again")
            return(intInput(prompt))


midiDivice = intInput("Enter Midi Device Number: ")
midiDivice = pygame.midi.Input(midiDivice)


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
