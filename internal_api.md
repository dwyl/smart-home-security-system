# `smart-home-*` Internal API Documentation

The smart home system uses an internal Phoenix Channel (Websocket) API to
communicate in real time with different devices on the network.

---

## Hub

### Socket
On connecting to the Socket a device must provide a unique identifier
to the server as part of the connection params.

#### Connecting to `Socket`

```elixir
params: %{
  name: "unique_name"
}
```

All current devices use the value returned by `:inet.gethostname`, as this
should be unique and is based off `cpuid`.

### Channels

The hub currently provides the following channels:

+ `lock:<lock-serial>`

#### `lock:<lock-serial>`

Locks and similar devices must connect to this channel with their own serial
number. On connecting to this channel, the hub will assign the device a 
unique ID, or give the device its previous UUID. 

On joining, the hub will give the current state of the lock as a response.
The `lock` MUST use this state to configure itself.

##### Events

+ `reset`
  
  Sending a `reset` event will cause the hub to reply with the intented
  state of the device, similar to the initial handshake.

  This is useful for putting the device in a known good state after 
  accomplishing a task.

  No message body.

  Reply: Initial state.

+ `pair:complete`
  
  Devices should send this event once a pairing event has been completed.
  They should send back ALL the infomation sent to them in the initial message,
  plus the serial number of the item being paired.

  ```elixir
  message: %{
    # << Initial params sent on pair request>>,
    serial: "paired items serial"
  }
  ```

  Reply: `:ok`

---
## Devices

### Lock

#### Channels

Lock-style devices should handle and connect to the following channels:

+ `lock:<lock_serial>`


#### `lock:<lock_serial>`

All lock style devices must connect to this channel to be able to be controlled.

##### Events

+ `mode:pair`

  On receiving this event, devices must reconfigure themselves into a 
  "pairing" mode. They must also keep track the event payload as this must be
  sent back to the server on complete to identify the pair.
  -- See Hub/`pair:complete`.

  ```elixir
  payload: %{
    # KEEP TRACK OF ALL THE INFO IN HERE
  }
  ```

  Reply: no

