from SerialBus import SerialBus

serialbus = SerialBus(baud = 19200, serialnum="ABCD")

while True:

    cmd = input('Send: ')
    answer = serialbus.send_request_wait(10, bytes(cmd, 'ascii'))
    answer_str = "";
    for char in answer:
        answer_str += (chr(char))
    print(answer_str)
