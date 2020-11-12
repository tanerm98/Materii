#!/bin/bash

mkdir -p files
for i in $(seq 1 100); do
	chunk=10
	base64 /dev/urandom | head -c ${chunk} > files/f${i}
done
