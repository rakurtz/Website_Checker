import threading
import queue
import time


def read_kbd_input(inputQueue):
    #print('Ready for keyboard input:')
    while True:
        input_str = input()
        inputQueue.put(input_str)


def main():
    EXIT_COMMAND = "q"
    COMMAND_1 = "1"
    COMMAND_2 = "2"
    COMMAND_3 = "3"

    inputQueue = queue.Queue()

    inputThread = threading.Thread(target=read_kbd_input, args=(inputQueue,), daemon=True)
    inputThread.start()

    while True:
        if inputQueue.qsize() > 0:
            input_str = inputQueue.get()
            print("input_str = {}".format(input_str))

            if input_str == EXIT_COMMAND:
                print("Exiting serial terminal.")
                break
            elif input_str == COMMAND_1:
                print("let's go to command 1")
            elif input_str == COMMAND_2:
                print("let's go to command 2")
            elif input_str == COMMAND_3:
                print("let's go to command 3")

            # Insert your code here to do whatever you want with the input_str.

        # The rest of your program goes here.

        time.sleep(0.01)
    print("End.")


if (__name__ == '__main__'):
    main()