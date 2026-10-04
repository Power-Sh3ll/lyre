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

.mp3

### Stage 2: Voice or Noise Check (Voice Activity Detection - VAD)

Check if the audio contains distinguishable voices or just background noise before proceeding to diarization.

Proposed Output:
```json
{
    segments: [
        {
            "start": 0.0,
            "end": 5.0,
            "type": "voice" // (Voice, Noise, None)
        }
    ]
}
```