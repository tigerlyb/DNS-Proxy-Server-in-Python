DNS Proxy Server 
================

Source code: DNSserver.py

For Testing: 
Run the server at port 6760: python DNSserver.py 128.192.1.9 6760

Test the server: 
dig -p 6760 @172.17.152.18 www.uga.com

If an UDP DNS request is coming, the server will start a new thread to handler this request, convert the UDP request to TCP and send it to the upstream DNS server. If the request is not a DNS query, the server will drop it. When the server got the TCP answer from upstream DNS server, it will convert to UDP answer and send it back to the client.

Description:
This project is to design and develop a DNS proxy. A DNS proxy is a DNS forwarder program that acts as a DNS resolver for client programs but requires an upstream DNS server to perform the DNS lookup. The DNS proxy receives queries from outside and forward queries to a DNS server.

For this project, the proxy is required to receive queries in UDP mode, which is the default transport protocol for DNS. However, for forwarding query to a DNS server, TCP should be used by the proxy.  No caching capacity is required.  

The proxy should only forward valid DNS request. For incoming UDP packets that do not have a valid DNS header, those packets should be discarded.

This proxy program take two command line arguments: 
1) upstream DNS server IP address; 
2) local UDP port number for the proxy.
