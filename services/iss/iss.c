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
#define BUFFER_LEN 64
#define SOCKETS_COUNT 4 + BACKLOG_LEN

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

int
check_alphabet(char *str)
{
    int n = strlen(str);
    if(strlen(str) == 0)
        return FALSE;
    for(int i=0; i < n; i++)
    {
        if(str[i] != 'A' && str[i] != 'T' && str[i] != 'G' && str[i] != 'C')
            return FALSE;
    }
    return TRUE;
}

int
try_match(const char * dna)
{
    return 0;
}

char *
try_add_pattern(const char *pattern, const char * comment)
{
    return NULL;
}

void
run(int listen_port)
{
    const char error_msg[] = "Invalid request, must be a '\n'-terminated line no longer than 64 chars";
    const char error_msg1[] = "Invalid DNA string, must contain character from [ATGC] alphabet and have non-zero length";
    const char error_msg2[] = "Invalid Virus Pattern string, must be in <DNA-sequence><space><Comment> format";
    char * msg;

    int len, rc, one = 1;
    int listen_sd = -1, new_sd = -1;
    int compress_array = FALSE;
    int close_conn;
    struct sockaddr_in sin;

    struct pollfd fds[SOCKETS_COUNT];
    char buffers[SOCKETS_COUNT][BUFFER_LEN];
    int positions[SOCKETS_COUNT];
    char *buffer;

    // char buffer[1024];
    int nfds = 1, current_size = 0, i, j;

    listen_sd = socket(AF_INET, SOCK_STREAM, 0);
    if (listen_sd < 0)
    {
        perror("socket() failed");
        exit(-1);
    }

    rc = setsockopt(listen_sd, SOL_SOCKET, SO_REUSEADDR, &one, sizeof(one));
    if (rc < 0)
    {
        perror("setsockopt() failed");
        exit(-1);
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

    memset(buffers, 0, sizeof(buffers));
    memset(positions, 0, sizeof(positions));

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
                // printf("cur %d, list %d\n", fds[i].fd, listen_sd);
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

                    // printf("    New incoming connection - %d\n", new_sd);

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
                    // printf("Starting recv\n");
                    buffer = buffers[i];
                    rc = recv(fds[i].fd, buffer + positions[i], BUFFER_LEN - positions[i], 0);
                    // printf("Recved %d bytes\n", rc);
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
                        printf("    Connection closed by peer\n");
                        close_conn = TRUE;
                        break;
                    }

                    len = rc;
                    printf("    %d bytes received\n", len);

                    int len = strnlen(buffer, BUFFER_LEN);
                    char *eol_pos = memchr(buffer, '\n', len);

                    if(eol_pos == NULL && len == BUFFER_LEN)
                    {
                        //TODO copypaste
                        rc = send(fds[i].fd, error_msg, strlen(error_msg), 0);
                        if (rc < 0)
                        {
                            perror("    send() failed");
                            close_conn = TRUE;
                            break;
                        }
                    }
                    else if(eol_pos == NULL)
                        continue;

//-------------------PROCESSING PROTOCOL-------------------

                    len = eol_pos - buffer;
                    if(len > 0 && buffer[len-1] == '\r')
                        len--;
                    buffer[len] = 0;

                    char *comment = memchr(buffer, ' ', len);
                    if(comment == NULL)
                    {
                        if(check_alphabet(buffer))
                        {
                            pid_t pid;
                            switch(pid=fork()) {
                            case -1:
                                perror("fork()");
                                exit(-1);
                            case 0:
                                if(try_match(buffer))
                                    msg = "MATCHED!";
                                else
                                    msg = "NO MATCH";

                                //TODO copypaste
                                rc = send(fds[i].fd, msg, strlen(msg), 0);
                                if (rc < 0)
                                {
                                    perror("    send() failed");
                                    close_conn = TRUE;
                                    break;
                                }
                            default:
                                close_conn = TRUE;
                                break;
                            }
                        }
                        else
                        {
                            //TODO copypaste
                            rc = send(fds[i].fd, error_msg1, strlen(error_msg1), 0);
                            if (rc < 0)
                            {
                                perror("    send() failed");
                                close_conn = TRUE;
                                break;
                            }
                        }
                    }
                    else
                    {
                        comment[0] = 0;
                        comment++;

                        if(check_alphabet(buffer))
                        {
                            char *existing_comment = try_add_pattern(buffer, comment);
                            if(existing_comment)
                                msg = existing_comment;
                            else
                                msg = comment;

                            //TODO copypaste
                            rc = send(fds[i].fd, msg, strlen(msg), 0);
                            if (rc < 0)
                            {
                                perror("    send() failed");
                                close_conn = TRUE;
                                break;
                            }
                        }
                        else
                        {
                            //TODO copypaste
                            rc = send(fds[i].fd, error_msg2, strlen(error_msg2), 0);
                            if (rc < 0)
                            {
                                perror("    send() failed");
                                close_conn = TRUE;
                                break;
                            }
                        }
                    }
                } while(TRUE);

                // printf("Exited recv loop\n");

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
            return -1;
        }
    }

    run(listen_port);
    return 0;
}