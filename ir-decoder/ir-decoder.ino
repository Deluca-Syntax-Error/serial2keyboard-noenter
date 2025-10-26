const int irPin = 9;
int lastKey = 0;
unsigned long lastKeyTime = 0;

const unsigned long holdDelay = 300;   
const unsigned long repeatInterval = 100;
const unsigned long minInterval = 300; // debounce para no enviar dos veces

bool isHolding = false;

void setup() {
  Serial.begin(115200);
  pinMode(irPin, INPUT);
}

void loop() {
  unsigned long now = millis();
  int key = getIrKey();

  if (key != 0) {
    if (key != lastKey) {
      Serial.println(key);
      lastKey = key;
      lastKeyTime = now;
      isHolding = false;
    } else {
      // mismo botón
      if (!isHolding && now - lastKeyTime > holdDelay) {
        isHolding = true;
        lastKeyTime = now;
      }
      if (isHolding && now - lastKeyTime >= repeatInterval) {
        Serial.println(key);
        lastKeyTime = now;
      }
    }
  } else {
    // botón liberado
    lastKey = 0;
    isHolding = false;
  }
}

int getIrKey() {
  long len = pulseIn(irPin, LOW);
  int key = 0;
  long temp;

  if (len > 5000) { // código completo
    for (int i = 1; i <= 32; i++) {
      temp = pulseIn(irPin, HIGH);
      if (temp > 1000) key = key + (1 << (i - 17));;
    }
    if(key<0) key = -key;
    
    return key;
  } else if (len > 500) { // código corto (hold)
    return lastKey;
  }

  return 0;
}

<<<<<<< HEAD
=======
int sendText(char* tx) {
  Serial.write(tx);
  Serial.write(0x02);
  delay(200); // CAMBIO: era 500, ahora 200
  return 0;
}

int exe(char* tx) {
  Serial.write(0x00);
  delay(200); // CAMBIO: era 500, ahora 200
  Serial.write("r");
  delay(200); // CAMBIO: era 500, ahora 200
  Serial.write(tx);
  delay(200); // CAMBIO: era 500, ahora 200
  Serial.write(0x02);
  delay(200); // CAMBIO: era 500, ahora 200
  return 0;
}

int ful() {
  Serial.write(0x03);
  delay(200); // CAMBIO: era 500, ahora 200
  return 0;
}

int vol(char v, int cant) {
  byte vol;
  if (v == '+') {
    vol = 0x06;
  } else if (v == '-') {
    vol = 0x07;
  }
  
  for (int i = 0; i < cant; i++) { // ARREGLADO: faltaba i=0
    Serial.write(vol);
    delay(150); // CAMBIO: era 300, ahora 150
  }
  return 0;
}
>>>>>>> 24916d06ea6a12c5da61bcfc4911f00031c9bc60
