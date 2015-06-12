gcc -c sample.c
gcc -shared -o sample.dll sample.o -Wl,--out-implib,libsample.a