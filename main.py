import argparse
import logging
import time

from config.settings import Settings

Settings.setup_cuda_dll_path()

logging.basicConfig(level=logging.INFO, format="%(message)s")
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("huggingface_hub").setLevel(logging.ERROR)
logging.getLogger("faster_whisper").setLevel(logging.WARNING)

try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv(): pass

from controllers.speech_to_text_controller import SpeechToTextController
from services.audio_capture_service import AudioCaptureService
from utils.audio_helpers import AudioHelpers

logger = logging.getLogger(__name__)

_BANNER = """+--------------------------------------------+
|        Study Speech-to-Text                 |
|   Local transcription of system audio       |
+--------------------------------------------+"""

def main():
    """
    Ponto de entrada da CLI: parseia os argumentos e despacha para o comando escolhido.

    Returns:
        None
    """
    Settings.force_utf8_console()
    load_dotenv()

    parser = argparse.ArgumentParser(description="Study Speech-to-Text")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    listen_parser = subparsers.add_parser("listen", help="Start transcribing system audio")
    listen_parser.add_argument("--whisper-model", default=Settings.WHISPER_MODEL_SIZE, help="tiny/base/small/medium/large-v3")
    listen_parser.add_argument("--language", default=Settings.WHISPER_LANGUAGE, help="Language code")

    subparsers.add_parser("test-audio", help="Test audio capture for 5 seconds")

    args = parser.parse_args()

    if args.command is None or args.command == "listen":
        print(_BANNER)
        whisper_model = getattr(args, "whisper_model", Settings.WHISPER_MODEL_SIZE)
        language = getattr(args, "language", Settings.WHISPER_LANGUAGE)
        controller = SpeechToTextController(whisper_model=whisper_model, language=language)
        controller.start()

    elif args.command == "test-audio":
        print(_BANNER)
        print("Testing audio capture for 5 seconds...")
        audio_service = AudioCaptureService()
        audio_service.start()
        chunks = []
        max_rms = 0.0
        end_time = time.time() + 5
        while time.time() < end_time:
            payload = audio_service.get_audio_chunk()
            if payload is None:
                continue
            data, sample_rate, channels = payload
            chunks.append(payload)
            audio_array = AudioHelpers.pcm_to_float32(data, sample_rate, channels)
            max_rms = max(max_rms, AudioHelpers.calculate_rms(audio_array))
        audio_service.stop()
        if not chunks:
            print("No audio detected. Check your audio device.")
        elif max_rms > Settings.SPEECH_RMS_THRESHOLD:
            print(f"Audio detected successfully. Captured {len(chunks)} chunks, peak RMS={max_rms:.4f}.")
        else:
            print(f"Chunks captured ({len(chunks)}), but signal is silent (peak RMS={max_rms:.6f}). Check system volume/output device.")

if __name__ == "__main__":
    main()
