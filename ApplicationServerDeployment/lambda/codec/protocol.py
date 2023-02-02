# Copyright 2023 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

"""
Sidewalk Sensor Monitoring Application - protocol constants.
"""

from enum import Enum


class OpCode(Enum):
    """
    Represents Operation Code values.
    """
    MSG_TYPE_READ = '00'
    MSG_TYPE_WRITE = '01'
    MSG_TYPE_NOTIFY = '10'
    MSG_TYPE_RESP = '11'


class Class(Enum):
    """
    Represents Command Class values.
    """
    DEMO_APP_CLASS = '00'
    DEMO_APP_CLASS_CUSTOM = '01'


class ClassCmdId(Enum):
    """
    Represents Class Command Id subsets.
    """
    DEMO_APP_CLASS_CMD_CAP_DISCOVERY_ID = '000'
    DEMO_APP_CLASS_CMD_ACTION = '001'
    DEMO_APP_CUSTOM_CMD_DATA = '000'


class NormalId(Enum):
    """
    Represents Command Id values.
    """
    DEMO_APP_CAP_DISCOVERY_NOTIFICATION = '010'
    DEMO_APP_CAP_DISCOVERY_RESP = '011'
    DEMO_APP_ACTION_REQ = '101'
    DEMO_APP_ACTION_NOTIFICATION = '110'
    DEMO_APP_ACTION_RESP = '111'


class CustomId(Enum):
    DEMO_APP_CUSTOM_DATA_REQ = '001'
    DEMO_APP_CUSTOM_DATA_RESP = '011'
    DEMO_APP_CUSTOM_DATA_NOTIFICATION = '010'


class TagType(Enum):
    """
    Represents Tag Type values.
    """
    NUMBER_OF_BUTTONS = '000001'
    NUMBER_OF_LEDS = '000010'
    LED_ON = '000011'
    LED_OFF = '000100'
    BUTTON_PRESS = '000101'
    TEMP_SENSOR_DATA = '000110'
    CURRENT_GPS_TIME_IN_SECS = '000111'
    DL_LATENCY_IN_SECS = '001000'
    LED_ON_RESP = '001001'
    LED_OFF_RESP = '001010'
    TEMP_SENSOR_AVAILABLE_AND_UNIT_REPRESENTATION = '001011'
    LINK_TYPE = '001100'
    BUTTON_PRESSED_RESP = '001101'
    CUSTOM_DATA = '001110'


class TlvFormat(Enum):
    """
    Represents Tag-Length-Value format values.
    """
    SIZE_OPTIMIZED_1B = '00'
    SIZE_OPTIMIZED_2B = '01'
    SIZE_OPTIMIZED_4B = '10'
    STANDARD = '11'


class LinkType(Enum):
    """
    Represents Link Type values.
    """
    BLE = '00000001'
    FSK = '00000010'
    LORA = '00000100'


class SensorUnits(Enum):
    """
    Represents Temperature Sensor unit values.
    """
    CELSIUS = '0'
    FAHRENHEIT = '1'


"""
Maps Class Cmd Ids to Id subsets.
"""
DefaultIdToCmdIdValueMap = {
    NormalId.DEMO_APP_CAP_DISCOVERY_NOTIFICATION: ClassCmdId.DEMO_APP_CLASS_CMD_CAP_DISCOVERY_ID.value,
    NormalId.DEMO_APP_CAP_DISCOVERY_RESP: ClassCmdId.DEMO_APP_CLASS_CMD_CAP_DISCOVERY_ID.value,
    NormalId.DEMO_APP_ACTION_REQ: ClassCmdId.DEMO_APP_CLASS_CMD_ACTION.value,
    NormalId.DEMO_APP_ACTION_RESP: ClassCmdId.DEMO_APP_CLASS_CMD_ACTION.value,
    NormalId.DEMO_APP_ACTION_NOTIFICATION: ClassCmdId.DEMO_APP_CLASS_CMD_ACTION.value,
}

CustomIdToCmdIdValueMap = {
    CustomId.DEMO_APP_CUSTOM_DATA_REQ: ClassCmdId.DEMO_APP_CUSTOM_CMD_DATA.value,
    CustomId.DEMO_APP_CUSTOM_DATA_RESP: ClassCmdId.DEMO_APP_CUSTOM_CMD_DATA.value,
    CustomId.DEMO_APP_CUSTOM_DATA_NOTIFICATION: ClassCmdId.DEMO_APP_CUSTOM_CMD_DATA.value,
}

ClassToIdValueMap = {
    Class.DEMO_APP_CLASS: DefaultIdToCmdIdValueMap,
    Class.DEMO_APP_CLASS_CUSTOM: CustomIdToCmdIdValueMap,
}

ClassValueToIdValueMap = {
    Class.DEMO_APP_CLASS.value: DefaultIdToCmdIdValueMap,
    Class.DEMO_APP_CLASS_CUSTOM.value: CustomIdToCmdIdValueMap,
}

ClassToIdMap = {
    Class.DEMO_APP_CLASS.value: NormalId,
    Class.DEMO_APP_CLASS_CUSTOM.value: CustomId,
}


