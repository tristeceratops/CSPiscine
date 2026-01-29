#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void)
{
    char input[64];
    char out[9];
    char tmp[4];
    int i, j;

    printf("Enter key: ");

    if (scanf("%63s", input) != 1)
    {
	    printf("Nope!\n");
	    exit(1);
    }

    if (input[0] != '4')
    {
	    printf("Nope!\n");
	    exit(1);
    }
    if (input[1] != '2')
    {
	    printf("Nope!\n");
	    exit(1);
    }

    fflush(stdout);

    memset(out, 0, sizeof(out));
    out[0] = '*';

    i = 2;
    j = 1;

    while (strlen(out) < 8 && i < (int)strlen(input))
    {
        tmp[0] = input[i];
        tmp[1] = input[i + 1];
        tmp[2] = input[i + 2];
        tmp[3] = '\0';

        out[j] = (char)atoi(tmp);

        i += 3;
        j += 1;
    }

    out[j] = '\0';

    if (strcmp(out, "********") == 0)
        printf("Good job.\n");
    else
        printf("Nope.\n");

    return 0;
}
