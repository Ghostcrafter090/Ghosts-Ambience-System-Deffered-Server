int lightning = 11;

float f;

unsigned long l;
unsigned long t;
unsigned long tic;
unsigned long ticn;
unsigned long wait = 1;

int counter = 0;
int i = 0;
int vol;
int pin;
int row;
int updateScreen = 0;
int pins[2][5] = {{4, 5, 6, 7, 8}, {2, 3}};
int values[2][5] = {{0, 0, 0, 0, 0}, {0, 0, 0, 0, 0}};

int genRand(int low, int high) {
  int n = random(low, high);
  return n;
}

void setup() {
  Serial.begin(2000000);
  for (auto pin : pins[0]) {
    pinMode(pin, OUTPUT);
  }
  // SoftPWMBegin();
  // SoftPWMSet(lightning, 0);
}

void Math() {
  vol = analogRead(0);
  Serial.println(vol);
  vol = (vol * 10) / 30;
  if (vol > 255) {
    vol = 255;
  }
  pin = genRand(0, 4);
  row = 0; // genRand(0, 1);
  if (vol < 0) {
    vol = 0;
  }
  if (values[row][pin] > 255) {
    values[row][pin] = 0;
  }
  if (row == 0) {
    t = ((values[row][pin] * 6) + (vol)) / 7;
    if (t > values[row][pin]) {
      values[row][pin] = t;
    }
    if (l < millis()) {
      l = millis() + 2000;
      values[row][pin] = ((values[row][pin] * 6) + (vol)) / 7;
    }
  } else {
    values[row][pin] = ((values[row][pin] * 4) + (vol)) / 5;
  }
  if (vol < 0) {
    vol = 0;
  }
}

void mathNoFastLoop() {
  vol = (analogRead(1)) - (vol * vol);
  if (vol < 105) {
    vol = 0;
  }
  vol = vol * 2;
  if (vol > 255) {
    vol = 255;
  }
  pin = genRand(0, 4);
  row = 0; // genRand(0, 1);
  //  if (vol < 20) {
  //    vol = 0;
  //  }
  if (values[row][pin] > 255) {
    values[row][pin] = 0;
  }
  // analogWrite(lightning, (vol));
}

void loop() {
  for (int j = 0; j < 5; j++) {
    mathNoFastLoop();
    analogWrite(j, values[0][j]);
  }
}