
struct prime_request{
	int a;
	int b;
};

struct prime_result{
	int sum;
};

program PRIMEPROG{
	version PRIMEVERS{
		prime_result FIND_PRIMES(prime_request) = 1;
	} = 1;
} = 0x32345678;