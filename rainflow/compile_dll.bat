gcc -c rainflow.c
gcc -shared -o rainflow.dll rainflow.o -Wl,--out-implib,librainflow.a