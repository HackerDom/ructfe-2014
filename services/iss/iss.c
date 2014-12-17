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

#define BACKLOG_LEN 1024
#define IN_BUFFER_LEN 128
#define OUT_BUFFER_LEN 128
#define SOCKETS_COUNT 1 + BACKLOG_LEN

#define TRUE 1
#define FALSE 0

#define MAX_PENALTY 2

struct node
{
    struct node *A_child;
    struct node *T_child;
    struct node *G_child;
    struct node *C_child;
    char *comment;
};

struct node *root;
FILE *file;

void make_non_blocking(int fd)
{
    int flags = fcntl(fd, F_GETFL, 0);
    if (fcntl(fd, F_SETFL, flags | O_NONBLOCK) < 0)
    {
        perror("fcntl() on set O_NONBLOCK failed");
        exit(-1);
    }
}

void make_blocking(int fd)
{
    int flags = fcntl(fd, F_GETFL, 0);
    if (fcntl(fd, F_SETFL, flags & ~O_NONBLOCK) < 0)
    {
        perror("fcntl() on remove O_NONBLOCK failed");
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
try_match_rec(struct node *cur, const char *dna, int penalty, char *buff)
{
    if(penalty > MAX_PENALTY)
        return FALSE;

    if(dna[0] == 0 && cur->comment != NULL)
    {
        buff[0] = ' ';
        strcpy(buff + 1, cur->comment);
        return TRUE;
    }

    if(cur->A_child != NULL)
    {
        buff[0] = 'A';
        if(dna[0] != 0 && try_match_rec(cur->A_child, dna + 1, dna[0] == 'A' ? penalty : penalty + 1, buff + 1))
            return TRUE;
        if(try_match_rec(cur->A_child, dna, penalty + 1, buff + 1))
            return TRUE;
    }
    if(cur->T_child != NULL)
    {
        buff[0] = 'T';
        if(dna[0] != 0 && try_match_rec(cur->T_child, dna + 1, dna[0] == 'T' ? penalty : penalty + 1, buff + 1))
            return TRUE;
        if(try_match_rec(cur->T_child, dna, penalty + 1, buff + 1))
            return TRUE;
    }
    if(cur->G_child != NULL)
    {
        buff[0] = 'G';
        if(dna[0] != 0 && try_match_rec(cur->G_child, dna + 1, dna[0] == 'G' ? penalty : penalty + 1, buff + 1))
            return TRUE;
        if(try_match_rec(cur->G_child, dna, penalty + 1, buff + 1))
            return TRUE;
    }
    if(cur->C_child != NULL)
    {
        buff[0] = 'C';
        if(dna[0] != 0 && try_match_rec(cur->C_child, dna + 1, dna[0] == 'C' ? penalty : penalty + 1, buff + 1))
            return TRUE;
        if(try_match_rec(cur->C_child, dna, penalty + 1, buff + 1))
            return TRUE;
    }

    buff[0] = 0;
    return dna[0] != 0 && try_match_rec(cur, dna + 1, penalty + 1, buff);
}

int
try_match(const char *dna, char *out_buff)
{
    return try_match_rec(root, dna, 0, out_buff);
}

char *
try_add_pattern(const char *pattern, char * comment)
{
    int p_len = strlen(pattern);
    int c_len = strlen(comment);
    struct node *cur = root;

    for(int i = 0; i < p_len; i++)
    {
        if(pattern[i] == 'A')
        {
            if(cur->A_child == NULL)
            {
                cur->A_child = malloc(sizeof(struct node));
                memset(cur->A_child, 0, sizeof(struct node));
            }
            cur = cur->A_child;
        }
        else if(pattern[i] == 'T')
        {
            if(cur->T_child == NULL)
            {
                cur->T_child = malloc(sizeof(struct node));
                memset(cur->T_child, 0, sizeof(struct node));
            }
            cur = cur->T_child;
        }
        else if(pattern[i] == 'G')
        {
            if(cur->G_child == NULL)
            {
                cur->G_child = malloc(sizeof(struct node));
                memset(cur->G_child, 0, sizeof(struct node));
            }
            cur = cur->G_child;
        }
        else
        {
            if(cur->C_child == NULL)
            {
                cur->C_child = malloc(sizeof(struct node));
                memset(cur->C_child, 0, sizeof(struct node));
            }
            cur = cur->C_child;
        }
    }
    if(cur->comment == NULL)
    {
        cur->comment = malloc(c_len + 1);
        memset(cur->comment, 0, c_len + 1);

        strcpy(cur->comment, comment);
        return comment;
    }
    return cur->comment;
}

int
init_state(FILE* fp)
{
    char *buffer = malloc(IN_BUFFER_LEN);
    size_t pos = 0;
    ssize_t read;

    int lines = 0;

    while ((read = fread(buffer + pos, 1, 1, fp)) > 0)
    {
        if(buffer[pos] == '\n')
        {
            buffer[pos] = 0;
            char *comment = memchr(buffer, ' ', pos);

            if(comment == NULL)
            {
                fprintf(stderr, "Corrupted state!");
                exit(-1);
            }
            comment[0] = 0;
            comment++;

            try_add_pattern(buffer, comment);
            pos = 0;
            lines++;
        }
        else
            pos++;
    }
    return lines;
}

//*************
//TODO close opened connections by timeout
//*************

//DEBUG
void
proof()
{
    printf("HACKED!\n");
}

void
run(int listen_port)
{
    const char error_msg[] = "Invalid request, must be a '\\n'-terminated line no longer than 64 chars\n";
    const char error_msg1[] = "Invalid DNA string, must contain character only from [ATGC] alphabet and have non-zero length\n";
    const char error_msg2[] = "Invalid Virus Pattern string, must be in <DNA-sequence><space><Comment> format\n";

    int len, rc, one = 1;
    int listen_sd = -1, new_sd = -1;
    int compress_array = FALSE;
    int close_conn;
    struct sockaddr_in sin;

    struct pollfd fds[SOCKETS_COUNT];
    char buffers[SOCKETS_COUNT][IN_BUFFER_LEN];
    int positions[SOCKETS_COUNT];
    char *request;

    int nfds = 1, current_size = 0, i, j;

    root = malloc(sizeof(struct node));
    memset(root, 0, sizeof(struct node));

    file = fopen("state", "a+");
    if(file == NULL)
    {
        perror("can't open state file for writing");
        exit(-1);
    }
    fseek(file, 0, SEEK_SET);
    printf("Loaded %d lines from state file\n", init_state(file));

    make_non_blocking(fileno(file));
    setvbuf(file, NULL, _IONBF, 0);

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

    char *result = malloc(OUT_BUFFER_LEN);
//DEBUG
    printf("result addr: %p\n", result);
    while (1) {
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
                continue;

            int fd = fds[i].fd;
            if (fd == listen_sd)
            {
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

                    make_non_blocking(new_sd);
                    fds[nfds].fd = new_sd;
                    fds[nfds].events = POLLIN;
                    nfds++;
                } while (new_sd != -1);
            }
            else
            {
                close_conn = FALSE;

                do
                {
                    request = buffers[i];
                    rc = recv(fd, request + positions[i], IN_BUFFER_LEN - positions[i], 0);
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
                    positions[i] += rc;

                    char *eol_pos = memchr(request, '\n', positions[i]);

                    if(eol_pos == NULL)
                    {
                        if(strnlen(request, IN_BUFFER_LEN) == IN_BUFFER_LEN)
                        {
                            memset(request, 0, sizeof(buffers[i]));
                            positions[i] = 0;

                            //TODO copypaste
                            rc = send(fd, error_msg, strlen(error_msg), 0);
                            if (rc < 0)
                            {
                                perror("    send() failed");
                                close_conn = TRUE;
                                break;
                            }
                        }
                        continue;
                    }

//-------------------PROCESSING PROTOCOL-------------------

                    len = eol_pos - request;
                    if(len > 0 && request[len-1] == '\r')
                        len--;
                    request[len] = 0;

                    char *comment = memchr(request, ' ', len);

                    if(comment == NULL)
                    {
                        if(check_alphabet(request))
                        {
                            pid_t pid = fork();
                            if(pid == -1)
                            {
                                perror("fork()");
                                exit(-1);
                            }
                            else if (pid == 0)
                            {
                                char *match = malloc(OUT_BUFFER_LEN);
                                memset(match, 0, OUT_BUFFER_LEN);

                                if(try_match(request, match))
                                    sprintf(result, "PATTERN MATCHED : %s\n", match);
                                else
                                    strcpy(result, "NO PATTERN MATCHED\n");

                                rc = send(fd, result, strlen(result), 0);
                                if (rc < 0)
                                    perror("    send() failed");

                                free(match);
                                free(result);
                                close(fd);

                                exit(0);
                            }
                        }
                        else
                        {
                            //TODO copypaste
                            rc = send(fd, error_msg1, strlen(error_msg1), 0);
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

                        if(check_alphabet(request))
                        {
                            char *result_comment = try_add_pattern(request, comment);

                            comment[-1] = ' ';
                            if(result_comment == comment)
                            {
                                fwrite(request, len, 1, file);
                                fwrite("\n", 1, 1, file);
                            }

                            sprintf(result, "%s\n", result_comment);
                            rc = send(fd, result, strlen(result), 0);

                            //TODO copypaste
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
                            rc = send(fd, error_msg2, strlen(error_msg2), 0);
                            if (rc < 0)
                            {
                                perror("    send() failed");
                                close_conn = TRUE;
                                break;
                            }
                        }
                    }
                    memset(request, 0, sizeof(buffers[i]));
                    positions[i] = 0;

                } while(TRUE);

                if (close_conn)
                {
                    close(fd);
                    fds[i].fd = -1;
                    positions[i] = 0;
                    memset(buffers[i], 0, sizeof(buffers[i]));
                    compress_array = TRUE;
                }
            }
        }

        //TODO ineffective
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
