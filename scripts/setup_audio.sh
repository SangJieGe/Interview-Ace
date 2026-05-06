#!/usr/bin/env bash
# ============================================================
# Interview Ace — Audio Setup Script
#
# Sets up audio routing for capturing system audio (interviewer)
# and microphone (candidate) on Linux.
#
# Usage: bash scripts/setup_audio.sh
# ============================================================

set -euo pipefail

echo "🎤 Interview Ace — Audio Setup"
echo "================================"

# Check for PulseAudio or PipeWire
if command -v pactl &>/dev/null; then
    echo "✓ PulseAudio detected"
    echo ""
    echo "Available audio input devices:"
    pactl list sources short
    echo ""
    echo "To capture system audio, you may need to create a monitor source:"
    echo "  pactl load-module module-loopback"
elif command -v pw-cli &>/dev/null; then
    echo "✓ PipeWire detected"
    echo ""
    echo "Available audio devices:"
    pw-cli ls Device
else
    echo "⚠ No PulseAudio or PipeWire found."
    echo "  Install PulseAudio: sudo apt install pulseaudio"
    echo "  Or PipeWire: sudo apt install pipewire"
fi

echo ""
echo "📝 Set AUDIO_DEVICE_INDEX in .env to your preferred device."
echo "   Run: python -m scripts.list_devices  (coming soon)"
echo ""
echo "Done!"
