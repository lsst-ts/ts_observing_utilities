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
import sys

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"

COLORS = {
    "WARNING": YELLOW,
    "INFO": WHITE,
    "DEBUG": BLUE,
    "CRITICAL": RED,
    "ERROR": RED,
}


class DecoratedLogger(logging.Formatter):
    """
    Custom log formatter inspired on Jupyter's logging messages.

    Parameters
    ----------
    fmt : str, optional
        Log format.
    use_colors : bool (True).
        Print colored messages?
    """

    def __init__(
        self,
        fmt=" [%(levelname).1s %(asctime)s %(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        use_colors=True,
    ):
        logging.Formatter.__init__(self, fmt, datefmt=datefmt)
        self.use_colors = use_colors

    @staticmethod
    def color_format(message, level_name, left_char="[", right_char="]"):
        """
        Replaces part of the output message with characters that start and end
        the colored string.

        Parameters
        ----------
        message : str
            Logging message.
        level_name : str
            Logging level name as a string.
        left_char : str, optional
            Left character that encapsulates the left side of the part that
            will be colored. Default: "[".
        right_char : str, optional
            Right character that encapsulates the right side of the part that
            will be colored. Default: "[".

        Returns
        -------
        str : message containing the special characters that enable colors.
        """
        colour = COLOR_SEQ % (30 + COLORS[level_name])

        message = message.replace(left_char, "{:s} {:s}".format(colour, left_char))
        message = message.replace(right_char, "{:s} {:s}".format(right_char, RESET_SEQ))

        return message

    def format(self, record):
        """
        Override the default logging format.

        See also
        --------
        https://docs.python.org/3/library/logging.html#logging.Formatter.format
        """
        # Call the original formatter class to do the grunt work
        result = logging.Formatter.format(self, record)

        if self.use_colors:
            result = self.color_format(result, record.levelname)

        return result

    @classmethod
    def get_decorated_logger(cls, logger_name=None, use_color=True):
        """
        Return a logger with the "logger_name".

        Parameters
        ----------
        logger_name : str, optional
            The logger name to be used in different contexts.
        use_color : bool, optional
            Use colors on Stream Loggers.

        Returns
        ------
        logging.Logger : the logger to be used.
        """
        _logger = logging.getLogger(logger_name)

        message_format = " [%(levelname).1s %(asctime)s %(name)s] %(message)s"
        date_format = "%Y-%m-%d %H:%M:%S"
        formatter = cls(message_format, datefmt=date_format, use_colors=use_color)

        if len(_logger.handlers) == 0:
            handler = logging.StreamHandler(sys.stdout)
            handler.setFormatter(formatter)

            _logger.addHandler(handler)
            _logger.setLevel(logging.DEBUG)
        else:
            for handler in _logger.handlers:
                handler.setFormatter(formatter)

        return _logger
