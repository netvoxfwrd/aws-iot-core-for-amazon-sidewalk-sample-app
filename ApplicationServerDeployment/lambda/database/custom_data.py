# Copyright 2023 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

from datetime import datetime, timezone

from typing import final


@final
class CustomData(object):
    """
    A class that represents the CustomData table record.

    Attributes
    ----------
        _wireless_device_id: str
            Measurement source.
        _sensor: int
            Custom sensor data stored as a int.
        _temp: int
            Custom sensor temperature stored as a int.
        _time: int
            UTC time in seconds.
    """

    def __init__(self, wireless_device_id, sensor: int = 0, temp: int = 0, time: int = -1):
        self._wireless_device_id = wireless_device_id
        self._value = ""
        self._sensor = sensor
        self._temp = temp

        if time < 0:
            time_now = datetime.now(timezone.utc).timestamp()
            self._time = int(round(time_now * 1000))
        else:
            self._time = time

    def get_data_from_string(self, value: str = ""):
        self._value = value
        assert len(self._value) == 24, "Custom data format needs to be changed"

        # Custom data format
        # 2B (sensor) + 1B (internal temp)
        self._sensor = int(value[:16], 2)
        self._temp = int(value[16: 24], 2)

    def get_wireless_device_id(self) -> str:
        return self._wireless_device_id

    def set_sensor(self, sensor: int):
        self._sensor = sensor

    def set_temp(self, temp: int):
        self._temp = temp

    def get_sensor(self) -> str:
        return str(self._sensor)

    def get_temp(self) -> str:
        return str(self._temp)

    def get_time(self) -> int:
        return self._time

    def _bin2hex(self, binary: str):
        _he = int(binary, 2)
        _he = hex(_he)[2:]
        return _he.zfill(len(binary) // 4)

    def __str__(self):
        return f"Custom payload-  sensor: {self._sensor}, temp: {self._temp}, time: {self._time}"

    def to_dict(self) -> dict:
        """
        Returns dict representation of the Custom Data object.

        :return:    Dict representation of the Custom Data.
        """
        return {
            "wireless_device_id": self._wireless_device_id,
            "sensor": self.get_sensor(),
            "temperature": self.get_temp(),
            "time": self.get_time(),
        }
