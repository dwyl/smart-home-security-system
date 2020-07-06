# Using PN532 on a Raspberry Pi with Elixir
 -- WORK IN PROGRESS --
 
 ----
 
 To connect our PN532 to our Raspberry Pi, we're going to communicate over the UART protocol.
 This is a really simple protocol, with one TX (Transmit) wire
 and one RX (Recieve) wire.
 
 The manufacturer suggests using SPI which I think is a good future goal. Adafruit has an
 excellent Python implementation which we could translate into Elixir: 
 https://github.com/adafruit/Adafruit_Python_PN532
 
### To connect over UART

[GPIO Diagram](https://pinout.xyz/pinout/uart)

| Pi           | PN532 |
|--------------|-------|
5v             | 5v
Ground         | Ground 
TXD (GPIO 14)  | RX
RXD (GPIO 15)  | TX


**Note:**
Currently struggling to read tags - this could be a UART problem (manufacturer suggests SPI)
or Pi may not be able to produce enough power. In which case we need to get power from somewhere
else (PoE?)

### Communicating

To communicate with the NFC module, I've forked https://github.com/jmerriweather/nerves_io_pn532
to https://github.com/dwyl/nerves_io_pn532 where I have bumped dependencies and currently documenting
availiable methods.

Some things I still need to work out:

+ [ ] Reducing `ACK` frequency - this may be possible but could compromise Read times
+ [ ] Do we need to read cards other than MiFare type cards? We will need to implement this.

#### Connecting to board

Using `Nerves.IO.PN532`:

Refer to https://github.com/dwyl/nerves_io_pn532/blob/master/README.md

##### Interface Names:

```
rpi4 ~> "ttyS0"
rpi0 ~> "ttyAMA0"
```

(Another reason to use SPI in future, Pi's only have one UART out and its very useful for debugging etc)

