#include "mbed.h"
#include "bbcar.h"
#include "bbcar_rpc.h"

Ticker servo_ticker;

PwmOut pin5(D5), pin6(D6);
DigitalInOut pin10(D11);
BufferedSerial uart(D1, D0);
BufferedSerial xbee(D10, D9);
BBCar car(pin5, pin6, servo_ticker);

int main() {
    uart.set_baud(9600);
    xbee.set_baud(9600);
    char buf[256], outbuf[256];
    FILE *devin = fdopen(&uart, "r");
    FILE *devout = fdopen(&uart, "w");
    bool round = 1;
    bool ok = 1;
    parallax_ping  ping1(pin10);

    while (1) {
        printf("dis = %f\n", (float)ping1);
        if ((float)ping1 < 15 && round  && (float)ping1 > 5) {
            car.turn(100, -0.01);
            ThisThread::sleep_for(1000ms);
            car.goStraight(100);
            ThisThread::sleep_for(30ms);
            car.turn(100, 0.35);
            ThisThread::sleep_for(6000ms);
            round = 0;
            car.stop();
        }
        memset(buf, 0, 256);
        for( int i = 0; ; i++ ) {
            char recv = fgetc(devin);
            buf[i] = fputc(recv, devout);
            if (buf[0] == 'K' && ok) {
                xbee.write("K\n", 3);
                ok = 0;
            }
            if (recv == '\n') {
                printf("\r\n");
                break;
            }
        }
        printf("%s\n",buf);
        RPC::call(buf, outbuf);
    }
}
