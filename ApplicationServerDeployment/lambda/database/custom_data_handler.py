# Copyright 2023 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import boto3

from custom_data import CustomData


class CustomDataHandler:
    """
    A class that provides read and write methods for the Measurements table.
    """

    DATABASE_NAME = 'SidewalkTimestream'
    TABLE_NAME = 'CustomData'

    def __init__(self):

        self._boto3_write_client = boto3.client('timestream-write')

    # -----------------
    # Write operations
    # -----------------
    def add_custom_data(self, custom_data: CustomData):
        """
        Writes CustomData object into the CustomData table.

        :param custom_data: CustomData object.
        """
        self._boto3_write_client.write_records(
            DatabaseName=self.DATABASE_NAME,
            TableName=self.TABLE_NAME,
            Records=[
                {
                    'Time': str(custom_data.get_time()),
                    'TimeUnit': 'MILLISECONDS',
                    'Dimensions': [
                        {
                            'Name': 'wireless_device_id',
                            'Value': custom_data.get_wireless_device_id()
                        }
                    ],
                    'MeasureName': "custom_data",
                    'MeasureValue': str(custom_data.get_value()),
                    'MeasureValueType': 'VARCHAR'
                }
            ]
        )
