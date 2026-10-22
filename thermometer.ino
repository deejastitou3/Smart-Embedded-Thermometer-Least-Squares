#include <math.h>

// --- Pin Definitions ---
const int PIN_LM35 = A0;       // Analog input for LM35
const int PIN_BUTTON = 2;      // Trigger button (active LOW with INPUT_PULLUP)
const int PIN_BUZZER = 8;      // Buzzer for measurement confirmation

// --- Constants ---
const int NUM_MEAS = 20;       // Number of samples for statistical filtering
const float VREF = 5.0;        // Arduino reference voltage
const float ADC_RES = 1024.0;  // 10-bit ADC resolution

void setup() {
  Serial.begin(9600);
  pinMode(PIN_BUTTON, INPUT_PULLUP);
  pinMode(PIN_BUZZER, OUTPUT);
  digitalWrite(PIN_BUZZER, LOW);
}

void loop() {
  // Wait for button press to trigger measurement
  if (digitalRead(PIN_BUTTON) == LOW) {
    delay(50); // Simple debounce
    
    float temp_values[NUM_MEAS];
    float sum_x = 0, sum_y = 0, sum_xy = 0, sum_x2 = 0;
    
    // 1. Data Acquisition & Summation for Least Squares
    for (int i = 0; i < NUM_MEAS; i++) {
      int raw_adc = analogRead(PIN_LM35);
      // LM35 characteristic: 10mV per °C. ADC step = 5V/1024. Temp = raw * (5/1024) * 100
      temp_values[i] = raw_adc * (VREF / ADC_RES) * 100.0; 
      
      sum_x += i;
      sum_y += temp_values[i];
      sum_xy += (float)i * temp_values[i];
      sum_x2 += (float)i * i;
      
      delay(10); // Small delay to space out samples and reduce correlation
    }
    
    // 2. Calculate Least Squares Linear Regression coefficients (y = ax + b)
    float denominator = (NUM_MEAS * sum_x2) - (sum_x * sum_x);
    // Prevent division by zero (though mathematically impossible here)
    if (denominator != 0) {
      float a = ((NUM_MEAS * sum_xy) - (sum_x * sum_y)) / denominator;
      float b = (sum_y - (a * sum_x)) / NUM_MEAS;
      
      // 3. Statistical Filtering: Select the measurement with minimum error to the regression line
      float best_temp = temp_values[0];
      float min_err = 1000.0;
      
      for (int i = 0; i < NUM_MEAS; i++) {
        float err = fabs(temp_values[i] - ((a * i) + b));
        if (err < min_err) {
          min_err = err;
          best_temp = temp_values[i];
        }
      }
      
      // 4. Transmit filtered data and signal completion
      Serial.println(best_temp);
      
      digitalWrite(PIN_BUZZER, HIGH);
      delay(200);
      digitalWrite(PIN_BUZZER, LOW);
    }
    
    delay(1000); // Wait before allowing the next trigger
  }
}