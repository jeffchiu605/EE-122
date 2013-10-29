import sys
import getopt

import Checksum
import BasicSender

'''
This is a skeleton sender class. Create a fantastic transport protocol here.
'''
"""
class Sender(BasicSender.BasicSender):
    def __init__(self, dest, port, filename, debug=False):
        super(Sender, self).__init__(dest, port, filename, debug)
"""
class Sender(BasicSender.BasicSender):
    seqno = 0
    msg_type = None
    packet_size = 1300
    window = 0
    current = 0
    size = 5
    message = {}
    last_packet_no = None

"""
    # Main sending loop.
    def start(self):
        raise NotImplementedError

    def handle_timeout(self):
        pass

    def handle_new_ack(self, ack):
        pass

    def handle_dup_ack(self, ack):
        pass

    def log(self, msg):
        if self.debug:
            print msg

"""    

    # Main sending loop.
    def start(self):
        self.send_first_five()
        self.send_receive_loop()

    def dict_next(self):
        if self.msg_type != 'end':
            msg = self.infile.read(self.packet_size)
            self.msg_type = 'data'
            if self.seqno == 0:
                self.msg_type = 'start'
            elif msg == "":
                self.msg_type = 'end'
                self.last_packet_no = self.seqno
                self.infile.close()

            packet = self.make_packet(self.msg_type, self.seqno, msg)
            self.message[self.seqno] = packet
            if len(self.message) > 2 * self.size:
                del self.message[self.seqno-self.size]
            self.seqno += 1

    def send_first_five(self):
        for n in range(5):
            self.dict_next()
            if n in self.message:
                self.send(self.message[n])

    def send_receive_loop(self):
        while True:
            response = self.receive(.5)
            if response is not None and Checksum.validate_checksum(response):
                ack_no = self.ack_number(response)
                if ack_no > self.window:
                    self.dict_next()
                    self.window += 1
                    self.increment_current()
            else:
                self.increment_current()
            self.send(self.message[self.current])
            if self.window == self.last_packet_no:
                break

    def ack_number(self, response):
        return int(response.split('|')[1])

    def increment_current(self):
        self.current += 1
        if self.current >= (self.window + self.size):
            self.current = self.window
        if self.current > self.last_packet_no and self.last_packet_no is not None:
            self.current = self.last_packet_no



'''
This will be run if you run this script from the command line. You should not
change any of this; the grader may rely on the behavior here to test your
submission.
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
