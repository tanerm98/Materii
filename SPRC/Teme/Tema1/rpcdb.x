
struct sensor_data {
	int data_id;
	int no_values;
	float *values;
};

struct statistics {
	int min;
	int max;
	int avg;
	int med;
};

struct package {
	int id;
	unsigned long token;
	string message<>;
	struct sensor_data data;
	struct statistics stats;
};

program RPCDBPROG{
	version RPCDBVERS{
		package LOGIN(package) = 1;
		package LOGOUT(package) = 1;
		package ADD(package) = 1;
		package UPDATE(package) = 1;
		package DEL(package) = 1;
		package READ(package) = 1;
		package GET_STAT(package) = 1;
		package GET_STAT_ALL(package) = 1;
		package LOAD() = 1;
		package STORE() = 1;
	} = 1;
} = 0x31234567;