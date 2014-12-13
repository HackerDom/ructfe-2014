extern "C" {
#include <wattcp.h>
}
#include <stdio.h>

tcp_Socket sock;

static const int port = 16742;

int main()
{
	char buffer[256];

   sock_init();
	tcp_listen(&sock, port, 0, 0, NULL, 0);
	printf("Listening on port %d...", port);
	sock_wait_established((sock_type *)&sock, 0, NULL, NULL);
	printf("Accepted client!");
   sock_gets((sock_type *)&sock, buffer, 256);
   sock_puts((sock_type *)&sock, buffer);
	sock_close((sock_type *)&sock);

   return 0;

   sock_err:
   printf("Listen failed!");
	return 1;
}