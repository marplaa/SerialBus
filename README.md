# SerialBus
Arduino library for a simple master-slave network using MAX485

It is quite easy to use!

Python code:

```python
>>> from SerialBus import SerialBus
>>> bus = SerialBus(baud = 19200, serialnum = "ABCD")
>>> bus.send_request_wait(10, bytes('?', 'ascii'), is_string = True)
'Hello from slave number 10!'
```

Arduino code:

```c++
void new_message(byte msg[], int len) {
  if (msg[0] == '?') {
    byte msg_out[] = "Hello from slave number 10!";
    bus.sendData(msg_out, sizeof(msg_out)-1);
  }
}
```

See the wiki for ducumentation: https://github.com/marplaa/SerialBus/wiki
