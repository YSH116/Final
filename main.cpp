#include "mbed.h"
#include "bbcar.h"
#include "bbcar_rpc.h"

Ticker servo_ticker;

PwmOut pin5(D5), pin6(D6);
// DigitalInOut pin11(D11);
BufferedSerial uart(D10, D9);
BufferedSerial xbee(D1, D0);
BBCar car(pin5, pin6, servo_ticker);

int main() {
    uart.set_baud(9600);
    char buf[256], outbuf[256];
    FILE *devin = fdopen(&uart, "r");
    FILE *devout = fdopen(&uart, "w");

    while (1) {
        // parallax_ping  ping(pin11);
        // printf("dis = %f\n", (float)ping);
        
        memset(buf, 0, 256);
        for( int i = 0; ; i++ ) {
            char recv = fgetc(devin);
            buf[i] = fputc(recv, devout);
            if (buf[0] == 'K') {
                xbee.write("K\n", 3);
            }
            if (recv == '\n') {
                printf("\r\n");
                break;
            }
        }
        printf("%s\n",buf);
        RPC::call(buf, outbuf);
        
        // if((float)ping < 10) {
        //     car.stop();
        //     printf("distance = %f\n", (float)ping);
        // }
    }
}