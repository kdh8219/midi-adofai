import pygame.midi
import pyautogui


class NoInputableMidiDevice(Exception):
    pass


def getMidiInput() -> pygame.midi.Input:

    midiList = []
    for n in range(pygame.midi.get_count()):
        midiList.append([n, pygame.midi.get_device_info(n)[0], pygame.midi.get_device_info(n)[1]]
                        if pygame.midi.get_device_info(n)[2] == 1 else "")

    midiList = list(filter(None, midiList))
    if len(midiList) == 0:
        raise(NoInputableMidiDevice(
            "No inputable MIDI devices found:Try to plug in a MIDI device and restart the program"))
    elif len(midiList) == 1:
        return pygame.midi.Input(midiList[0][0])
    else:
        print()
        print()
        for n in range(len(midiList)):
            print(f"{midiList[n][0]} {midiList[n][1]} {midiList[n][2]}")
        print()
        print()

        def intInput(prompt: str, errMsg: str = "Invalid input, try again") -> int:
            while True:
                try:
                    return int(input(prompt))
                except ValueError:
                    print(errMsg)
                    return(intInput(prompt, errMsg))

        midiDivice = intInput("Enter Midi Device Number: ")
        midiDivice = pygame.midi.Input(midiDivice)
        return midiDivice


def run(midiDivice: pygame.midi.Input, ONLY_UPPER_C5: bool,
        KEYLIST: list[str] = ['a', 'b', 'c', 'd', 'e', 'g', 'h', 'i',
                              'j', 'k', 'l', 'm', 'q', 'r', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        ) -> None:
    pyautogui.PAUSE = 0
    while True:
        if midiDivice.poll():
            event = midiDivice.read(1)[0]
            data = event[0]
            if ((ONLY_UPPER_C5 and (data[1] >= 72 and data[0] == 144)) or (not ONLY_UPPER_C5 and data[0] == 144)):
                pyautogui.keyDown(KEYLIST[data[1] % len(KEYLIST)])
                print(
                    f"{event}=>key down \"{KEYLIST[data[1] % len(KEYLIST)]}\"")
            elif ((ONLY_UPPER_C5 and (data[1] >= 72 and data[0] == 128)) or (not ONLY_UPPER_C5 and data[0] == 128)):
                pyautogui.keyUp(KEYLIST[data[1] % len(KEYLIST)])
                print(f"{event}=>key up \"{KEYLIST[data[1] % len(KEYLIST)]}\"")
            else:
                print(f"{event}")


if __name__ == "__main__":
    pygame.midi.init()

    def runner(only_upper_c5: bool = False):
        print("\nscope:", "only upper c5"if only_upper_c5 else "all")
        print()
        try:
            run(getMidiInput(), only_upper_c5)
        except NoInputableMidiDevice as e:
            print(f"\n \n {'*'*80} \n {e} \n {'*'*80}\n \n")
            exit()
    try:
        import typer
        typer.run(runner)
    except ImportError:
        print("\nno typer:\"\"\"install typer\"\"\"")
        runner()
