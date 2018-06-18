import pytest


from app.schemas import get_language


class TestSchema:
    @pytest.mark.parametrize('lang_in, lang_out', [
        (None, 'pt-br'),
        ('fr-be', 'pt-br'),
        ('ja-jp', 'pt-br'),
        ('es-sp', 'es-ar'),
        ('es-ar', 'es-ar'),
    ])
    def test_get_language(self, lang_in, lang_out):
        assert get_language(lang_in) == lang_out
