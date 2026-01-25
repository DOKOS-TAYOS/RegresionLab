#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for logger module.
"""

import unittest
import sys
import logging
import tempfile
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent / 'src'
sys.path.insert(0, str(src_path))

from utils.logger import (
    get_log_level_from_env,
    get_log_file_from_env,
    should_log_to_console,
    setup_logging,
    get_logger,
    log_function_call,
    log_exception,
    ColoredFormatter
)
import os


class TestGetLogLevelFromEnv(unittest.TestCase):
    """Tests for get_log_level_from_env function."""
    
    def setUp(self) -> None:
        """Save original LOG_LEVEL."""
        self.original_level = os.getenv('LOG_LEVEL')
    
    def tearDown(self) -> None:
        """Restore original LOG_LEVEL."""
        if self.original_level:
            os.environ['LOG_LEVEL'] = self.original_level
        elif 'LOG_LEVEL' in os.environ:
            del os.environ['LOG_LEVEL']
    
    def test_default_log_level(self) -> None:
        """Test default log level when env var not set."""
        if 'LOG_LEVEL' in os.environ:
            del os.environ['LOG_LEVEL']
        level = get_log_level_from_env()
        self.assertEqual(level, logging.INFO)
    
    def test_debug_level(self) -> None:
        """Test DEBUG log level."""
        os.environ['LOG_LEVEL'] = 'DEBUG'
        level = get_log_level_from_env()
        self.assertEqual(level, logging.DEBUG)
    
    def test_warning_level(self) -> None:
        """Test WARNING log level."""
        os.environ['LOG_LEVEL'] = 'WARNING'
        level = get_log_level_from_env()
        self.assertEqual(level, logging.WARNING)
    
    def test_error_level(self) -> None:
        """Test ERROR log level."""
        os.environ['LOG_LEVEL'] = 'ERROR'
        level = get_log_level_from_env()
        self.assertEqual(level, logging.ERROR)
    
    def test_case_insensitive(self) -> None:
        """Test that log level is case insensitive."""
        os.environ['LOG_LEVEL'] = 'debug'
        level = get_log_level_from_env()
        self.assertEqual(level, logging.DEBUG)
    
    def test_invalid_level(self) -> None:
        """Test that invalid level defaults to INFO."""
        os.environ['LOG_LEVEL'] = 'INVALID'
        level = get_log_level_from_env()
        self.assertEqual(level, logging.INFO)


class TestGetLogFileFromEnv(unittest.TestCase):
    """Tests for get_log_file_from_env function."""
    
    def setUp(self) -> None:
        """Save original LOG_FILE."""
        self.original_file = os.getenv('LOG_FILE')
    
    def tearDown(self) -> None:
        """Restore original LOG_FILE."""
        if self.original_file:
            os.environ['LOG_FILE'] = self.original_file
        elif 'LOG_FILE' in os.environ:
            del os.environ['LOG_FILE']
    
    def test_default_log_file(self) -> None:
        """Test default log file when env var not set."""
        if 'LOG_FILE' in os.environ:
            del os.environ['LOG_FILE']
        log_file = get_log_file_from_env()
        self.assertEqual(log_file, 'regressionlab.log')
    
    def test_custom_log_file(self) -> None:
        """Test custom log file from env var."""
        os.environ['LOG_FILE'] = 'custom.log'
        log_file = get_log_file_from_env()
        self.assertEqual(log_file, 'custom.log')


class TestShouldLogToConsole(unittest.TestCase):
    """Tests for should_log_to_console function."""
    
    def setUp(self) -> None:
        """Save original LOG_CONSOLE."""
        self.original_console = os.getenv('LOG_CONSOLE')
    
    def tearDown(self) -> None:
        """Restore original LOG_CONSOLE."""
        if self.original_console:
            os.environ['LOG_CONSOLE'] = self.original_console
        elif 'LOG_CONSOLE' in os.environ:
            del os.environ['LOG_CONSOLE']
    
    def test_default_console_logging(self) -> None:
        """Test default console logging when env var not set."""
        if 'LOG_CONSOLE' in os.environ:
            del os.environ['LOG_CONSOLE']
        result = should_log_to_console()
        self.assertTrue(result)
    
    def test_console_true(self) -> None:
        """Test console logging enabled."""
        for value in ['true', 'True', '1', 'yes', 'YES']:
            os.environ['LOG_CONSOLE'] = value
            result = should_log_to_console()
            self.assertTrue(result, f"Failed for value: {value}")
    
    def test_console_false(self) -> None:
        """Test console logging disabled."""
        os.environ['LOG_CONSOLE'] = 'false'
        result = should_log_to_console()
        self.assertFalse(result)


class TestSetupLogging(unittest.TestCase):
    """Tests for setup_logging function."""
    
    def setUp(self) -> None:
        """Create temporary log file."""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.log')
        self.temp_file.close()
        self.temp_log_path = self.temp_file.name
    
    def tearDown(self) -> None:
        """Remove temporary log file."""
        # Clear all handlers
        logger = logging.getLogger()
        logger.handlers.clear()
        
        # Delete temp file
        Path(self.temp_log_path).unlink(missing_ok=True)
    
    def test_setup_with_defaults(self) -> None:
        """Test setup logging with default values."""
        setup_logging(log_file=self.temp_log_path, console=False)
        
        logger = logging.getLogger()
        self.assertGreater(len(logger.handlers), 0)
    
    def test_setup_with_custom_level(self) -> None:
        """Test setup logging with custom level."""
        setup_logging(log_file=self.temp_log_path, level=logging.DEBUG, console=False)
        
        logger = logging.getLogger()
        self.assertEqual(logger.level, logging.DEBUG)
    
    def test_log_file_created(self) -> None:
        """Test that log file is created."""
        setup_logging(log_file=self.temp_log_path, console=False)
        
        self.assertTrue(Path(self.temp_log_path).exists())


class TestGetLogger(unittest.TestCase):
    """Tests for get_logger function."""
    
    def test_get_logger_returns_logger(self) -> None:
        """Test that get_logger returns a logger instance."""
        logger = get_logger('test_module')
        self.assertIsInstance(logger, logging.Logger)
    
    def test_logger_name(self) -> None:
        """Test that logger has correct name."""
        logger = get_logger('test_module')
        self.assertEqual(logger.name, 'test_module')
    
    def test_multiple_loggers(self) -> None:
        """Test getting multiple loggers with different names."""
        logger1 = get_logger('module1')
        logger2 = get_logger('module2')
        
        self.assertNotEqual(logger1.name, logger2.name)


class TestLogFunctionCall(unittest.TestCase):
    """Tests for log_function_call function."""
    
    def test_log_function_call(self) -> None:
        """Test logging a function call."""
        logger = get_logger('test')
        
        # This should not raise an exception
        log_function_call(logger, 'test_function', x=1, y=2, name='test')
    
    def test_log_function_call_no_params(self) -> None:
        """Test logging a function call without parameters."""
        logger = get_logger('test')
        
        # This should not raise an exception
        log_function_call(logger, 'test_function')


class TestLogException(unittest.TestCase):
    """Tests for log_exception function."""
    
    def test_log_exception_with_context(self) -> None:
        """Test logging an exception with context."""
        logger = get_logger('test')
        exception = ValueError("Test error")
        
        # This should not raise an exception
        log_exception(logger, exception, "Test context")
    
    def test_log_exception_without_context(self) -> None:
        """Test logging an exception without context."""
        logger = get_logger('test')
        exception = RuntimeError("Test error")
        
        # This should not raise an exception
        log_exception(logger, exception)


class TestColoredFormatter(unittest.TestCase):
    """Tests for ColoredFormatter class."""
    
    def test_formatter_creation(self) -> None:
        """Test creating a ColoredFormatter."""
        formatter = ColoredFormatter('%(message)s')
        self.assertIsInstance(formatter, ColoredFormatter)
    
    def test_format_log_record(self) -> None:
        """Test formatting a log record."""
        formatter = ColoredFormatter('%(levelname)s - %(message)s')
        record = logging.LogRecord(
            name='test',
            level=logging.INFO,
            pathname='test.py',
            lineno=1,
            msg='Test message',
            args=(),
            exc_info=None
        )
        
        formatted = formatter.format(record)
        self.assertIn('INFO', formatted)
        self.assertIn('Test message', formatted)


if __name__ == '__main__':
    unittest.main()
