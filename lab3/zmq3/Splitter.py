import pickle
import random
import sys
import time

import zmq

import constPipe

fileToSplit = open(sys.argv[1], "rt")

src = constPipe.SRC  # check task src host
prt = constPipe.PORT1 # check task src port

context = zmq.Context()
push_socket = context.socket(zmq.PUSH)  # create a push socket

address = "tcp://" + src + ":" + prt  # how and where to connect
push_socket.bind(address)  # bind socket to address

time.sleep(1) # wait to allow all clients to connect

# splitting

for line in fileToSplit:
    workload = line.split('.')
    for sentence in workload:
        if not sentence.strip():
            continue
        push_socket.send(pickle.dumps(sentence.strip()))  # send workload to worker