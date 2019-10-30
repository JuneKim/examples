#include <string.h>
#include <stdio.h>
#include <stdlib.h>

static unsigned char _calculate_csum(unsigned char *parsed_msg, int len)
{
    unsigned char csum = 0x0;

    for (;len > 0; len--) {
        csum += *parsed_msg++;
    }

    return 0xFF - csum;
}

int main()
{
	char msg[] = "$MTD,0,20,30<";
	unsigned char *start = strchr(msg, '$');
	unsigned char *end = strchr(msg, '<');
	unsigned char csum = _calculate_csum(start + 1, end - start - 4);
	unsigned char recv_csum = strtol(end - 2, NULL, 16);

	printf("cal[0x%x] vs recv[0x%x]\n", csum, recv_csum);

	return 0;
}
