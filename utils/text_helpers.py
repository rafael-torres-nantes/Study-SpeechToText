import logging
import re

logger = logging.getLogger(__name__)

class TextHelpers:
    """Funções auxiliares de manipulação de texto, sem estado."""

    _WHISPER_ARTIFACTS = [r"\[BLANK_AUDIO\]", r"\[SILENCE\]", r"\(silence\)", r"\[.*?\]"]

    @staticmethod
    def clean_transcription(text: str) -> str:
        """
        Remove artefatos comuns do Whisper e normaliza espaçamento.

        Args:
            text (str): Texto bruto retornado pela transcrição.

        Returns:
            str: Texto limpo, sem marcadores como "[BLANK_AUDIO]" e sem espaços duplicados.
        """
        for artifact in TextHelpers._WHISPER_ARTIFACTS:
            text = re.sub(artifact, "", text, flags=re.IGNORECASE)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    @staticmethod
    def format_timestamp(seconds: float) -> str:
        """
        Formata uma duração em segundos como string "HH:MM:SS".

        Args:
            seconds (float): Duração em segundos.

        Returns:
            str: Duração formatada, ex: "01:01:01".
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
