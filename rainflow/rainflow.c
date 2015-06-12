/********************************************************************
 * Copyright:   (c) 2007-2008 Ladisk <www.fs.uni-lj.si/ladisk>
 * Author:      Primoz Cermelj <primoz.cermelj@gmail.com>
 *********************************************************************/
#include "rainflow.h"


/*-------------------------------------------------------------
 * rf3
 *
 * Performs rainflow analysis without time analysis and returns
 * the actual number of rows in the output rf matrix - the
 * actual size of the data in array_out is (Nr x 3).
 *
 * Based on Adam Nieslony's rainflow.c for Matlab.
 *-------------------------------------------------------------*/
int rf3(double *array_ext,	// (in) an array of turning points (see sig2ext on how to get these)
		int nr,				// (in) length of the array_ext (number of rows of the vector)
		double *array_out)	// (out) output matrix of size nr x 3; the columns are:
							// 		cycles amplitude, cycles mean value, number of
							// 		cycles (0.5 or 1.0). This array must be allocated
							// 		apriori.
{
  double a[512], ampl, mean;
  int index, j, cNr, tot_num;

  tot_num = nr;

  // Init array_out to zero
  for (index=0; index<nr*3; index++) {
    array_out[index] = 0.0;
  }

  j = -1;
  cNr = 1;
  for (index=0; index<tot_num; index++) {
    a[++j]=*array_ext++;
    while ( (j >= 2) && (fabs(a[j-1]-a[j-2]) <= fabs(a[j]-a[j-1])) ) {
      ampl = fabs( (a[j-1]-a[j-2])/2 );
      switch(j){
        case 0: { break; }
        case 1: { break; }
        case 2: {
          mean=(a[0]+a[1])/2;
          a[0]=a[1];
          a[1]=a[2];
          j=1;
          if (ampl > 0) {
            *array_out ++= ampl;
            *array_out ++= mean;
            *array_out ++= 0.50;
          }
          break;
        }
        default: {
          mean = (a[j-1]+a[j-2])/2;
          a[j-2] = a[j];
          j = j-2;
          if (ampl > 0) {
            *array_out ++= ampl;
            *array_out ++= mean;
            *array_out ++= 1.00;
            cNr++;
          }
          break;
        }
      }
    }
  }
  for (index=0; index<j; index++) {
    ampl = fabs(a[index]-a[index+1])/2;
    mean = (a[index]+a[index+1])/2;
    if (ampl > 0){
      *array_out ++= ampl;
      *array_out ++= mean;
      *array_out ++= 0.50;
    }
  }

  return (tot_num - 1 - cNr);
}


/*-------------------------------------------------------------
 * rf5
 *
 * Performs rainflow analysis with time analysis.
 *
 * Inputs:
 *      array_ext   an array of turning points (see sig2ext on how to get these)
 *      nr          length of the array_ext and  number of rows in array_out
 *      array_t     an array of time values
 *
 * Outputs:
 *      cnr         the actual number of rows in the rf matrix
 *      array_out   matrix of length nr x 5 where the result will be returned;
 *                  this array must be pre-allocated apriori.
 *
 * Based on Adam Nieslony's rainflow.c for Matlab.
 *-------------------------------------------------------------*/
int rf5(double *array_ext, int nr, double *array_t, double *array_out){
  double a[512], t[512], ampl, mean, period, atime;
  int index, j, cNr, tot_num;

  tot_num = nr;

  // Init array_out to zero
  for (index=0; index<nr*5; index++) {
    array_out[index] = 0.0;
  }

  j = -1;
  cNr = 1;
  for (index=0; index<tot_num; index++) {
    a[++j]=*array_ext++;
    t[j]=*array_t++;
    while ( (j >= 2) && (fabs(a[j-1]-a[j-2]) <= fabs(a[j]-a[j-1])) ) {
      ampl=fabs( (a[j-1]-a[j-2])/2 );
      switch(j) {
        case 0: { break; }
        case 1: { break; }
        case 2: {
          mean=(a[0]+a[1])/2;
          period=(t[1]-t[0])*2;
          atime=t[0];
          a[0]=a[1];
          a[1]=a[2];
          t[0]=t[1];
          t[1]=t[2];
          j=1;
          if (ampl > 0) {
            *array_out++=ampl;
            *array_out++=mean;
            *array_out++=0.50;
            *array_out++=atime;
            *array_out++=period;
          }
          break;
        }
        default: {
          mean=(a[j-1]+a[j-2])/2;
          period=(t[j-1]-t[j-2])*2;
          atime=t[j-2];
          a[j-2]=a[j];
          t[j-2]=t[j];
          j=j-2;
          if (ampl > 0) {
            *array_out++=ampl;
            *array_out++=mean;
            *array_out++=1.00;
            *array_out++=atime;
            *array_out++=period;
            cNr++;
          }
          break;
        }
      }
    }
  }
  for (index=0; index<j; index++) {
    ampl=fabs(a[index]-a[index+1])/2;
    mean=(a[index]+a[index+1])/2;
    period=(t[index+1]-t[index])*2;
    atime=t[index];
    if (ampl > 0){
      *array_out++=ampl;
      *array_out++=mean;
      *array_out++=0.50;
      *array_out++=atime;
      *array_out++=period;
    }
  }

  return (tot_num - 1 - cNr);
}


