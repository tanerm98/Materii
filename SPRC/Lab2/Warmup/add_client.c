/*
 * This is sample code generated by rpcgen.
 * These are only templates and you can use them
 * as a guideline for developing your own functions.
 */

#include "add.h"

int main(int argc, char *argv[]) {
	int i;
	CLIENT *cl;
	prime_result *result;
	prime_request request;

	if (argc != 4){
		printf("usage: %s host min max\n", argv[0]);
		exit(1);
	}

	cl = clnt_create("localhost", PRIMEPROG, PRIMEVERS, "tcp");
	if (cl == NULL) {
		clnt_pcreateerror(argv[1]);
		exit(2);
	}

	request.min = atoi(argv[2]);
    request.max = atoi(argv[3]);

    result = find_primes_1(&request, cl);
    if (result == NULL){
	    clnt_perror(cl, argv[1]);
	    exit(3);
    }

    for (i = 0; i < result->array.array_len; i++) {
        printf("%d is prime\n", result->array.array_val[i]);
    }

    printf("count of primes found = %d\n",result->array.array_len);

//    xdr_free(xdr_prime_result, result);
    clnt_destroy(cl);

	return 0;
}
