# About
This is the Remote Script of an Ableton Control Surface that sends out the active track's color in RGB over MIDI. It sends it in two formats:
* MIDI CC:
  * each byte of the RGB value (R_hi, R_lo, G_hi, G_lo, B_hi, B_lo) is sent using a different CC (100-105) on channel 0 (status byte = 0xB0). *
* SYSEX:
  * the whole RGB is sent with a single SYSEX message using manufacturer ID = 100 (no particular reason other than being in the valid range < 128). 

\* CC (100-105) should work with most devices that have at most 64 elements to map (knobs, faders, buttons, etc). Notes use a different kind of MIDI message and don't interfere with each other.


# Installation
1. Copy dir *Color_Sender* to the *Remote Scripts* dir in your Ableton's User Library:
* macOS = `/Users/[username]/Music/Ableton/User Library/Remote Scripts/`
* Windows = `C:\Users\[username]\Documents\Ableton\User Library\Remote Scripts\`
2. Select the *Color Sender* Control Surface in Ableton:
  * `Settings > Link, Tempo & MIDI > MIDI`
    * Make sure that *Remote* is enabled for your device's `Output Ports`
3. Configure your external device.
4. Vibe jamming in sync with track colors.


# F.A.Q.

## Remote Script? Control Surface?
tl;dr - they are what external devices use to interact with Ableton Live.
 
Control Surfaces typically enable tactile control of Live, but they work both ways and they can also send updates to an external device. The Remote Script is the code that contains the Control Surface implementation.

## What version of Ableton Live is supported?
Tested with Ableton Live 11 and 12.

## Can I assign more than one Control Surface to the same device?
Yes, if your device already has a different Control Surface assigned, you can still add a second one to it - it will send in and receive MIDI out from all Control Surfaces assigned.