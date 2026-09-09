# Ambiente atual — Study-SpeechToText

Derivado do `Project-EnglishAssistant`, mantendo apenas o pipeline de captura de
áudio + transcrição (Speech-to-Text). Removido: Claude/Gemini CLI, contexto
customizável, tutor de inglês, streaming de sugestão.

## Pipeline

```
AudioCaptureService -> TranscriptionService -> SpeechToTextController -> terminal + output/
```

## Dependências externas

- Windows 10/11 (WASAPI Loopback exclusivo do Windows)
- Nenhuma chave de API — tudo roda local
