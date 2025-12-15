from _Framework.ControlSurface import ControlSurface
from _Framework.SubjectSlot import subject_slot
from itertools import chain
from datetime import datetime

LOG_FILE_PATH = ""
CC_STATUS_BYTE = 0xB0
CC_NUMBER_R_hi = 100
CC_NUMBER_R_lo = 101
CC_NUMBER_G_hi = 102
CC_NUMBER_G_lo = 103
CC_NUMBER_B_hi = 104
CC_NUMBER_B_lo = 105
SYSEX_START = 0xF0
SYSEX_END = 0xF7
SYSEX_MANUFACTURER_ID = 100
SYSEX_COMMAND = 0x01

class Color_Sender(ControlSurface):
    """
    When a new track is selected it sends its RGB using 2 types of MIDI messages:
        1. CC (100-105) = R_hi:100:, R_lo:101, G_hi:102, G_lo:103, B_hi:104, B_lo:105
        2. SYSEX = 0xdb, Value = RGB
    """
    def __init__(self, c_instance):
        ControlSurface.__init__(self, c_instance)
        
        with self.component_guard():
            self._setup_listeners()
            
        self._log_message("--- Color Sender initialized ---")


    def _log_message(self, message):
        super(Color_Sender, self).log_message(message)
        
        if not LOG_FILE_PATH:
            return

        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"[{timestamp}] {message}\n"
            
            with open(LOG_FILE_PATH, 'a') as f:
                f.write(log_entry)
        except Exception as e:
            super(Color_Sender, self).log_message(self, f"FILE LOG ERROR: Could not write to log file. {e}")


    def _setup_listeners(self):
        self._on_selected_track_changed.subject = self.song().view
        self._log_message("Setup listeners complete.")


    @subject_slot('selected_track')
    def _on_selected_track_changed(self, *a, **k):
        active_track = self.song().view.selected_track
        
        if not active_track:
            return

        color = active_track.color
        self._send_cc_color(color)
        self._send_sysex_color(color)
        
        log_msg = f"Track changed to: {active_track.name}"
        self._log_message(log_msg)


    def _send_cc_color(self, color):
        if not self._enabled:
            return
            
        r_8bit = (color >> 16) & 0xFF
        g_8bit = (color >> 8) & 0xFF
        b_8bit = color & 0xFF
        
        self._send_cc_color_hl(CC_NUMBER_R_lo, CC_NUMBER_R_hi, r_8bit)
        self._send_cc_color_hl(CC_NUMBER_G_lo, CC_NUMBER_G_hi, g_8bit)
        self._send_cc_color_hl(CC_NUMBER_B_lo, CC_NUMBER_B_hi, b_8bit)


    def _send_cc_color_hl(self, cc_number_lo, cc_number_hi, color_8bit):
        lo_4bit = color_8bit & 0x0F
        self._send_cc_color_4bit(cc_number_lo, lo_4bit)
        
        hi_4bit = color_8bit >> 4
        self._send_cc_color_4bit(cc_number_hi, hi_4bit)


    def _send_cc_color_4bit(self, cc_number, color_4bit):
        if 0 <= color_4bit <= 127:
            self._send_midi((CC_STATUS_BYTE, cc_number, color_4bit))
            
            log_msg = f"Sent CC {cc_number} with value {color_4bit} (RGB)."
            self._log_message(log_msg)
        else:
             error_msg = f"Error: CC {cc_number} with RGB {color_4bit} is out of valid MIDI range (0-127)."
             self._log_message(error_msg)


    def _send_sysex_color(self, color):
        if not self._enabled:
            return

        sysex_message = [
            SYSEX_START,
            SYSEX_MANUFACTURER_ID,
            SYSEX_COMMAND,
        ]

        sysex_message.append(color & 0x7F) # bits 0-6 (LSB of B)
        sysex_message.append((color >> 7) & 0x7F) # bits 7-13 (MSB of B + LSB of G)
        sysex_message.append((color >> 14) & 0x7F) # bits 14-20 (MSB of G + LSB of R)
        sysex_message.append((color >> 21) & 0x7F) # bits 21-27 (MSB of R)
        sysex_message.append(SYSEX_END)
        
        self._send_midi(tuple(sysex_message))
        self.log_message(f"Sent 24-bit RGB ({color}) via SysEx.")


def create_instance(c_instance):
    return Color_Sender(c_instance)