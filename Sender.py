import sys
import getopt

import Checksum
import BasicSender

'''
This is a skeleton sender class. Create a fantastic transport protocol here.
'''


# I try to follow the rules, but I got so caught up by my implementations.
# on
""" 
I send out 5 packets.
#wait for acks, once you get the acks then, I can store 
#them in a dictionary (this is what i want). 
# most important thing is tnot send something, if the reciever 
#the reciever's window is not ready for it. 
# For example, sending packet 6, when reciever has noly recived 
 packet 2. You need to wait till tehy ack packet 1.

# other test cases. If you have both packet 1 and 2, +
I can move my window to [3,4,5,6,7] so as long as I follow these rules..
I make sure that I don't increment my window wrong, I should be good.
"""

class Sender(BasicSender.BasicSender):
    seqno = 0
    packet_size = 1300
    window = 5
    current = 0
#    size = 5
    message = [] # message[0] is first packet, message[1] is second packet, ... , message[n-1] is last packet (n messages)
    last_packet_no = None
    ack_no = 0 # the last ack we received

    # Main sending loop.
    def start(self):
        self.send_receive_loop()

    def dict_next(self):
        # rewrite this function!
        # it will be called ONCE at the beginning of the program
        # when it is called, it will fill up the array self.message
        # with EVERY single packet.
        if len(self.message) == 0
            message = self.infile.read(self.packet_size)
            self.message = 'data'

                self.msg_type = 'start'
            elif msg == "":
                self.last_packet_no = self.seqno
                self.infile.close()


    def send_five(self, ack_no):
        window_start = ack_no
        if window_start > len(self.message):
            window_start = len(self.message)

        window_end = ack_no + self.window - 1
        if window_end > len(self.message):
            window_end = len(self.message)

        for n in range(window_start, window_end + 1):
            if 0 <= n < len(self.message):
                self.send(self.message[n])

    def send_receive_loop(self):
        while True:
            self.send_five(self.ack_no)
            response = self.receive(.5)
            if response is not None and Checksum.validate_checksum(response):
                # ack_no is always the last received ack
                if self.ack_no <= self.ack_number(response):
                    self.ack_no = self.ack_number(response)

#            if self.window == self.last_packet_no:
            if ack_no >= len(message):
                break

    def ack_number(self, response):
        return int(response.split('|')[1])

    def handle_timeout(self):
        pass

    def handle_dup_ack(self, ack):
        pass

    def log(self, msg):
        if self.debug:
            print msg

'''
This will be run if you run this script from the command line. You should not
need to change any of this.
'''
if __name__ == "__main__":
    def usage():
        print "BEARS-TP Sender"
        print "-f FILE | --file=FILE The file to transfer; if empty reads from STDIN"
        print "-p PORT | --port=PORT The destination port, defaults to 33122"
        print "-a ADDRESS | --address=ADDRESS The receiver address or hostname, defaults to localhost"
        print "-d | --debug Print debug messages"
        print "-h | --help Print this usage message"

    try:
        opts, args = getopt.getopt(sys.argv[1:],
                               "f:p:a:d", ["file=", "port=", "address=", "debug="])
    except:
        usage()
        exit()

    port = 33122
    dest = "localhost"
    filename = None
    debug = False

    for o,a in opts:
        if o in ("-f", "--file="):
            filename = a
        elif o in ("-p", "--port="):
            port = int(a)
        elif o in ("-a", "--address="):
            dest = a
        elif o in ("-d", "--debug="):
            debug = True

    s = Sender(dest,port,filename,debug)
    try:
        s.start()
    except (KeyboardInterrupt, SystemExit):
        exit()
