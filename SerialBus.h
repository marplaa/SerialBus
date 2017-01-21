#include "Arduino.h"

//#define DEBUG

#ifndef SerialBus_h
#define SerialBus_h

class SerialBus {

public:
	SerialBus(HardwareSerial *serial, long baudrate, byte address,
			void (*callback)(byte[], int));
	SerialBus(HardwareSerial *serial, long baudrate, byte address,
			void (*callback)(byte[], int), int sendPin);
	SerialBus(HardwareSerial *serial, long baudrate, byte address,
			void (*callback)(byte[], int), void (*callback_ack)(), int sendPin);
	void setAckCallback(void (*callback_ack)());
	void check();
	boolean waiting();
	//void sendMessage(byte[], byte);
	//int sendMessageAckWait(byte msg[], byte length, long timeout);
    //int sendMessageAckWait(byte msg[], byte length);
    byte sendDataAck(byte *data, int length);
    int sendDataAckWait(byte *data, int length, long timeout);
	//byte sendMessageTo(byte msg[], byte length, byte address,
	//		boolean permitToSend);
	//void sendMessage(String);
	byte sendData(byte *data, int length);
	void start();

private:
	byte _msg_index;
	byte _myAddress;
	long _baudrate;
	unsigned long _timeout_r;
	unsigned long _timeout_s;
	byte _message_in[60];
	byte _message_in_length;
	byte _checksum_in;
	byte _message_out[60];
	byte _message_out_length;

	int _max485_sendPin;
	void (*callback_function)(byte[], int);
	void init(HardwareSerial *serial, long baudrate, byte address,
			void (*callback)(byte[], int), void (*callback_ack)(), int sendPin);
	byte transmitDataBlock();
	void cleanUp();
	void newMessageReceived();
	boolean sendAck();
	boolean sendRawMessage(byte msg[], byte msg_length);
	byte get_XOR_checksum(byte str[], byte toIndex);
	void createHeader(byte message[], byte size, boolean pending, boolean ack);

};
#endif
