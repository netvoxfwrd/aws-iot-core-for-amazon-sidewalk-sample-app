# Copyright 2023 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
import traceback
from datetime import datetime, timezone

import boto3

from custom_data import CustomData


class CustomDataHandler:
    """
    A class that provides read and write methods for the Measurements table.
    """

    DATABASE_NAME = "SidewalkTimestream"
    TABLE_NAME = "CustomData"
    CUSTOM_DATA_SENSOR = "custom_data_sensor"
    CUSTOM_DATA_TEMP = "custom_data_temp"

    def __init__(self):
        self._boto3_query_client = boto3.client('timestream-query')
        self._boto3_write_client = boto3.client("timestream-write")

    # -----------------
    # Write operations
    # -----------------
    def add_custom_data(self, custom_data: CustomData):
        """
        Writes CustomData object into the CustomData table.

        :param custom_data: CustomData object.
        """
        try:
            self._boto3_write_client.write_records(
                DatabaseName=self.DATABASE_NAME,
                TableName=self.TABLE_NAME,
                Records=[
                    {
                        "Time": str(custom_data.get_time()),
                        "TimeUnit": "MILLISECONDS",
                        "Dimensions": [
                            {
                                "Name": "wireless_device_id",
                                "Value": custom_data.get_wireless_device_id(),
                            }
                        ],
                        "MeasureName": "custom_data_sensor",
                        "MeasureValue": str(custom_data.get_sensor()),
                        "MeasureValueType": "DOUBLE",
                    },
                    {
                        "Time": str(custom_data.get_time()),
                        "TimeUnit": "MILLISECONDS",
                        "Dimensions": [
                            {
                                "Name": "wireless_device_id",
                                "Value": custom_data.get_wireless_device_id(),
                            }
                        ],
                        "MeasureName": "custom_data_temp",
                        "MeasureValue": str(custom_data.get_temp()),
                        "MeasureValueType": "DOUBLE",
                    },
                ],
            )
        except self._boto3_write_client.exceptions.RejectedRecordsException as err:
            self._print_rejected_records_exceptions(err)
        except Exception as err:
            print("Error:", err)

    def get_custom_data(
            self, wireless_device_id: str, time_range_start: int, time_range_end: int
    ) -> [CustomData]:
        """
        Queries CustomData table for the records coming from given device withing a given time span.

        :param wireless_device_id:  Id of the wireless device.
        :param time_range_start:    Start time (UTC time in seconds).
        :param time_range_end:      End time (UTC time in seconds).
        :return:                    List of CustomData objects.
        """
        query = "SELECT * " \
                "FROM \"SidewalkTimestream\".\"CustomData\" " \
                "WHERE \"wireless_device_id\" = '{}' AND time between '{}' AND '{}'"
        return self._run_query(
            query.format(
                wireless_device_id,
                datetime.fromtimestamp(time_range_start, tz=timezone.utc),
                datetime.fromtimestamp(time_range_end, tz=timezone.utc)
            )
        )

    # -----------------
    # For internal use
    # -----------------
    def _run_query(self, query: str) -> [CustomData]:
        custom_data: {int, CustomData} = {}
        try:
            pages = []
            paginator = self._boto3_query_client.get_paginator('query')
            page_iterator = paginator.paginate(QueryString=query)
            for page in page_iterator:
                pages.append(page)

            for page in pages:
                wireless_device_id_position = None
                time_position = None
                measure_value_position = None
                measure_name_position = None

                column_info = page['ColumnInfo']

                for position, column in enumerate(column_info):
                    name = column['Name']

                    if name == 'wireless_device_id':
                        wireless_device_id_position = position
                    elif name == 'time':
                        time_position = position
                    elif name == 'measure_value::double':
                        measure_value_position = position
                    elif name == 'measure_name':
                        measure_name_position = position


                rows = page['Rows']
                for row in rows:
                    data: list = row['Data']
                    wireless_device_id: str = ""
                    timestamp = 0

                    if 'ScalarValue' in data[wireless_device_id_position]:
                        wireless_device_id = data[wireless_device_id_position]['ScalarValue']


                    if 'ScalarValue' in data[time_position]:
                        timestamp = int(round(
                            datetime.strptime(data[time_position]['ScalarValue'][:-3], "%Y-%m-%d %H:%M:%S.%f")
                            .replace(tzinfo=timezone.utc)
                            .timestamp() * 1000
                        ))


                    #custom_data_point: CustomData = CustomData(wireless_device_id, measure_value, timestamp)
                    custom_data_point: CustomData = custom_data.get(timestamp, CustomData(wireless_device_id, time=timestamp))

                    if 'ScalarValue' in data[measure_value_position] and 'ScalarValue' in data[measure_name_position]:
                        if data[measure_name_position]["ScalarValue"] == self.CUSTOM_DATA_SENSOR:
                            sensor_value = data[measure_value_position]['ScalarValue']
                            custom_data_point.set_sensor(sensor_value)

                        elif data[measure_name_position]["ScalarValue"] == self.CUSTOM_DATA_TEMP:
                            sensor_value = data[measure_value_position]['ScalarValue']
                            custom_data_point.set_temp(sensor_value)
                        else:
                            raise Exception(f'Custom data object: {data[measure_name_position]["ScalarValue"]} is not supported. ' +
                                  f'Supported objects {self.CUSTOM_DATA_TEMP}  and {self.CUSTOM_DATA_SENSOR}')

                    custom_data[timestamp] = custom_data_point
        except Exception:
            print(f'Unexpected error occurred while fetching measurements: {traceback.format_exc()}')

        return list(custom_data.values())


    @staticmethod
    def _print_rejected_records_exceptions(err):
        print("RejectedRecords: ", err)
        for rr in err.response["RejectedRecords"]:
            print("Rejected Index " + str(rr["RecordIndex"]) + ": " + rr["Reason"])
            if "ExistingVersion" in rr:
                print("Rejected record existing version: ", rr["ExistingVersion"])
