#include    <sys/socket.h>  /* basic socket definitions */
#include    <time.h>        /* old system? */
#include    <netinet/in.h>  /* sockaddr_in{} and other Internet defns */
#include    <arpa/inet.h>   /* inet(3) functions */
#include    <errno.h>
#include    <fcntl.h>       /* for nonblocking */
#include    <stdio.h>
#include    <stdlib.h>
#include    <poll.h>
#include    <netdb.h>
#include    <strings.h>
#include	<Python.h>
#define _POSIX_SOURCE
#include <math.h>
#include <float.h>
#include <string.h>
#include <unistd.h>

#define MAXLINE 1024
#ifndef OPEN_MAX
#define OPEN_MAX 255
#endif
#define LISTENQ 1024
#define SERV_PORT 2707

int main(int argc, char **argv) {
	int					i, maxi, listenfd, connfd, sockfd, j, k;
	int					nready;
	ssize_t				n;
	char				line[MAXLINE];
	socklen_t			clilen;
	struct pollfd		client[OPEN_MAX];
	struct sockaddr_in	cliaddr, servaddr;
	char				*token, *cmd;
	PyObject *pName, *pModule, *addPath, *regUser, *viewData, *pFunc;
    PyObject *pArgs, *pValue;
    setbuf(stdout, NULL);
    Py_Initialize();
    pName = PyString_FromString("network");
    pModule = PyImport_Import(pName);
    Py_DECREF(pName);
    if (pModule != NULL) {
		//addPath  = PyObject_GetAttrString(pModule, "add_path");
		addPath  = PyObject_GetAttrString(pModule, "add_path");
		regUser  = PyObject_GetAttrString(pModule, "register");
		viewData = PyObject_GetAttrString(pModule, "view_user");
    	if (addPath && PyCallable_Check(addPath) &&
    		regUser && PyCallable_Check(regUser) &&
    		viewData && PyCallable_Check(viewData)) {

			listenfd = socket(AF_INET, SOCK_STREAM, 0);

			bzero(&servaddr, sizeof(servaddr));
			servaddr.sin_family      = AF_INET;
			servaddr.sin_addr.s_addr = htonl(INADDR_ANY);
			servaddr.sin_port        = htons(SERV_PORT);

			bind(listenfd, (struct sockaddr*) &servaddr, sizeof(servaddr));

			listen(listenfd, LISTENQ);

			client[0].fd = listenfd;
			client[0].events = POLLRDNORM;
			for (i = 1; i < OPEN_MAX; i++) client[i].fd = -1;
			maxi = 0;
			for (;;) {
				nready = poll(client, maxi+1, -1);
				if (client[0].revents & POLLRDNORM) {/* new client connection */
					clilen = sizeof(cliaddr);
					connfd = accept(listenfd, (struct sockaddr *) &cliaddr, &clilen);
					for (i = 1; i < OPEN_MAX; i++)
						if (client[i].fd < 0) {
							client[i].fd = connfd;	/* save descriptor */
							break;
						}
					if (i == OPEN_MAX)
						printf("too many clients\n");

					client[i].events = POLLRDNORM;
					if (i > maxi)
						maxi = i;				/* max index in client[] array */

					if (--nready <= 0)
						continue;				/* no more readable descriptors */
				}

				for (i = 1; i <= maxi; i++) {	/* check all clients for data */
					if ( (sockfd = client[i].fd) < 0)
						continue;
					if (client[i].revents & (POLLRDNORM | POLLERR)) {
						memset(line, 0, MAXLINE);
						if ( (n = recvfrom(sockfd, line, MAXLINE, 0, (struct sockaddr *) &cliaddr, &clilen)) < 0) {
							if (errno == ECONNRESET) {
								/*connection reset by client */
								close(sockfd);
								client[i].fd = -1;
							} else
								printf("readline error\n");
						} else if (n == 0) {
							/*connection closed by client */
							close(sockfd);
							client[i].fd = -1;
						} else if (n > 1) {
							if (strstr(line, "quit") != NULL)
							{
								sendto(sockfd, "bye, bye!\n", 10, 0, (struct sockaddr *) &cliaddr, sizeof(cliaddr));
								close(sockfd);
								client[i].fd = -1;
							} else {
								cmd = strtok(line, " \r\n");
								if (strcmp(cmd, "add") == 0){
									pFunc = addPath;
									n = 2;
								} else if (strcmp(cmd, "register") == 0) {
									pFunc = regUser;
									n = 1;
								} else if (strcmp(cmd, "view") == 0) {
									pFunc = viewData;
									n = 3;
								} else if (strcmp(cmd, "Question") == 0) {
									sendto(sockfd, "42\n", 3, 0, (struct sockaddr *) &cliaddr, sizeof(cliaddr));
									continue;

								}else {
									sendto(sockfd, "Bad command\n", 12, 0, (struct sockaddr *) &cliaddr, sizeof(cliaddr));
									continue;
								}
								pArgs = PyTuple_New(n);
								for (j = 0; j < n; j++) {
									token = strtok(NULL, " \r\n");
									if (token) {
										pValue = PyString_FromString(token);
										if (pValue) {
											PyTuple_SetItem(pArgs, j, pValue);
											token = NULL;
											continue;
										}
									}
									break;
								}

								for (k = j; k < n; k++)
									PyTuple_SetItem(pArgs, k, Py_None);

								pValue = PyObject_CallObject(pFunc, pArgs);
								Py_DECREF(pArgs);
								if (pValue) {
    								char *s = PyString_AsString(pValue);
									sendto(sockfd, s, strlen(s), 0, (struct sockaddr *) &cliaddr, sizeof(cliaddr));

								} else {
									sendto(sockfd, "Error\n", 6, 0, (struct sockaddr *) &cliaddr, sizeof(cliaddr));
								}
							}
						}

						if (--nready <= 0)
							break;				/* no more readable descriptors */
					}
				}
			}
		}
	}else {
        PyErr_Print();
        return 1;
    }
	Py_Finalize();
	return 0;
}