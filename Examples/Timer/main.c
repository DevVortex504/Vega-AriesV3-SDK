#include <stdio.h>
#include <time.h>
#include <taurus/encoding.h>
#include <taurus/uart.h>
#include <taurus/stdlib.h>

__attribute__((aligned(16))) int dummy_tls[16] = {0};
extern clock_t get_time(void);

int main() {
    printf("\r\n--- Aries V3 Timer Test ---\r\n");
    clock_t start = get_time();
    
    for(volatile int i = 0; i < 1000000; i++); 
    
    clock_t end = get_time();

    printf("Start cycle: %lu\r\n", (unsigned long)start);
    printf("End cycle: %lu\r\n", (unsigned long)end);
    printf("Elapsed cycles: %lu\r\n", (unsigned long)(end - start));
    fflush(stdout); // Force the output to the serial port

    while(1) {
        printf("Program ran successfully! Chilling...\r\n");
        fflush(stdout); // Force the output in the loop too
        for(volatile int i = 0; i < 5000000; i++); 
    }
    return 0;
}
