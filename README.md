# lyre
A python based voice diarization software. This software supports "sound profile" based diarization.

## Base Idea
Media in, diarized voices out

### Stage 1: Ingestion
Check media formation and compatibility before processing

IN:
MP4, MOV, M4V, MKV, WebM, AVI, FLV, WMV, MPEG/MPG, 3GP, OGV, TS/MTS

MP3, WAV, FLAC, AAC/M4A, OGG (Vorbis/Opus), WMA, AIFF, APE, ALAC

OUT:

.wav (16-bit PCM, mono, 16 kHz)

### Stage 2: Voice or Noise Check (Voice Activity Detection - VAD)

Check if the audio contains distinguishable voices or just background noise before proceeding to diarization.

Implemented with a dependency-free heuristic (frame energy, zero-crossing rate, and energy variation) using only the Python standard library.

Proposed Output (`type` is one of `"voice"`, `"noise"`, `"silence"`):
```json
{
    "segments": [
        {
            "start": 0.0,
            "end": 5.0,
            "type": "voice"
        }
    ]
}
```