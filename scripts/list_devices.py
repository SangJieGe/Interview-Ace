"""
Interview Ace — List Audio Devices

Run this script to see available audio input devices.
Use the device index to set AUDIO_DEVICE_INDEX in .env.

Usage:
    python -m scripts.list_devices
"""

try:
    import sounddevice as sd

    print("🎤 Available Audio Input Devices")
    print("=" * 50)
    devices = sd.query_devices()
    for i, dev in enumerate(devices):
        if dev["max_input_channels"] > 0:
            print(f"  [{i}] {dev['name']}")
            print(f"      Channels: {dev['max_input_channels']}, "
                  f"Sample Rate: {dev['default_samplerate']:.0f} Hz")
    print()
    print("Set AUDIO_DEVICE_INDEX in .env to your preferred device.")

except ImportError:
    print("⚠ sounddevice not installed. Run: pip install sounddevice")
