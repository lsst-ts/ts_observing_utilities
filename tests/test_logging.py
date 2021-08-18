# This file is part of ts_observing_utilities.
#
# Developed for Vera C. Rubin Observatory Telescope and Site Systems.
# This product includes software developed by the LSST Project
# (https://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import logging
import io
import unittest

from lsst.ts.observing.utilities.logging import get_logger, MyLogFormatter


class TestLogFormat(unittest.TestCase):
    logger_name = 'TestLogFormatApp'
    expected_log_format = r'(\[[D,I,W,E,C]\s\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\s\w*\]\s)'

    def setUp(self):

        self.formatter = MyLogFormatter()
        self.stream = io.StringIO()
        self.handler = logging.StreamHandler(self.stream)
        self.logger = get_logger(self.logger_name)

        for handler in self.logger.handlers:
            self.logger.removeHandler(handler)

        self.handler.setFormatter(self.formatter)

        self.logger.addHandler(self.handler)

    def tearDown(self):
        pass

    def assertLogFormat(self, message, level_name):

        with self.assertLogs(logger=self.logger_name, level=level_name) as cm:

            if not isinstance(level_name, str):
                level_name = logging.getLevelName(level_name)

            if level_name.upper() == 'DEBUG':
                self.logger.debug(message)
            elif level_name.upper() == 'INFO':
                self.logger.info(message)
            elif level_name.upper() == 'WARNING':
                self.logger.warning(message)
            elif level_name.upper() == 'ERROR':
                self.logger.error(message)
            elif level_name.upper() == 'CRITICAL':
                self.logger.critical(message)
            else:
                raise ValueError("level_name = {:} is not valid.".format(level_name))

            self.handler.flush()

            log_message = self.handler.format(cm.records[-1]).strip()
            self.assertRegex(log_message, self.expected_log_format)

    def test_number_of_handlers(self):
        logger = get_logger(self.logger_name)
        self.assertEqual(1, len(logger.handlers))

    def test_debug(self):
        message = 'test debug message'
        self.assertLogFormat(message, 'DEBUG')
        self.assertLogFormat(message, logging.DEBUG)

    def test_info(self):
        message = 'test info message'
        self.assertLogFormat(message, 'INFO')
        self.assertLogFormat(message, logging.INFO)

    def test_warning(self):
        message = 'test warning message'
        self.assertLogFormat(message, 'WARNING')
        self.assertLogFormat(message, logging.WARNING)

    def test_error(self):
        message = 'test error message'
        self.assertLogFormat(message, 'ERROR')
        self.assertLogFormat(message, logging.ERROR)

    def test_critical(self):
        message = 'test critical message'
        self.assertLogFormat(message, 'CRITICAL')
        self.assertLogFormat(message, logging.CRITICAL)

    def test_color(self):
        message = 'test color message'
        with self.assertLogs(logger=self.logger_name) as cm:
            self.logger.warning(message)
            self.handler.flush()

            log_message = self.handler.format(cm.records[-1]).strip()
            self.assertRegex(log_message, r'(\x1b)')
