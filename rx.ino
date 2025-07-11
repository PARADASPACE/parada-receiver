#include <SPI.h>
#include <LoRa.h>
#define LORA_SCK 18
#define LORA_MISO 19
#define LORA_MOSI 23
#define LORA_SS 5
#define LORA_RST 14
#define LORA_DIO0 26
#define LORA_BAND 433E6  // pro XL1278

typedef struct {
  uint16_t temp_cx100;
  uint16_t humidity_px10;
  uint16_t pressure_hPax10;
  int16_t acce_x, acce_y, acce_z;
  int16_t gyro_x, gyro_y, gyro_z;
  int16_t mpu_temp_cx100;
  int32_t gps_lat_microdeg;
  int32_t gps_lon_microdeg;
  int32_t gps_alt_cm;

  uint8_t crc8;
} __attribute__ ((packed)) packet_t;

packet_t receive_packet();

uint8_t calculate_crc8(const uint8_t* data, size_t len){
  uint8_t crc = 0x00;
  for(size_t i = 0; i < len; ++i){
    crc ^= data[i];
    for(uint8_t j = 0; j < 8; ++j){
      crc = (crc & 0x80) ? (crc << 1) ^ 0x07 : (crc << 1);
    }
  }
  return crc;
}


void setup() {
  Serial.begin(9600);
  while (!Serial);

  // Nastavení pinů
  //SPI.begin(LORA_SCK, LORA_MISO, LORA_MOSI, LORA_SS);
  LoRa.setPins(LORA_SS, LORA_RST, LORA_DIO0);

  Serial.println("Inicializuji LoRa přijímač…");

  if (!LoRa.begin(LORA_BAND)) {
    Serial.println("LoRa inicializace SELHALA!");
    while (1);
  }

  Serial.println("LoRa inicializována, čekám na zprávy…");
}

void loop() {
int packetSize = LoRa.parsePacket();
  if (packetSize) {
    packet_t packet;
    uint8_t* p = (uint8_t*)&packet;
    for (int i = 0; i < sizeof(packet_t); i++) {
      if (LoRa.available()) {
        p[i] = LoRa.read();
      }
    }

    if (calculate_crc8((uint8_t*)&packet, sizeof(packet_t) - 1) == packet.crc8) {
      print_packet(packet);
    } else {
      Serial.println("CRC check failed!");
      print_packet(packet);
    }
  }
}

void print_packet(packet_t packet) {
  Serial.print("temperature:");
  Serial.print((float)(packet.temp_cx100)/100);
  Serial.println();
3
  Serial.print("humidity:");
  Serial.println((float)(packet.humidity_px10)/10);

  Serial.print("pressure:");
  Serial.println((float)(packet.pressure_hPax10)/10);

  Serial.print("acceleration:");
  Serial.print((float)(packet.acce_x)/1000);
  Serial.print(",");
  Serial.print((float)(packet.acce_y)/1000);
  Serial.print(",");
  Serial.println((float)(packet.acce_z)/1000);

  Serial.print("gyroscope:");
  Serial.print((float)(packet.gyro_x)/100);
  Serial.print(",");
  Serial.print((float)(packet.gyro_y)/100);
  Serial.print(",");
  Serial.println((float)(packet.gyro_z)/100);


// GPSKU MUSIM JESTE DOPSAT A OVERIT!!!!
  Serial.print("GPS (LAT, LON, ALT): ");
  Serial.print((float)(packet.gps_lat_microdeg)/1e6);
  Serial.print(",");
  Serial.print((float)(packet.gps_lon_microdeg)/1e6);
  Serial.print(",");
  Serial.println((float)(packet.gps_alt_cm)/100);
}

packet_t receive_packet(){
int packetSize = LoRa.parsePacket();
  if (packetSize == sizeof(packet_t)) {
    packet_t packet;
    uint8_t* p = (uint8_t*)&packet;
    for (int i = 0; i < sizeof(packet_t); i++) {
      if (LoRa.available()) {
        p[i] = LoRa.read();
      }
    }

    if (calculate_crc8((uint8_t*)&packet, sizeof(packet_t) - 1) == packet.crc8) {
      print_packet(packet);
    } else {
      Serial.println("CRC check failed!");
    }
  }
}
