# Smart Home Security System




<!--
## Why?

We are building a 
We _firmly_ believe that all software should be open source 
_especially_ anything security related.
-->



## What?

Our Security System will consist of **4 parts**
and is best explained by the following diagrams.

## 1. "Low Stakes" Access 

For low-stakes access to _internal_ doors we assume the person has already verified their device at the _external_ door so we do not need to send them a push notification.

![image](https://user-images.githubusercontent.com/194400/85981976-f86c1d00-b9dc-11ea-83f0-440e556ed13b.png)

## 2. High Stakes Access

For _external_ entry into the building, we will send the person a push notification to confirm that they have the device in their possession. This is because it's possible to ***clone*** an NFC tag so we cannot rely on the tag being "real" for high-security access.
see:  https://medium.com/insidersec0x42/how-i-finally-managed-to-clone-a-nfc-tag-4a9f64ef49c5

![image](https://user-images.githubusercontent.com/194400/85982020-0752cf80-b9dd-11ea-9e16-71b26080584f.png)

View/Edit this diagram: https://docs.google.com/presentation/d/1Q8CekKPniStTpwOm2O1za3yCB7hGMAujfxQZRJvhGYQ


Our system will run on a Raspberry Pi<sup>1</sup>
and use a comodity NFC Reader to read the NFC chip of the mobile phone.

<!--

For the Mobile App

+ Flutter Beacon https://pub.dev/packages/flutter_beacon 
appears to be tested/maintained

-->

## Relevant Reading / Random Research

+ Turn Your Raspberry Pi into a Bluetooth Beacon
https://circuitdigest.com/microcontroller-projects/turn-your-raspberry-pi-into-bluetooth-beacon-using-eddystone-ble-beacon
+ List of NFC-enabled mobile devices
https://en.wikipedia.org/wiki/List_of_NFC-enabled_mobile_devices
+ What's the difference between RFID, NFC and BLE?
https://youtu.be/7atphSqrvAc
+ 5 Things You Need to Know About Beacon Technology:
https://www.wordstream.com/blog/ws/2018/10/04/beacon-technology