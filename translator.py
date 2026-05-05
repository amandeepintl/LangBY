"""
Langby - Translation Engine
Cached GoogleTranslator for fast, instant translation.
"""

from deep_translator import GoogleTranslator

# Cache translator instances by target language to avoid re-init overhead
_cache = {}


def translate(text, target_lang):
    """
    Translate text to the target language.
    Uses cached translator instances for speed.
    """
    if not text or not text.strip():
        return None

    try:
        # Reuse translator if same target language
        if target_lang not in _cache:
            _cache[target_lang] = GoogleTranslator(source='auto', target=target_lang)

        result = _cache[target_lang].translate(text.strip())
        return result
    except Exception as e:
        # Clear cache on error (might be stale session)
        _cache.pop(target_lang, None)
        print(f"[Langby] Translation error: {e}")
        return None
