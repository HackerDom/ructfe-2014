#include <netinet/in.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/poll.h>
#include <sys/fcntl.h>

#include <errno.h>
#include <limits.h>

#include <unistd.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

#define PORT 1013
#define BACKLOG_LEN 128
#define TRUE 1
#define FALSE 0

void make_non_blocking(int fd)
{
    int flags = fcntl(fd, F_GETFL, 0);
    if (fcntl(fd, F_SETFL, flags | O_NONBLOCK) < 0)
    {
        perror("fcntl() failed");
        exit(-1);
    }
}

void
run(int listen_port)
{
    int len, rc, one = 1;
    int listen_sd = -1, new_sd = -1;
    int compress_array = FALSE;
    int close_conn;
    char buffer[1024];
    struct sockaddr_in sin;
    struct pollfd fds[BACKLOG_LEN * 2];
    int nfds = 1, current_size = 0, i, j;

    listen_sd = socket(AF_INET, SOCK_STREAM, 0);
    if (listen_sd < 0)
    {
        perror("socket() failed");
        exit(-1);
    }

    {
        rc = setsockopt(listen_sd, SOL_SOCKET, SO_REUSEADDR, &one, sizeof(one));
        if (rc < 0)
        {
            perror("setsockopt() failed");
            exit(-1);
        }
    }

    make_non_blocking(listen_sd);

    memset(&sin, 0, sizeof(sin));
    sin.sin_family = AF_INET;
    sin.sin_addr.s_addr = 0;
    sin.sin_port = htons(listen_port);
    if (bind(listen_sd, (struct sockaddr*)&sin, sizeof(sin)) < 0) {
        perror("bind() failed");
        exit(-1);
    }

    if (listen(listen_sd, BACKLOG_LEN) < 0) {
        perror("listen() failed");
        exit(-1);
    }

    memset(fds, 0 , sizeof(fds));
    fds[0].fd = listen_sd;
    fds[0].events = POLLIN;

    while (1) {
        printf("Waiting on poll()...\n");
        rc = poll(fds, nfds, -1);
        if (rc < 0)
        {
            perror("poll() failed");
            break;
        }

        current_size = nfds;
        for (i = 0; i < current_size; i++)
        {
            if(fds[i].revents == 0)
            {
                printf("cur %d, list %d\n", fds[i].fd, listen_sd);
                continue;
            }

            // if(fds[i].revents != POLLIN)
            // {
            //     printf("    Error! revents = %d\n", fds[i].revents);
            //     exit(-1);
            // }

            if (fds[i].fd == listen_sd)
            {
                printf("    Listening socket is readable\n");

                do
                {
                    struct sockaddr_in ss;
                    socklen_t slen = sizeof(ss);
                    new_sd = accept(listen_sd, (struct sockaddr*)&ss, &slen);
                    if (new_sd < 0)
                    {
                        if (errno != EWOULDBLOCK && errno != EAGAIN)
                        {
                            perror("    accept() failed");
                            exit(-1);
                        }
                        break;
                    }

                    printf("    New incoming connection - %d\n", new_sd);

                    make_non_blocking(new_sd);
                    fds[nfds].fd = new_sd;
                    fds[nfds].events = POLLIN;
                    nfds++;
                } while (new_sd != -1);
            }
            else
            {
                printf("    Descriptor %d is readable\n", fds[i].fd);
                close_conn = FALSE;

                do
                {
                    printf("Starting recv\n");
                    rc = recv(fds[i].fd, buffer, sizeof(buffer), 0);
                    printf("Recved %d bytes\n", rc);
                    if (rc < 0)
                    {
                        if (errno != EWOULDBLOCK && errno != EAGAIN)
                        {
                            perror("    recv() failed");
                            close_conn = TRUE;
                        }
                        break;
                    }

                    if (rc == 0)
                    {
                        printf("    Connection closed\n");
                        close_conn = TRUE;
                        break;
                    }

                    len = rc;
                    printf("    %d bytes received\n", len);

                    rc = send(fds[i].fd, buffer, len, 0);
                    if (rc < 0)
                    {
                        perror("    send() failed");
                        close_conn = TRUE;
                        break;
                    }

                } while(TRUE);
                printf("Exited recv loop\n");

                if (close_conn)
                {
                    close(fds[i].fd);
                    fds[i].fd = -1;
                    compress_array = TRUE;
                }


            }
        }

        //TODO неэффективно
        if (compress_array)
        {
            compress_array = FALSE;
            for (i = 0; i < nfds; i++)
            {
                if (fds[i].fd == -1)
                {
                    for(j = i; j < nfds; j++)
                    {
                        fds[j].fd = fds[j+1].fd;
                    }
                    i--;
                    nfds--;
                }
            }
        }
    }
}

int
main(int argc, char **argv)
{
    int listen_port = PORT;

    if (argc > 1)
    {
        listen_port = atoi(argv[1]);
        if (listen_port <=0 || listen_port > 65535){
        fprintf(stderr, "Invalid listen_port '%s'\n", argv[1]);
        return 1;
    }

    run(listen_port);
    return 0;
}