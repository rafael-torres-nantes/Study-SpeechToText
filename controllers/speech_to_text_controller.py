import logging
import time
from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.markup import escape

from config.settings import Settings
from services.audio_capture_service import AudioCaptureService
from services.transcription_service import TranscriptionService
from utils.text_helpers import TextHelpers

logger = logging.getLogger(__name__)

class SpeechToTextController:
    """Orquestra captura de áudio e transcrição contínua em tempo real."""

    def __init__(self, whisper_model: str = Settings.WHISPER_MODEL_SIZE, language: str = Settings.WHISPER_LANGUAGE) -> None:
        """
        Função de inicialização do controller de transcrição.

        Args:
            whisper_model (str): Tamanho do modelo Whisper a carregar.
            language (str): Código de idioma para transcrição.

        Returns:
            None
        """
        self.whisper_model = whisper_model
        self.console = Console()
        self.audio_service = AudioCaptureService()
        self.transcription_service = TranscriptionService(model_size=whisper_model, language=language)
        self.is_running = False
        self._start_time = 0.0
        self._transcript_path = Settings.OUTPUT_DIR / f"transcript_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    def start(self) -> None:
        """
        Inicia a transcrição: exibe status inicial e entra no laço de escuta.

        Returns:
            None
        """
        self.is_running = True
        self._start_time = time.time()
        Settings.OUTPUT_DIR.mkdir(exist_ok=True)

        self.console.print(f"[bold green]Whisper Model:[/] {self.whisper_model}")
        self.console.print(f"[bold green]Transcript:[/] {self._transcript_path}")

        try:
            self._process_loop()
        except KeyboardInterrupt:
            self.console.print("\n[bold yellow]Stopping gracefully...[/]")
        finally:
            self.stop()

    def stop(self) -> None:
        """
        Finaliza a captura e a transcrição, e reporta a duração da sessão.

        Returns:
            None
        """
        self.is_running = False
        self.audio_service.stop()
        self.transcription_service.stop()
        elapsed = TextHelpers.format_timestamp(time.time() - self._start_time)
        self.console.print(f"[dim]Session ended - duration {elapsed}.[/]")

    def _process_loop(self) -> None:
        self.audio_service.start()
        accumulated_audio = []
        is_speaking = False
        max_silence_frames = max(1, int(Settings.SILENCE_TIMEOUT_SECONDS / Settings.AUDIO_CHUNK_DURATION_SECONDS))
        silence_frames = 0

        self.console.print(Panel(Text("Listening to system audio...", style="dim italic"), border_style="blue", title="Status"))

        while self.is_running:
            payload = self.audio_service.get_audio_chunk()
            if payload is None:
                time.sleep(0.1)
                continue

            chunk, sample_rate, channels = payload
            speech_detected = self.transcription_service.is_speech(chunk, sample_rate, channels)

            if speech_detected:
                is_speaking = True
                silence_frames = 0
                accumulated_audio.append(payload)
            elif is_speaking:
                silence_frames += 1
                accumulated_audio.append(payload)

            if is_speaking and silence_frames > max_silence_frames:
                transcription = self.transcription_service.transcribe(accumulated_audio)
                if transcription:
                    elapsed = TextHelpers.format_timestamp(time.time() - self._start_time)
                    self.console.print(Panel(escape(transcription), title=f"[{elapsed}]", border_style="cyan"))
                    self._append_transcript(elapsed, transcription)
                accumulated_audio = []
                is_speaking = False
                silence_frames = 0

    def _append_transcript(self, elapsed: str, text: str) -> None:
        """
        Acrescenta uma linha transcrita ao arquivo de transcript da sessão.

        Args:
            elapsed (str): Timestamp formatado desde o início da sessão.
            text (str): Texto transcrito.

        Returns:
            None
        """
        with open(self._transcript_path, "a", encoding="utf-8") as f:
            f.write(f"[{elapsed}] {text}\n")

if __name__ == "__main__":
    pass
