from pyfirmata import ArduinoNano, util
import time
board = ArduinoNano("COM4")
iterator = util.Iterator(board)
iterator.start()


while True:
    board.digital[13].write(1)
    time.sleep(1)
    board.digital[13].write(0)
    time.sleep(1)
