<div align="center">

# Getting Started with `dwyl/smart-home-*`
Set up a development or production environment of the Dwyl smart home system.

____

</div>

**This document is a work in progress, 
please file an issue for any problems you find setting up the
development environment**

----

### What?
This is a getting started guide for the Dwyl smart home system.
It contains everything you need to set up your own system;
either for development or production.

It contains no infomation on any of the protocols used or how the system works,
this can be found here: ***TODO: Design documentation***

### Why?
It is a complex system with lots of moving parts, 
and unfortunately setting it up requires some time and configuration. 
We've tried to make this as simple as possible, with only
two repositories needed to make a working system. 
You also need to make sure you have compatible hardware, 
found in the "prerequisites" section.

----

## Prerequisites

#### Required Knowledge

You should be able to go through this guide with no previous knowledge of Iot,
Elixir, or Nerves. 
However, we do recommened you go though our [Learn Nerves](https://github.com/dwyl/learn-nerves)
tutorial first so you know *why* things are happening and have Nerves setup
on your computer.
Some knowledge of wiring up GPIO headers on a Raspberry Pi would also
go a long way.

#### Required hardware
Although we have no "hard" requirements on the specifics - 
(it should work on any [Nerves compatible](https://hexdocs.pm/nerves/targets.html)
hardware) - this is the hardware the systems been designed for and will work
best on.

| Hardware | Notes |
|----------|--------|
Raspberry Pi 3+ / Zero | Or anything better with WiFi support
PN532 Development board | Find on with UART support
Necessary Connectors | You'll need at least 4 female-female wires <sup>1</sup>
Hub Server | Anything that can run a server, another Raspberry Pi, or I used my laptop for development.

1 : You can also use a breadboard with normal F-to-M jumper wires
https://imgur.com/a/OQK8zMO


#### Required Software

You'll need Elixir and Nerves setup on your computer. 
If you don't have this, please follow the first part of our 
[Learn Nerves](https://github.com/dwyl/learn-nerves) tutorial.

API Development software. Our hub currently does not have a GUI,
only a REST API. 
I recommend using [Insomnia Core](https://insomnia.rest/) as there's a 
workspace already setup in the Hub repo.

You'll also need a Dwyl API key, follow the instructions here:
https://github.com/dwyl/auth_plug#2-get-your-auth_api_key-

## Setup

1. Clone the necessary repositories:

        git clone https://github.com/dwyl/smart-home-auth-server
        git clone https://github.com/dwyl/smart-home-firmware

2. If you haven't yet, set your DWYL_API_KEY/AUTH_API_KEY

        export AUTH_API_KEY=<Your Key> 

3. Wire up the Raspberry Pi to the PN532 board over UART

  [GPIO Diagram](https://pinout.xyz/pinout/uart)

  | Pi           | PN532 |
  |--------------|-------|
  5v             | 5v
  Ground         | Ground 
  TXD (GPIO 14)  | RX
  RXD (GPIO 15)  | TX

Use the linked GPIO diagram to work out which pins which. Your development
board should have pins labelled.


