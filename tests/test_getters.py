# This file is part of ts_observing_utilities
#
# Developed for the LSST Telescope and Site Systems.
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

import asynctest
import logging
import pathlib

from lsst.ts.observing.utilities.auxtel.latiss.getters import get_image

logging.basicConfig()
# Make matplotlib less chatty
logging.getLogger("matplotlib").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)
logger.propagate = True

# See if data is available from current location
# Expect to run from NCSA test stand

mapper = pathlib.Path("/project/shared/auxTel/_parent/_mapper")

if mapper.exists():
    dataAvailable = True
else:
    dataAvailable = False


@asynctest.skipIf(dataAvailable is False, "No data available")
class TestGetters(asynctest.TestCase):
    async def test_get_image(self):
        day_obs = "2020-03-15"
        seq_num = "139"
        data_id = dict(dayObs=day_obs, seqNum=seq_num)

        # BestEffortISR will run be default
        logger.debug("Starting test with ISR enabled")
        await get_image(
            data_id,
            dataset="raw",  # "quickLookExp",
            datapath="/project/shared/auxTel/",
            timeout=10,
        )
        # Not sure how to assert if things ran properly. If it errors it
        # raises an exception

        logger.debug("Running test of get_image without ISR enabled")
        await get_image(
            data_id,
            runBestEffortIsr=False,
            dataset="raw",  # "quickLookExp",
            datapath="/project/shared/auxTel/",
            timeout=10,
        )