/*-------------------------------------------------------------
 * sig2ext
 *
 * Searches local extrema from time course (signal) sig.
 *
 * Inputs:
 *      sig         an array of n time points
 *      time_sig    an array of n delta time points (pass NULL if this array
 *                  is to be assumed in the form of 0, 1, 2,....)
 *      n           number of points (sig, time_sig)
 *      clsn        number of classes (pass -1 if not to be used, i.e., no
 *                  divisions into classes)
 *      ext         (output) extrema found on sig
 *      exttime     (output) time values corresponding to ext;
 *                  if time was NULL, a dt=1 is assumed.
 * Outputs:
 *      np          number of extrema (number of points on the output)
 *
 * Based on Adam Nieslony's sig2ext.m (Matlab function).
 *-------------------------------------------------------------*/
int sig2ext(double *sig, double *time_sig, long n, int clsn,
            double *ext, double *exttime){
    int i, have_time = 0;
    double smax, smin;
    double *w1;
    int *w;
    int np;

    if (time_sig != NULL){
        have_time = 1;
    }
    if (clsn != -1){
        clsn--;
        smax = arr_max(sig, n, NULL);
        smin = arr_min(sig, n, NULL);
        for (i=0; i<n; i++){
            sig[i] = round((sig[i]-smin)*clsn/(smax-smin))*(smax-smin)/clsn + smin;
        }
    }

    if (have_time != 1){
        time_sig = NNEW(double, n);
        for (i=0; i<n; i++){
            time_sig[i] = i;
        }
    }

    w = NNEW(int, n);
    w1 = diff(sig, n);
    for (i=1; i<n; i++){
        if (w1[i-1]*w1[i] <= 0) w[i] = 1;
    }
    w[0] = 1;
    w[n-1] = 1;
    np = repl(ext, w, n, sig);
    np = repl(exttime, w, n, time_sig);

    free(w1);
    RENEW(w, int, np);
    w1 = diff(ext, np);
    for (i=1; i<np; i++){
        if (!(w1[i-1]==0 && w1[i]==0)) w[i] = 1;
    }
    w[0] = 1;
    w[np-1] = 1;
    np = repl(ext, w, np, ext);
    np = repl(exttime, w, np, exttime);

    for (i=1; i<np; i++){
        if (ext[i-1] != ext[i]) w[i] = 1;
    }
    w[0] = 1;
    np = repl(ext, w, np, ext);
    RENEW(w1, double, np-1);
    for (i=0; i<np-1; i++){
        w1[i] = 0.5*( exttime[i+1] - exttime[i]);
        exttime[i] = exttime[i] + w1[i]*(!w[i+1]);
    }
    np = repl(exttime, w, np, exttime);

    if (np > 2){
        free(w1);
        RENEW(w, int, np);
        w1 = diff(ext, np);
        for (i=1; i<np; i++){
            if (w1[i-1]*w1[i] < 0) w[i] = 1;
        }
        w[0] = 1;
        w[np-1] = 1;
        np = repl(ext, w, np, ext);
        np = repl(exttime, w, np, exttime);
    }

    free(w1);
    free(w);
    if (have_time != 1) free(time_sig);

    return np;
}

/*-------------------------------------------------------------
 * arr_min
 *
 * Returns minimum of a double vector. If the pos is given as a
 * non-NULL pointer, the position of the min value is returned
 * as well.
 *-------------------------------------------------------------*/
double arr_min(double *sig, int n, int *pos){
    int i, ind=0;

    double min_val = sig[0];
    for (i=1; i<n; i++){
        if (sig[i] < min_val){
            min_val = sig[i];
            ind = i;
        }
    }
    if (pos != NULL) *pos = ind;
    return min_val;
}


/*-------------------------------------------------------------
 * arr_max
 *
 * Returns maximum of a double vector. If the pos is given as a
 * non-NULL pointer, the position of the max value is returned
 * as well.
 *-------------------------------------------------------------*/
double arr_max(double *sig, int n, int *pos){
    int i, ind=0;

    double max_val = sig[0];
    for (i=1; i<n; i++){
        if (sig[i] > max_val){
            max_val = sig[i];
            ind = i;
        }
    }
    if (pos != NULL) *pos = ind;
    return max_val;
}

/*-------------------------------------------------------------
 * diff
 *
 * Returns a new, dynamically allocated vector with the length
 * n-1 and values defined as:
 *      v[2]-v[1]
 *      v[3]-v[2]
 *      ....
 *
 * Make sure the vector is cleared with free when no longer
 * needed.
 *-------------------------------------------------------------*/
double *diff(double *vec, int n){
    // The length of vec_out is n-1!
    int i;
    double *vec_out;

    vec_out = NNEW(double, n-1);
    for (i=0; i<(n-1); i++){
        vec_out[i] = vec[i+1] - vec[i];
    }
    return vec_out;
}


/*-------------------------------------------------------------
 * repl
 *
 * Replaces x with x_repl where filt is 1. x and filt are of the length n
 * while x_repl can be n or greater. x is replaced inplace. It returns
 * the number of terms replaced.
 *-------------------------------------------------------------*/
int repl(double *x, int *filt, int n, double *x_repl){
    int i, j;
    j = 0;
    for (i=0; i<n; i++){
        if (filt[i] > 0){
            x[j] = x_repl[i];
            j++;
        }
    }
    return j;
}