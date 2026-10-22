#include <taurus/stdlib.h>
#include <taurus/encoding.h>
#include <taurus/uart.h>
#include <taurus/gpio.h>
#include <stdio.h>

#define PIR_PIN 0   // Connect PIR OUT pin to GPIO 0
#define RED_LED_PIN 24  // Onboard Red LED on Aries V3 (Active-Low)
#define GREEN_LED_PIN 22  // Onboard Green LED on Aries V3 (Active-Low)
#define BLUE_LED_PIN 23  // Onboard Blue LED on Aries V3 (Active-Low)

#define PWM_STEPS 16
#define COLOR_FRAMES 625

static void show_color(int red, int green, int blue) {
    // 625 frames x 16 steps x 1000 iterations is about two seconds.
    for (int frame = 0; frame < COLOR_FRAMES; frame++) {
        for (int step = 0; step < PWM_STEPS; step++) {
            GPIO_write_pin(RED_LED_PIN, step < red ? LOW : HIGH);
            GPIO_write_pin(GREEN_LED_PIN, step < green ? LOW : HIGH);
            GPIO_write_pin(BLUE_LED_PIN, step < blue ? LOW : HIGH);

            for (volatile int delay = 0; delay < 1000; delay++);
        }
    }

}

int main() {
    GPIO_write_pin(RED_LED_PIN, HIGH);
    GPIO_write_pin(GREEN_LED_PIN, HIGH);
    GPIO_write_pin(BLUE_LED_PIN, HIGH);

    printf("\r\n--- Dhinka Chika VIBGYOR with RGB ---\r\n");
    printf("GET READYYYYYYY...\r\n");

    // Simple delay to let the PIR sensor stabilize its infrared reading
    for (volatile int i = 0; i < 15000000; i++);


    fflush(stdout); // Force the output to the serial port
    fflush(stderr); // Force the error output to the serial port

    // Turn off onboard Green LED initially (HIGH = OFF for onboard LEDs)
    GPIO_write_pin(GREEN_LED_PIN, HIGH);

    while (1) {
        // VIBGYOR, using 16-step software PWM values for R, G, and B.
        show_color(8, 0, 16);   // Violet
        show_color(4, 0, 16);   // Indigo
        show_color(0, 0, 16);   // Blue
        show_color(0, 16, 0);   // Green
        show_color(16, 16, 0);  // Yellow
        show_color(16, 6, 0);   // Orange
        show_color(16, 0, 0);   // Red
    }

    return 0;
}