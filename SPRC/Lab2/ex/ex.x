
struct student{
	string nume<>;
	string grupa<>;
};

struct rezultat {
	string s<rezultat>;
};

program CHECKPROG{
	version CHECKVERS{
		rezultat GRADE(student) = 1;
	} = 1;
} = 0x31234567;