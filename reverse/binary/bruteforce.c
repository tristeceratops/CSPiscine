#include <stdlib.h>
#include <string.h>

char *incrementString(char *str, int size)
{
	char *cpy = str;
	int i = size - 1;

	while (i >= 0)
	{
		if (str[i] != 255)
		{
			cpy[i]++;
			return cpy;
		}
		i--;
	}
	return str;
}


int main(int argc, char **argv)
{
	if (argc != 2)
		return 0;
/*
	int maxlen = 5;
	int len = 1;
	char *str = malloc((maxlen + 1) * sizeof(char));
	strcat(str, "");
	while (len <= maxlen)
	{
		
	}
*/
	system(argv[1]);
}
