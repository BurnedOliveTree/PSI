#include "Socket.h"

Socket::Socket(char* ip, int port, bool is_serv){
    is_server = is_serv;
    socket_ip = ip;
    socket_port = port;
    if (std::string(ip).find('.') != std::string::npos){
        std::cout << "Using IPv4" << std::endl; 
        desc_4.sin_family = AF_INET;
        desc_4.sin_port = htons( socket_port );

        if( inet_pton( AF_INET, socket_ip, & desc_4.sin_addr ) <= 0 )
        {
            std::cout << "inet_pton didn't convert IP";
        }
    
        sock = socket( AF_INET, SOCK_DGRAM, 0 );
        if(( sock ) < 0 )
        {
            std::cout << "Socket wasn't created";
        }
        socket_len = sizeof(desc_4);
        self_addr = (struct sockaddr*) &desc_4;
    }
    else {
        std::cout << "Using IPv6" << std::endl; 
        desc_6.sin6_family = AF_INET6;
        desc_6.sin6_port = htons( socket_port );

        if( inet_pton( AF_INET6, socket_ip, & desc_6.sin6_addr ) <= 0 )
        {
            std::cout << "inet_pton didn't convert IP";
        }
    
        sock = socket( AF_INET6, SOCK_DGRAM, 0 );
        if(( sock ) < 0 )
        {
            std::cout << "Socket wasn't created";
        }
        socket_len = sizeof(desc_6);
        self_addr = (struct sockaddr*) &desc_6;
    }
}

Socket::~Socket(){
    shutdown(sock, SHUT_RDWR);
}

void Socket::Bind(){
    if( bind( sock, self_addr, socket_len ) < 0 )
    {
        std::cout << "Socket wasn't binded";
    }
}

void Socket::Send(std::string msg){
    strncpy( buffer, msg.c_str(), sizeof(buffer));
    struct sockaddr* dst;
    socklen_t dst_len;
    if(is_server){
        dst = &dest_addr;
        dst_len = dest_len;
    }
    else{
        dst = self_addr;
        dst_len = socket_len;
    }
    if(sendto(sock, buffer, strlen(buffer), 0, dst, socket_len ) < 0 )
        {
            std::cout << "Couldn't send message to server";
        }
}

std::string Socket::Receive(){
    memset(buffer, 0, sizeof(buffer));
    struct sockaddr* dst;
    socklen_t* dst_len;
    if(is_server){
        dst = &dest_addr;
        dst_len = &dest_len;
    }
    else{
        dst = self_addr;
        dst_len = &socket_len;
    }
    if( recvfrom(sock, buffer, sizeof(buffer), 0, dst, &socket_len) < 0 )
        {   
            std::cout << "Couldn't receive message from server";
        }
    std::string msg(buffer);
    std::cout << "Received message: " << msg << std::endl;
    return msg;
}
