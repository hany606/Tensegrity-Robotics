#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>

#define port_num 10006
#define hostname "localhost"
#define BUFFER_SIZE 100

char buffer[BUFFER_SIZE];
struct sockaddr_in serv_addr;
struct hostent *server;
int sockfd;

void error(const char *msg)
{
    printf("ERROR\n");
    perror(msg);
    exit(0);
}

int main(int argc, char *argv[])
{
    
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(port_num);

    
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0) 
        error("ERROR opening socket");
    server = gethostbyname(hostname);
    if (server == NULL) {
        fprintf(stderr,"ERROR, no such host\n");
        exit(0);
    }
    
    
    if (connect(sockfd, (struct sockaddr *) &serv_addr, sizeof(serv_addr)) < 0) 
        error("ERROR connecting");


    while(1){
        strcpy(buffer,"Hello from the client\0");
        int n = write(sockfd, buffer, strlen(buffer));
        if (n < 0) 
            error("ERROR writing to socket");
        printf("Already wrote\n");
        bzero(buffer,256);
        n = read(sockfd, buffer, 255);
        if (n < 0) 
            error("ERROR reading from socket");
        printf("%s\n", buffer);
        int bla;
        scanf("%d",&bla);
        printf("asdasdas\n");
    }

    close(sockfd);
    return 0;
}