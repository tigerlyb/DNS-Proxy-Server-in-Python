import socket
import sys
import struct
import thread

# convert the UDP DNS query to the TCP DNS query
def getTcpQuery(query):
    message = "\x00"+ chr(len(query)) + query
    return message

# send a TCP DNS query to the upstream DNS server
def sendTCP(DNSserverIP, query):
    server = (DNSserverIP, 53)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server)
    tcp_query = getTcpQuery(query)
    sock.send(tcp_query)  	
    data = sock.recv(1024)
    return data

# a new thread to handle the UPD DNS request to TCP DNS request
def handler(data, addr, socket, DNSserverIP):
    #print "Request from client: ", data.encode("hex"), addr
    #print ""
    TCPanswer = sendTCP(DNSserverIP, data)
    #print "TCP Answer from server: ", TCPanswer.encode("hex")
    #print ""
    if TCPanswer:
        rcode = TCPanswer[:6].encode("hex")
        rcode = str(rcode)[11:]
        #print "RCODE: ", rcode
        if (int(rcode, 16) == 1):
            print "Request is not a DNS query. Format Error!"
        else:
            print "Success!"
            UDPanswer = TCPanswer[2:]
            #print "UDP Answer: ", UDPanswer.encode("hex")
            socket.sendto(UDPanswer, addr)
    else:
        print "Request is not a DNS query. Format Error!"

if __name__ == '__main__':
    DNSserverIP = sys.argv[1]
    port = int(sys.argv[2])
    host = ''
    try:
        # setup a UDP server to get the UDP DNS request
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((host, port))
        while True:
            data, addr = sock.recvfrom(1024)
            thread.start_new_thread(handler, (data, addr, sock, DNSserverIP))
    except Exception, e:
        print e
        sock.close()
