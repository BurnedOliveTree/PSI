#pragma once

#include <stdio.h>
#include <stdlib.h> 
#include <string.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <string>
#include <iostream>
#include "Socket.h"

class Server{
    Socket sock;
public:
    Server(std::string ip = "127.0.0.1" , int port = 8000);
    void SendString(std::string msg);
    void SendStruct(struct SimpStruct msg);
    std::string ReceiveString();
    std::shared_ptr<struct SimpStruct> ReceiveStruct();
    bool CheckQuit(std::string msg);
};