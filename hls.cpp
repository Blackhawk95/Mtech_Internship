#include <hls_math.h>
#include <stdio.h>
//for micro_dataset
#include "uwin.h"
#include "uwout.h"
#define I 21
#define H 51
#define O 2

/* for mini_dataset
#include "weightin.h"
#include "weightout.h"
#define I 166
#define H 181
#define O 2
*/

float sigmoid(float x){
	return 1/(1+  hls::expf(-x)  );
}


void mlcore(float inp[I],float res[O]){
#pragma HLS INTERFACE s_axilite port=return bundle=CRTL_BUS
#pragma HLS INTERFACE bram port=res
#pragma HLS INTERFACE bram port=inp
	int i,j,k;
	float c[1][H];

	float output[1][O];

		//initializing to zero
		/*
		for(j = 0;j<H;j++)
			c[0][j] = 0;


		for(j = 0;j<O;j++)
			output[0][j] = 0;
		*/


	//first layer

		for(j = 0;j< H;j++){
			//#pragma HLS PIPELINE
			c[0][j] = 0;
			for(k = 0;k<I;k++){
				#pragma HLS PIPELINE
				c[0][j] += inp/*ut[0]*/[k] * wi[k][j];
			}
			c[0][j] = sigmoid(c[0][j]);
			//printf("c:%2.5f \n",c[i][j]);
		}



	//second layer
		for(j = 0;j< O;j++){
			//#pragma HLS PIPELINE
			output[0][j] = 0;
			for(k = 0;k<H;k++){
				#pragma HLS PIPELINE
				output[0][j] += c[0][k] * wo[k][j];
			}
			output[0][j] = sigmoid(output[0][j]);
			res[j] = output[0][j];
			//printf("output:%2.5f \n",output[i][j]);
		}
		//return 0;
}

