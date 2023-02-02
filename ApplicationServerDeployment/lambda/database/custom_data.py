# Copyright 2023 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import time

from typing import final


@final
class CustomData(object):
    """
    A class that represents the CustomData table record.

    Attributes
    ----------
        _wireless_device_id: str
            Measurement source.
        _value: str
            Custom data stored as a string.
        _time: int
            UTC time in seconds.
    """

    def __init__(self, wireless_device_id, value: str = '', time: int = 0):
        self._wireless_device_id = wireless_device_id
        self._time = time if time != 0 else self._get_gps_time();
        self._value = hex(int(value, 2))

    def get_wireless_device_id(self) -> str:
        return self._wireless_device_id

    def get_value(self) -> str:
        return str(self._value)

    def get_time(self) -> int:

        return self._time

    def _get_gps_time(self) -> int:
        """ 
        Return gps time
        """

        return int(time.time() - 315964782)

    def to_dict(self) -> dict:
        """
        Returns dict representation of the Measurement object.

        :return:    Dict representation of the Measurement.
        """
        return {
                'wireless_device_id': self._wireless_device_id,
                'value': self.get_value(),
                'time': self.get_time()
            }
