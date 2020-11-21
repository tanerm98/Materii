const MAXBUF = 1000;

struct sensor_data {
	int data_id;
	int no_values;
	float array<MAXBUF>;
};

struct statistics {
	int min;
	int max;
	int avg;
	int med;
};

struct package{
	int id;
	unsigned hyper token;

	string command<>;
    string message<>;

    struct sensor_data data;
    struct statistics stats;
};

program RPCDBPROG{
	version RPCDBVERS{
		package COMMAND(package) = 1;
	} = 1;
} = 0x32345678;