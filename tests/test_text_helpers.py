from utils.text_helpers import TextHelpers


def test_clean_transcription_removes_whisper_artifacts():
    assert TextHelpers.clean_transcription("[BLANK_AUDIO]") == ""
    assert TextHelpers.clean_transcription("Hello [SILENCE] world") == "Hello world"
    assert TextHelpers.clean_transcription("(silence) Hi there") == "Hi there"


def test_clean_transcription_removes_generic_bracket_tags():
    assert TextHelpers.clean_transcription("Hello [music] world") == "Hello world"


def test_clean_transcription_collapses_whitespace():
    assert TextHelpers.clean_transcription("  Hello    world  ") == "Hello world"


def test_clean_transcription_preserves_normal_text():
    assert TextHelpers.clean_transcription("How are you doing today?") == "How are you doing today?"


def test_format_timestamp():
    assert TextHelpers.format_timestamp(3661) == "01:01:01"
    assert TextHelpers.format_timestamp(59) == "00:00:59"
