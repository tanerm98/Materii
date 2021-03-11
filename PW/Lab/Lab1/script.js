// ex 2
console.log("hello world!");

// ex 3
var d = new Date();
console.log(d);

// ex 4
var v = [];
for (i = 0; i < 101; i++) {
	v.push(i);
}
console.log(v.filter(x => x % 2 == 0));

// ex 5
const afisare = (arr, index) => console.log(arr[index]);
function myFunc (arr, index, functie) {
	functie(arr, index);
}
myFunc(v, 50, afisare);

// ex 6
const stai2SecundeBoss = () => console.log("Am stat 2 secunde");

const getAgePromise = new Promise((resolve, reject) => {
    setTimeout(function () {resolve(25);}, 2000);
});
getAgePromise.then((age) => console.log(`My age is ${age}`));

const getAgeAsync = () => new Promise((resolve, reject) => {
    setTimeout(function () {resolve(25);}, 2000);
});
const asinc = async () => {
    const age = await getAgeAsync();
    console.log(`My age is ${age}`);
}
asinc();