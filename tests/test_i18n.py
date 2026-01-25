#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for i18n module.
"""

import unittest
import os
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent / 'src'
sys.path.insert(0, str(src_path))

from i18n import initialize_i18n, t, _get_language_from_env, DEFAULT_LANGUAGE


class TestI18nLanguageDetection(unittest.TestCase):
    """Tests for language detection."""
    
    def setUp(self) -> None:
        """Save original language."""
        self.original_lang = os.getenv('LANGUAGE')
    
    def tearDown(self) -> None:
        """Restore original language."""
        if self.original_lang:
            os.environ['LANGUAGE'] = self.original_lang
        elif 'LANGUAGE' in os.environ:
            del os.environ['LANGUAGE']
        # Reinitialize with original settings
        initialize_i18n()
    
    def test_default_language(self) -> None:
        """Test default language is Spanish."""
        self.assertEqual(DEFAULT_LANGUAGE, 'es')
    
    def test_get_language_spanish(self) -> None:
        """Test getting Spanish language from env."""
        for lang_value in ['es', 'español', 'spanish', 'ESP']:
            os.environ['LANGUAGE'] = lang_value
            result = _get_language_from_env()
            self.assertEqual(result, 'es', f"Failed for: {lang_value}")
    
    def test_get_language_english(self) -> None:
        """Test getting English language from env."""
        for lang_value in ['en', 'english', 'inglés', 'ENG']:
            os.environ['LANGUAGE'] = lang_value
            result = _get_language_from_env()
            self.assertEqual(result, 'en', f"Failed for: {lang_value}")
    
    def test_get_language_unknown(self) -> None:
        """Test unknown language defaults to Spanish."""
        os.environ['LANGUAGE'] = 'unknown'
        result = _get_language_from_env()
        self.assertEqual(result, 'es')


class TestI18nInitialization(unittest.TestCase):
    """Tests for i18n initialization."""
    
    def test_initialize_spanish(self) -> None:
        """Test initializing with Spanish."""
        initialize_i18n('es')
        result = t('menu.welcome')
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, 'menu.welcome')
    
    def test_initialize_english(self) -> None:
        """Test initializing with English."""
        initialize_i18n('en')
        result = t('menu.welcome')
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, 'menu.welcome')
    
    def test_initialize_invalid_language(self) -> None:
        """Test initializing with invalid language falls back."""
        initialize_i18n('invalid')
        result = t('menu.welcome')
        self.assertIsInstance(result, str)


class TestI18nTranslation(unittest.TestCase):
    """Tests for translation function."""
    
    def setUp(self) -> None:
        """Initialize i18n with Spanish."""
        initialize_i18n('es')
    
    def test_simple_translation(self) -> None:
        """Test simple translation."""
        result = t('menu.welcome')
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)
    
    def test_nested_translation(self) -> None:
        """Test nested translation with dot notation."""
        result = t('error.title')
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)
    
    def test_missing_key(self) -> None:
        """Test missing translation key returns key itself."""
        result = t('nonexistent.key.path')
        self.assertEqual(result, 'nonexistent.key.path')
    
    def test_translation_with_params(self) -> None:
        """Test translation with format parameters."""
        result = t('log.version', version='1.0.0')
        self.assertIsInstance(result, str)
        self.assertIn('1.0.0', result)
    
    def test_translation_with_missing_params(self) -> None:
        """Test translation with missing format parameters."""
        result = t('log.version')
        self.assertIsInstance(result, str)
    
    def test_incomplete_path(self) -> None:
        """Test incomplete translation path."""
        result = t('menu')
        self.assertEqual(result, 'menu')


class TestI18nBothLanguages(unittest.TestCase):
    """Tests to verify both language files work."""
    
    def test_spanish_translations(self) -> None:
        """Test Spanish translations are loaded."""
        initialize_i18n('es')
        keys_to_test = [
            'menu.welcome',
            'error.title',
            'dialog.exit_option'
        ]
        for key in keys_to_test:
            result = t(key)
            self.assertNotEqual(result, key, f"Missing Spanish translation for: {key}")
    
    def test_english_translations(self) -> None:
        """Test English translations are loaded."""
        initialize_i18n('en')
        keys_to_test = [
            'menu.welcome',
            'error.title',
            'dialog.exit_option'
        ]
        for key in keys_to_test:
            result = t(key)
            self.assertNotEqual(result, key, f"Missing English translation for: {key}")


if __name__ == '__main__':
    unittest.main()
