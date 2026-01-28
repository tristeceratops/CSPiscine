#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void ok(void)
{
	puts("Good job.");
}

void no(void)
{
	puts("Nope.");
	exit(1);
}

int main(void)
{
    char input[64];
    char out[9];
    char tmp[4];
    int i, j;

    printf("Enter key: ");

    if (scanf("%63s", input) != 1)
        no();

    if (input[0] != '0')
        no();
    if (input[1] != '0')
        no();

    fflush(stdout);

    memset(out, 0, sizeof(out));
    out[0] = 'd';

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

    if (strcmp(out, "delabere") == 0)
        ok();
    else
        no();

    return 0;
}

