#include <stdio.h>
#include <dir.h>

const char conf_path[] = "C:\\FDOS\\wattcp.cfg";

int main()
{
	char ip[256], netmask[256], gateway[256];

	printf("Welcome to RuCTFE 2014 DOS!\n\n");

	ffblk entry;
   if (findfirst(conf_path, &entry, 0) == 0)
   {
   	printf("Network is already configured!\n");
      return 0;
   }

	printf("Please enter your team number: ");

   int team_number;
   char buffer[256];
   while (true)
   {
   	fgets(buffer, sizeof(buffer), stdin);
   	if (sscanf(buffer, "%d", &team_number) != 1 || team_number < 0 || team_number > 767)
      	printf("\nPlease enter a number between 0 and 767: ");
      else
      	break;
	}

   sprintf(ip, "my_ip = 10.%d.%d.2\n", team_number / 256 + 60, team_number % 256);
   sprintf(netmask, "netmask = 255.255.255.0\n");
   sprintf(gateway, "gateway = 10.%d.%d.1\n", team_number / 256 + 60, team_number % 256);

   printf("\n\nYour network settings:\n");
   printf(ip);
   printf(netmask);
   printf(gateway);

   FILE *file = fopen(conf_path, "w");
   if (!file)
   {
   	printf("Failed to open config file!\n");
      return 1;
   }
   fputs(ip, file);
   fputs(netmask, file);
   fputs(gateway, file);
   fclose(file);
}