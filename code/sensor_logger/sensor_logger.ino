const int SENSOR_PIN = A0;
const unsigned long SAMPLE_INTERVAL_MS = 20;
const unsigned long DEBOUNCE_MS = 300;
const float SMOOTHING_FACTOR = 0.25;
const int CALIBRATION_SAMPLES = 50;

int whiteReading = 250;
int grayReading = 550;
int tapeReading = 800;
int blackReading = 850;

float smoothedReading = -1.0;
int lineCount = 0;
bool overLine = false;
unsigned long lastLineCountMs = 0;
unsigned long lastSampleMs = 0;

int lineThreshold() {
  return (whiteReading + tapeReading) / 2;
}

const char *nearestShade(int reading) {
  int whiteDistance = abs(reading - whiteReading);
  int grayDistance = abs(reading - grayReading);
  int blackDistance = abs(reading - blackReading);
  if (whiteDistance <= grayDistance && whiteDistance <= blackDistance) {
    return "white";
  }
  if (grayDistance <= blackDistance) {
    return "gray";
  }
  return "black";
}

int captureAverage() {
  long total = 0;
  for (int i = 0; i < CALIBRATION_SAMPLES; i++) {
    total += analogRead(SENSOR_PIN);
    delay(20);
  }
  return (int)(total / CALIBRATION_SAMPLES);
}

void captureAnchor(char name, int *anchor) {
  int value = captureAverage();
  *anchor = value;
  Serial.print("captured,");
  Serial.print(name);
  Serial.print(",");
  Serial.println(value);
}

void printSummary() {
  Serial.println("summary");
  Serial.print("white,");
  Serial.println(whiteReading);
  Serial.print("gray,");
  Serial.println(grayReading);
  Serial.print("tape,");
  Serial.println(tapeReading);
  Serial.print("black,");
  Serial.println(blackReading);
  Serial.print("line_threshold,");
  Serial.println(lineThreshold());
  Serial.print("line_count,");
  Serial.println(lineCount);
}

void handleCommand(char command) {
  if (command == 'w') {
    captureAnchor('w', &whiteReading);
  } else if (command == 'g') {
    captureAnchor('g', &grayReading);
  } else if (command == 't') {
    captureAnchor('t', &tapeReading);
  } else if (command == 'b') {
    captureAnchor('b', &blackReading);
  } else if (command == 'z') {
    lineCount = 0;
    lastLineCountMs = 0;
    Serial.println("lines_reset");
  } else if (command == 'p') {
    printSummary();
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(SENSOR_PIN, INPUT);
  Serial.println("time_ms,reading,line_count,shade");
}

void loop() {
  while (Serial.available() > 0) {
    handleCommand(Serial.read());
  }

  unsigned long now = millis();
  if (now - lastSampleMs < SAMPLE_INTERVAL_MS) {
    return;
  }
  lastSampleMs = now;

  int raw = analogRead(SENSOR_PIN);
  if (smoothedReading < 0.0) {
    smoothedReading = raw;
  }
  smoothedReading += (raw - smoothedReading) * SMOOTHING_FACTOR;
  int reading = (int)(smoothedReading + 0.5);

  bool readingIsLine = reading > lineThreshold();
  if (readingIsLine && !overLine && now - lastLineCountMs >= DEBOUNCE_MS) {
    lineCount++;
    lastLineCountMs = now;
  }
  overLine = readingIsLine;

  Serial.print(now);
  Serial.print(',');
  Serial.print(reading);
  Serial.print(',');
  Serial.print(lineCount);
  Serial.print(',');
  Serial.println(nearestShade(reading));
}
