#include <stdio.h>
#include <math.h>
#include "input.h"
/* this is for macro dataset */
#include "uwin.h"
#include "uwout.h"
#define I 21
#define H 51
#define O 2

/* this is for mini dataset
#include "weightin.h"
#include "weightout.h"
#define I 166
#define H 181
#define O 2
*/

float sigmoid(float x){
	return 1/(1+exp(-x));
}


int main(){
	int i,j,k;
	/*float wi[I][H] = {{-26.10358188 , -1.29695116 ,  1.63924277 ,  0.60541821 ,  4.89508298  , -0.86717864 },
				 {-25.07003169 , -0.374077  ,   0.35889264 ,  2.6561695  ,  6.17836236  , -1.50447126},
				 {47.38150408  ,  -0.65023365 ,  0.79413649 , -5.29996176 , -11.40776078 ,  -0.77544805},
				 {-23.38160837 , -0.93217123  , -1.76122653 ,  1.55934721  , 3.56837802 ,   0.17770462}};

	float wo[H][O] = {{-4.55514845, -3.65390281,  3.66980762},{-1.97919096,  0.57353846, -1.88925239}, {-5.85737392,  1.39218831, -1.38577587}
			   ,{ 9.31296445, -8.58462589, -4.36471466},{ 1.49031218 , 2.20566146, -2.26111594},{-1.43212691, -0.29205873,  0.99511218}};

	float input[1][I] ={6.0      ,     2.7  ,          5.1      ,     1.6  }; //{4.6    ,       3.4       ,     1.4      ,     0.3}; // {7.2 , 3.2  , 6.0  ,  1.8}; //   Iris-virginica
	*/

	//float input[1][I] = {1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}; //malware

	float c[1][H];

	float output[1][O];

	//initializing to zero
	for(i = 0;i< 1;i++)
		for(j = 0;j<H;j++)
			c[i][j] = 0;

	for(i = 0;i< 1;i++)
		for(j = 0;j<O;j++)
			output[i][j] = 0;



	//first layer
	for(i = 0;i < 1;i++)
		for(j = 0;j< H;j++){
			for(k = 0;k<I;k++)
				c[i][j] += input[i][k] * wi[k][j];
			c[i][j] = sigmoid(c[i][j]);
			//printf("c:%2.5f \n",c[i][j]);
		}
	//second layer
	for(i = 0;i < 1;i++)
		for(j = 0;j< O;j++){
			for(k = 0;k<H;k++)
				output[i][j] += c[i][k] * wo[k][j];
			output[i][j] = sigmoid(output[i][j]);
			printf("output:%2.5f \n",output[i][j]);
		}

}
