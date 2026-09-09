# 🎙️ Study-SpeechToText

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Whisper](https://img.shields.io/badge/Faster--Whisper-STT-FF6F00?style=for-the-badge)
![Windows](https://img.shields.io/badge/Windows-WASAPI-0078D6?style=for-the-badge&logo=windows&logoColor=white)

Transcrição local e contínua do áudio do sistema, via WASAPI Loopback e Faster-Whisper.
Repositório de estudo derivado do `Project-EnglishAssistant`, mantendo só o módulo de
Speech-to-Text — sem o assistente conversacional.

---

## Índice

- [📚 Contextualização do projeto](#-contextualização-do-projeto)
- [🛠️ Tecnologias/Ferramentas utilizadas](#️-tecnologiasferramentas-utilizadas)
- [🖥️ Funcionamento do sistema](#️-funcionamento-do-sistema)
- [📁 Estrutura do projeto](#-estrutura-do-projeto)
- [📌 Como executar o projeto](#-como-executar-o-projeto)

---

## 📚 Contextualização do projeto

Estudo isolado do módulo de captura + transcrição do `Project-EnglishAssistant`:

1. **Captura de áudio do sistema** — WASAPI Loopback no Windows, sem microfone virtual.
2. **Transcrição local** — Faster-Whisper, sem enviar áudio para nuvem.
3. **Saída** — imprime no terminal (Rich) e acrescenta cada trecho transcrito em
   `output/transcript_<timestamp>.txt`.

Sem IA de sugestão de resposta, sem contexto customizável — só o pipeline de STT.

---

## 🛠️ Tecnologias/Ferramentas utilizadas

| Tecnologia | Uso |
|---|---|
| **Python 3.10+** | Linguagem principal |
| **PyAudioWPatch** | Captura de áudio do sistema via WASAPI Loopback |
| **Faster-Whisper** | Transcrição de fala para texto (STT) local |
| **Rich** | Interface de terminal com formatação rica |
| **python-dotenv** | Gerenciamento de variáveis de ambiente |

---

## 🖥️ Funcionamento do sistema

```
[System Audio] -> [WASAPI Loopback] -> [Audio Chunks]
                                            |
                                     [Speech Detection]
                                            |
                                     [Faster-Whisper STT]
                                            |
                                [Terminal + output/transcript_*.txt]
```

1. **AudioCaptureService** captura áudio do sistema via WASAPI Loopback em chunks.
2. **TranscriptionService** detecta fala (RMS energy) e transcreve com Faster-Whisper.
3. **SpeechToTextController** orquestra o laço, imprime no terminal e grava em `output/`.

---

## 📁 Estrutura do projeto

```
Study-SpeechToText/
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
├── pytest.ini
├── config/
│   └── settings.py
├── controllers/
│   └── speech_to_text_controller.py
├── services/
│   ├── audio_capture_service.py
│   └── transcription_service.py
├── utils/
│   ├── audio_helpers.py
│   └── text_helpers.py
├── output/
├── docs/
│   ├── current-state/
│   ├── planning/
│   └── implementation/
└── tests/
```

---

## 📌 Como executar o projeto

### Pré-requisitos

- Python 3.10+
- Windows 10/11 (WASAPI Loopback é exclusivo do Windows)

### Instalação

```bash
git clone https://github.com/rafael-torres-nantes/Study-SpeechToText.git
cd Study-SpeechToText
pip install -r requirements.txt
cp .env.example .env
```

### Uso

```bash
# Iniciar a transcrição contínua
python main.py listen

# Especificar modelo Whisper
python main.py listen --whisper-model large-v3

# Testar captura de áudio
python main.py test-audio
```
