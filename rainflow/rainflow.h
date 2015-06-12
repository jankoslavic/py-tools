/********************************************************************
 * fatigue.h Fatigue related functions.
 *
 * Name:        fatigue.h
 * Purpose:     Fatigue analysis
 * Copyright:   (c) 2007-2008 Ladisk <www.fs.uni-lj.si/ladisk>
 * Author:      Primoz Cermelj <primoz.cermelj@gmail.com>
 * License:     BSD license
 *********************************************************************/
#include <math.h>
#include <stdlib.h>
#include <stdio.h>

int rf3(double *array_ext, int nr, double *array_out);
int rf5(double *array_ext, int nr, double *array_t, double *array_out);
int sig2ext(double *sig, double *time_sig, long n, int clsn,
            double *ext, double *exttime);
double arr_min(double *sig, int n, int *pos);
double arr_max(double *sig, int n, int *pos);
#define NNEW(a,b) (a *)calloc((b),sizeof(a))
#define RENEW(a,b,c) a=(b *) realloc((b *)(a),(c)*sizeof(b))
double *diff(double *vec, int n);
int repl(double *x, int *filt, int n, double *x_repl);
