#!/usr/bin/env python3
"""Create .wav files."""
import array
import math
import wave


def _gen_audio(len_ms: int) -> bytes:
    """Return a byte string representing an audio waveform of the requested length (in milliseconds)."""
    audio = array.array('h')

    for n in range(int(len_ms * 44.1)):
        audio.append(int(32765 * math.sin(2 * math.pi * 440 * (n / 44100))))

    return audio.tobytes()


with wave.open('test-10ms.wav', 'wb') as f:
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(44100)
    f.writeframes(_gen_audio(10))


with wave.open('test-250ms.wav', 'wb') as f:
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(44100)
    f.writeframes(_gen_audio(250))


with wave.open('test-1000ms.wav', 'wb') as f:
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(44100)
    f.writeframes(_gen_audio(1_000))


with wave.open('test-5000ms.wav', 'wb') as f:
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(44100)
    f.writeframes(_gen_audio(5_000))


with wave.open('test-10000ms.wav', 'wb') as f:
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(44100)
    f.writeframes(_gen_audio(10_000))
