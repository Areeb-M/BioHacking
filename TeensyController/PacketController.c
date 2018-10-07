
char packet_header = 255;
int packet_size = 4;

void setup() {
  Serial.begin(9600);
}

void loop() {
  char packet[packet_size];
  int count = 0;

  // Construct the packet
  while(count < packet_size){
    if(Serial.available()){
      char c = Serial.read();
      if (c != packet_header && count == 0)
        return;
      packet[count++] = c;
    }
  }

  execute(packet[1], packet[2], packet[3]);
}

void execute(char command, char arg1, char arg2){
  switch (command){
    case 0:
      ping(arg1, arg2);
      break;
    case 1:
      pinWrite(arg1, arg2);
      break;
    case 2:
      pinSetup(arg1, arg2);
      break;
    case 3:
      sleep(arg1, arg2);
      break;
  }
}

void ping(char arg1, char arg2){
  Serial.print(arg1 + arg2, DEC);
}


int write_states[] = {LOW, HIGH};
void pinWrite(char arg1, char arg2){
  digitalWrite(arg1, write_states[arg2]);
}

int pin_modes[] = {INPUT, OUTPUT, INPUT_PULLUP};
void pinSetup(char arg1, char arg2){
  pinMode(arg1, pin_modes[arg2]);
}

void sleep(char arg1, char arg2){
  int time = arg1 << 8;
  time = time + arg2;
  delay(time);
}
