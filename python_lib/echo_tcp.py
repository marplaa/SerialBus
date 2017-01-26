from SerialBus import SerialBusTCP

serialbus = SerialBusTCP(host='localhost', port=6964)

while True:

    cmd = input('Send: ')
    answer = serialbus.send_request_wait(10, bytes(cmd, 'UTF8'))
    answer_str = "";
    for char in answer:
        answer_str += (chr(char))
    print(answer_str)
