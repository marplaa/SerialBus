import socket
import sys
import time

class SerialBusTCP:

    

    CONNECTION_ERROR = 5

    

    waiting = False
    msg_index = 0



    def __init__(self, host = None, port = None):
        if host is not None and port is not None:
            self.connect(host, port)

    def close(self):
        if self.connected:
            self.sock.close()
            self.connected = False

    def is_connected():
        return self.connected


    def wait_until_ready(self, address):
        
        while self.send_request_wait(address, bytes([4])) is None:
            pass
        

    def get_device_vidpid(self, vendor_id, product_id):

        # a list containing active ports
        portlist = list(serial.tools.list_ports.comports())

        for device in portlist:
            if device.pid == product_id and device.vid == vendor_id:
                return device.device

    def build_header(self, address, permission_to_send, size):

        # header: 11111111 10XYYYYY 11111111 1ZZZZZZ1
        # X = permission to send
        # Y = slave address
        # Z = message size incl checksum

        header_1 = 128 + address
        if permission_to_send:
            header_1 += 32

        header_3 = 129 + (size << 1)

        header = [255, header_1, 255, header_3]
        
        return bytes(header)


    def connect(self, host, port):
        """ port as device name e.g. "/dev/ttyUSB0"
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        

        try:
            # Connect to server and send data
            
            self.sock.connect((host, port))
            self.sock.settimeout(2.0)
            self.connected = True
        except:
            raise


    def send_msg(self, address, msg):
        """ send a message to address. permission to send = false"""

        header = self.build_header(address, True, len(msg)+1)
        message = header + bytes(msg)
        message += bytes([self.build_XOR_checksum(message)])

        self.send_raw_message(message)


    def send_request(self, address, msg):
        """ send a request. permission to send = true """
        header = self.build_header(address, True, len(msg)+1)
        message = header + bytes(msg)
        message += bytes([self.build_XOR_checksum(message)])
        self.send_raw_message(message)

    def send_request_wait(self, address, msg, timeout=5.0):
        """ send a request. permission to send = true """
        try:
            header = self.build_header(address, True, len(msg)+1)
            message = header + bytes(msg)
            message += bytes([self.build_XOR_checksum(message)])

            self.send_raw_message(message)
            

            s_address, answer = self.retrieve_msg(timeout=timeout)

            if (address == s_address):
                return answer
            else:
                return "wrong address"
        except:
            raise

    def send_ack(self, address, checksum):
        """ send a message to address. permission to send = false"""
        
            
        header = bytes([255, 128 + 64 + address, 255, 133])
        message = bytes(header) + bytes([checksum])
        message += bytes([self.build_XOR_checksum(message)])

        self.send_raw_message(message)

    def retrieve_next_part(self, address, checksum, msg, timeout=10**4):

        header = bytes([255, 128 + 64 + 32 + address, 255, 133])
        message = bytes(header) + bytes([0])
        message += bytes([self.build_XOR_checksum(message)])

        self.send_raw_message(message)

        s_address, answer = self.retrieve_msg(timeout=timeout)
        
        msg += answer

        return address, msg


    def return_message(self, address, msg):
        return address, msg
        
    def send_raw_message(self, raw_message):
        """ send raw message. sends raw_message as is """
        try:
            self.sock.sendall(raw_message)
        except:
            return

    def get_message(self, target):
        pass


    def retrieve_msg(self, timeout = 10**4):
        finished = False

        msg = []
        header = [0b00000000] * 4
        msg_size = 0
        msg_index = 0

        current_millis = 0
        start_millis = time.time()
        
        while current_millis - start_millis < timeout:

            current_millis = time.time()

            rawByte = self.sock.recv(1)
            if rawByte:
                inByte = ord(rawByte)
                #print(chr(int(inByte)), end='')
            else:
                return -1, None


            if msg_index > 3:
                #retrieve message

                msg.append(inByte)
                msg_index = msg_index + 1

                if msg_index == msg_size + 4:
                    # validate message
                    if self.is_valid_message(bytes(header + msg)):
                        checksum = msg[len(msg)-1]
                        if ack:
                            checksum = msg[len(msg)-1]
                            self.send_ack(address, checksum)
                        if pending:
                            return self.retrieve_next_part(address, checksum, msg[:len(msg)-1], timeout)
                        
                        return address, msg[:len(msg)-1]
                    else:
                        return -1, None
                        
            elif (msg_index == 0):
                if inByte == 255:
                    msg_index = 1
                    header[0] = 255
  
                else:
                    msg_index = 0
            elif msg_index == 1:
                
                if inByte < 128:
                    msg_index = 2
                    header[1] = inByte
                    address = inByte & 0b00011111
                    ack = inByte & 0b01000000
                    pending = inByte & 0b00100000
                    
                elif inByte == 255:
                    msg_index = 1
                else:
                    msg_index = 0
            elif msg_index == 2:
                if inByte == 255:
                    msg_index = 3
                    header[2] = 255
                    
                else:
                    msg_index = 0
            elif msg_index == 3:
                if inByte > 129:
                    #header complete
                    msg_size = (inByte - 129) >> 1
                    
                    msg_index = 4
                    header[3] = inByte
                    
                elif inByte < 128:
                    msg_index == 2
                    header[1] = inByte
                elif inByte == 255:
                    msg_index = 1
                else:
                    msg_index = 0
        return "Error retrieving"
            
        


            
        
    def is_valid_message(self, msg):

        if (msg[0] == 255 and not msg[1] & 0b10000000 and msg[2] == 255 and msg[3] & 0b10000001):
            # might be a valid message. check checksum
            size = (msg[3] & 0b01111110) >> 1
            if (len(msg) == size + 4):
                return self.check_checksum(msg)

        return False
                

    def decode_message(self, msg):
        """ returns slave address and message"""

        if self.is_valid_message(msg):
            
            address = msg[1] & 0b00011111
            message = msg[4:len(msg)-1]

            return address, message


    def check_checksum(self, msg):
        if self.build_XOR_checksum(msg[:len(msg)-1]) == msg[len(msg)-1]:
            return True
        return False

    def build_XOR_checksum(self, msg):
        # creates a XOR Checksum of msg

        result = 0b00000000
        for byte in msg:
            result = result ^ byte
        return result

    

