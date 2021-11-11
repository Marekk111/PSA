#!/usr/bin/env python
import struct
import socket

DNS_CLIENT_PORT = 60000
DNS_SERVER_PORT = 53
DNS_SERVER = '1.1.1.1'

#DNS hlavicka
transaction_id = 0x1234
flags = 0x0100
question_count = 1
answer_count = 0
authority_count = 0
additional_count = 0

dns_hlavicka_bajty = struct.pack("!6H",
                                transaction_id,
                                flags,
                                question_count,
                                answer_count,
                                authority_count,
                                additional_count)

#DNS telo - question
question_text = input("Zadajte DNS meno: ")
question_list = question_text.split(".")

qname = bytes()
for label in question_list:
    qname += struct.pack("!B", len(label))
    qname += label.encode()
qname += struct.pack("!B", 0)

qtype = struct.pack("!H", 1)
qclass = struct.pack("!H", 1)

dns_body_bytes = qname + qtype +qclass

#vytvorenie socketu
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", DNS_CLIENT_PORT))

#poslanie ziadosti
sock.sendto(dns_hlavicka_bajty + dns_body_bytes, (DNS_SERVER, DNS_SERVER_PORT))

#prijem odpovede
reply_bytes, reply_addr = sock.recvfrom(1000)

(transaction_id, flags) = struct.unpack("!2H", reply_bytes[0:4])
ip = socket.inet_ntoa(reply_bytes[-4:])

print("Odpoved od {}:{} - id: 0x{:02X}, flags: 0x{:02X}, addr: {}".format(reply_addr[0], 
                                                            reply_addr[1], 
                                                            transaction_id,
                                                            flags,
                                                            ip))

sock.close()