const MAXPRIMES = 1000;

struct prime_request{
	int min;
	int max;
};

struct prime_result{
	int array<MAXPRIMES>;
};

program PRIMEPROG{
	version PRIMEVERS{
		prime_result FIND_PRIMES(prime_request) = 1;
	} = 1;
} = 0x32345678;