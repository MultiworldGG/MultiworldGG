#!/bin/bash

./testsuite.sh 2 vanilla > results.txt 2> errors.txt
./testsuite.sh 5 basic 1 >> results.txt 2>> errors.txt
./testsuite.sh 5 basic 2 >> results.txt 2>> errors.txt
./testsuite.sh 5 basic 3 >> results.txt 2>> errors.txt
./testsuite.sh 10 crossed 1 >> results.txt 2>> errors.txt
./testsuite.sh 10 crossed 2 >> results.txt 2>> errors.txt
./testsuite.sh 10 crossed 3 >> results.txt 2>> errors.txt