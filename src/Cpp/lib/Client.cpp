#include "Client.h"

Client::Client(std::string ip, int port):sock(ip,port, false){
}

void Client::SendString(std::string msg){
    sock.Send(msg.c_str(),msg.length());
}

std::string Client::Receive(){
    return sock.Receive();
}