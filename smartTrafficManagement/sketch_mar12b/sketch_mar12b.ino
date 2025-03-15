#include <Arduino.h>
#include <string.h>
#include <LiquidCrystal.h>

// LCD Configuration (adjust pins based on your setup)
const int rs = A0, en = A1, d4 = A2, d5 = A3, d6 = A4, d7 = A5;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

// Pin definitions for 4 roads (each road: red, yellow, green)
const int redPins[4]    = {13, 10, 7, 4};
const int yellowPins[4] = {12, 9, 6, 3};
const int greenPins[4]  = {11, 8, 5, 2};

// Fixed yellow light duration (in milliseconds)
const unsigned long yellowTime = 2000; // 2 seconds

// Global counts array for 4 roads; updated from Serial
int counts[4] = {0, 0, 0, 0};
int roadIndex = 0;

// State management
enum State { WAITING_DATA, GREEN_PHASE, YELLOW_PHASE };
State currentState = WAITING_DATA;
unsigned long phaseStartTime;
unsigned long currentGreenDuration;

// Function prototypes
int findTime(int cnt);
void setAllRoadsToRed();
void updateCountsFromSerial();
void displayRemainingTime(int seconds);

void setup() {
  // Initialize LED pins
  for (int i = 0; i < 4; i++) {
    pinMode(redPins[i], OUTPUT);
    pinMode(yellowPins[i], OUTPUT);
    pinMode(greenPins[i], OUTPUT);
  }
  
  // Initialize LCD
  lcd.begin(16, 2);
  lcd.print("Time remaining:");
  
  // Start Serial
  Serial.begin(9600);
  while (!Serial); // Wait for Serial port
  
  Serial.println("Traffic Light System Initialized.");
  setAllRoadsToRed();
}

void loop() {
  switch (currentState) {
    case WAITING_DATA:
      if (Serial.available() > 0) {
        updateCountsFromSerial();
        int greenSeconds = findTime(counts[roadIndex]);
        currentGreenDuration = greenSeconds * 1000UL;
        
        setAllRoadsToRed();
        digitalWrite(redPins[roadIndex], LOW);
        digitalWrite(greenPins[roadIndex], HIGH);
        
        Serial.print("Road ");
        Serial.print(roadIndex + 1);
        Serial.print(" green for ");
        Serial.print(greenSeconds);
        Serial.println("s");
        
        phaseStartTime = millis();
        currentState = GREEN_PHASE;
      }
      displayRemainingTime(0); // Show 00 when waiting
      break;

    case GREEN_PHASE: {
      long elapsed = millis() - phaseStartTime;
      int remaining = (currentGreenDuration - elapsed) / 1000;
      remaining = max(remaining, 0); // Ensure non-negative
      displayRemainingTime(remaining);
      
      if (elapsed >= currentGreenDuration) {
        digitalWrite(greenPins[roadIndex], LOW);
        digitalWrite(yellowPins[roadIndex], HIGH);
        phaseStartTime = millis();
        currentState = YELLOW_PHASE;
        Serial.print("Road ");
        Serial.print(roadIndex + 1);
        Serial.println(" yellow.");
      }
      break;
    }

    case YELLOW_PHASE: {
      long elapsed = millis() - phaseStartTime;
      int remaining = (yellowTime - elapsed) / 1000;
      remaining = max(remaining, 0);
      displayRemainingTime(remaining);
      
      if (elapsed >= yellowTime) {
        digitalWrite(yellowPins[roadIndex], LOW);
        digitalWrite(redPins[roadIndex], HIGH);
        Serial.println("DONE");
        roadIndex = (roadIndex + 1) % 4;
        currentState = WAITING_DATA;
      }
      break;
    }
  }
}

// Helper functions
int findTime(int cnt) {
  if (cnt >= 50) return 60;
  if (cnt >= 40) return 50;
  if (cnt >= 30) return 40;
  if (cnt >= 20) return 30;
  if (cnt >= 10) return 20;
  return 10;
}

void setAllRoadsToRed() {
  for (int i = 0; i < 4; i++) {
    digitalWrite(redPins[i], HIGH);
    digitalWrite(yellowPins[i], LOW);
    digitalWrite(greenPins[i], LOW);
  }
}

void updateCountsFromSerial() {
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    input.trim();
    
    // Parse counts
    int idx = 0;
    char* token = strtok(const_cast<char*>(input.c_str()), " ,");
    while (token != NULL && idx < 4) {
      counts[idx++] = atoi(token);
      token = strtok(NULL, " ,");
    }
    
    // Print parsed counts
    Serial.print("Counts updated: ");
    for (int i = 0; i < 4; i++) {
      Serial.print(counts[i]);
      Serial.print(" ");
    }
    Serial.println();
  }
}

void displayRemainingTime(int seconds) {
  lcd.setCursor(0, 1);
  if (seconds < 10) lcd.print("0");
  lcd.print(seconds);
}