void setup() {
  // put your setup code here, to run once:
  pinMode(3, OUTPUT);
  digitalWrite(3, HIGH);
}

const int bufferSize = 24;
double analogBuffer[bufferSize];

int bufferI = 0;

void shiftBuffer(double n) {
  bufferI = bufferI + 1;
  if (bufferI >= bufferSize) {
    bufferI = 0;
  }
  analogBuffer[bufferI] = n;
}

double getBuffer(double i) {
  int ni = bufferI - bufferSize + i;
  if (ni >= bufferSize) {
    ni = ni - bufferSize;
  }
  if (ni < 0) {
    ni = ni + bufferSize;
  }
  return analogBuffer[ni];
}

double getMinimum() {
  int i = 0;
  double minimumValue = 1024;
  while (i < bufferSize) {
    if (getBuffer(i) < minimumValue) {
      minimumValue = getBuffer(i);
    }
    i = i + 1;
  }
  return minimumValue;
}

bool trigger = false;

unsigned long millisTic = 0;

void loop() {
  // put your main code here, to run repeatedly:
  double n = 1024 - analogRead(0);
  shiftBuffer(n);
  double minimum = getMinimum();

  if (millisTic < millis()) {
    millisTic = millis() + 1000;
    Serial.begin(115200);
    Serial.println(trigger);
    Serial.end();
    trigger = false;
  }
  
  if (-3 < (getBuffer(0) - getBuffer(bufferSize - 1)) < 3) {
    if ((getBuffer(0) - minimum) > 8) {
      if (!trigger) {
        trigger = true;
        int i = 0;
        Serial.begin(115200);
        while (i < bufferSize) {
          Serial.println(String(i) + " " + String(getBuffer(i)));
          i = i + 1;
        }
        Serial.end();
      }
    } else if ((getBuffer(bufferSize - 1) - minimum) > 8) {
      if (!trigger) {
        trigger = true;
        int i = 0;
        Serial.begin(115200);
        while (i < bufferSize) {
          Serial.println(String(i) + " " + String(getBuffer(i)));
          i = i + 1;
        }
        Serial.end();
      }
    } else {
      trigger = false;
    }
  } else {
    trigger = false;
  }
}