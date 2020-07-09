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


### Stuff to work on

We need to work out solutions to the following problems:

+ [X] **Can't get it to recognise the fob-type NFC tags, or NFC cards reliably**
      
     This could be down to a multitude of issues :/
      
     + We may not be delivering enough power to the NFC reader - we're using a 5v header with a 
       good power supply though.
     + ~~Apparently theres some issues when reading over UART - I may test this using a python SPI library.~~
     + Another issue - NFC seems like black magic.
    
     
     
+ [ ] **We're maintaining our own PN532 library**
      
     We're not NFC or embedded experts, ideally we wouldn't want to do this.
      Currently we're only maintaining documentation and dependencies.
      
+ [ ] **We ACK really frequently**

    Do we have to? It can slow the Pi Zero down to a crawl sometimes :(
    
    + This could be down to excessive logging - Erlang I/O is pretty slow ✅ -- Remove logging to remove performance issues
