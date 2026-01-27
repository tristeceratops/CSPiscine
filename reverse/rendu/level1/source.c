#include <string.h>
#include <stdio.h>


int main(int argc, char **argv)
{
	char *password = "__stack_check";
	char answer[119];

	printf("Please enter key: ");
	scanf("%s", answer);
	if (!strcmp(password, answer))
	{
		printf("Good job.\n");
	}
	else
	{
		printf("Nope.\n");
	}
	return 0;
}
