#include <stdio.h>
#include <xmlcore.h>
#include <xil_printf.h>
#include <xparameters.h>
#include "xuartps.h"
#include <math.h>
#include <xtime_l.h>

#include "uwin.h"
#include "uwout.h"
#include "input.h"
#define I 21
#define H 51
#define O 2

/* for minidataset
#include "weightin.h"
#include "weightout.h"
#define I 166
#define H 181
#define O 2

*/

//timer thingi


#define UART_DEVICE_ID XPAR_PS7_UART_1_DEVICE_ID

float *inpHW = (float *) 0x42000000;
float *resHW = (float *) 0x40000000;

XMlcore doml;
XMlcore_Config *doml_cfg;

XUartPs Uart_Ps; /* The instance of the UART Driver */
XUartPs_Config *uart_cfg;

unsigned int float_to_u32(float val){
	unsigned int result;
	union float_bytes {
		float v;
		unsigned char bytes[4];
	}data;
	data.v = val;

	result = (data.bytes[3] << 24) + (data.bytes[2]<<16) + (data.bytes[1]<<8) + (data.bytes[0]);
	return result;
}


void init_mlCore(){
	int status = 0;
	doml_cfg = XMlcore_LookupConfig(XPAR_MLCORE_0_DEVICE_ID);
	if(doml_cfg){
		status = XMlcore_CfgInitialize(&doml,doml_cfg);
		if(status != XST_SUCCESS)
			printf("failed to initialize\n");
	}
}

float sigmoid(float x){
	return 1/(1+  exp(-x)  );
}
//software version
void mlcore(float inp[I],float res[O]){
	int j,k;
		float c[1][H];

		float output[1][O];
		XTime tStart,tStop;

			//initializing to zero
	/*
			for(j = 0;j<H;j++)
				c[0][j] = 0;


			for(j = 0;j<O;j++)
				output[0][j] = 0;


	*/
		XTime_GetTime(&tStart);

		//first layer
			for(j = 0;j< H;j++){
				c[0][j] = 0;
				for(k = 0;k<I;k++)
					c[0][j] += inp/*ut[0]*/[k] * wi[k][j];
				c[0][j] = sigmoid(c[0][j]);
				//printf("c:%2.5f \n",c[i][j]);
			}
		//second layer
			for(j = 0;j< O;j++){
				output[0][j] = 0;
				for(k = 0;k<H;k++)
					output[0][j] += c[0][k] * wo[k][j];
				output[0][j] = sigmoid(output[0][j]);
				res[j] = output[0][j];
				//printf("output:%2.5f \n",output[i][j]);
			}
			XTime_GetTime(&tStop);
		    printf("Output took %llu clock cycles.\n", 2*(tStop - tStart));
		    printf("Software output took %.2f us.\n",1.0 * (tStop - tStart) / (COUNTS_PER_SECOND/1000000));
			printf("result: %f %f \n\n\n\r",res[0],res[1]);

			//return 0;

}

void menu(){
	XTime tStart,tStop;


	float z[1][I] = {1,1,0,1,0,0,0,1,0,1,1,0,1,0,0,0,0,0,0,0,0};

	//scanf("%s",a);
	/*
	for(int k = 0; k<I;k++)
		scanf("%f",&a[k]);

	for(int k = 0; k<I;k++){
			z[0][k]= a[k];
	}
	*/
	XTime_GetTime(&tStart);

	//printf("%s\n",a);
	for(int i = 0;i <I;i++)
		inpHW[i] = float_to_u32(z[0][i]);

	//hardware
	XMlcore_Start(&doml);
	//while(!XMlcore_IsReady(&doml));
	while(!XMlcore_IsDone(&doml));
	while(!XMlcore_IsIdle(&doml));
	XTime_GetTime(&tStop);
    printf("Output took %llu clock cycles.\n", 2*(tStop - tStart));
    printf("Hardware output took %.2f us.\n",1.0 * (tStop - tStart) / (COUNTS_PER_SECOND/1000000));
	printf("result: %f %f \n\n\n\r",resHW[0],resHW[1]);


} // menu()

int main()
{
	init_mlCore();
	printf("test new \n ");

	//float input[I] = {0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,1,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0}; //mbenignware
	float resa[O];

	for(int i = 0;i <I;i++)
		inpHW[i] = float_to_u32(input[0][i]);

	//software
	mlcore(input[0],resa);



	/*
	//hardware
	XMlcore_Start(&doml);
	//while(!XMlcore_IsReady(&doml));
	while(!XMlcore_IsDone(&doml));
	while(!XMlcore_IsIdle(&doml));


	printf("Hardware: %f %f \n\n",resHW[0],resHW[1]);
	*/

//while(true)
	//{

	menu();
	//}

	return 0;
}


