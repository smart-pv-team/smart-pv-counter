import datetime
import datetime as dt
import os

import pymongo as pymongo
from dateutil import tz


class Database:
    def __init__(self):
        self.database_url = os.environ.get("MONGODB_URI")
        self.db = pymongo.MongoClient(self.database_url).smartpv
        self.consumption_entity_collection = self.db.consumptionEntity
        self.consumption_device_entity_collection = self.db.consumptionDeviceEntity
        self.measurement_entity_collection = self.db.measurementEntity
        self.measurement_device_entity_collection = self.db.measurementDeviceEntity

    def get_period_devices_consumption(self, start_date, end_date):
        consumptions = list(map(lambda consumption:
                                (self.__datetime_to_datetime_without_seconds(consumption["date"]),
                                 consumption["activeDevicesIds"],
                                 consumption["farmId"]),
                                self.consumption_entity_collection
                                .find({"date": {'$lt': end_date, '$gt': start_date}})
                                .sort([("date", pymongo.ASCENDING)])))

        consumption_devices = list(
            map(lambda consumptionDevice: (str(consumptionDevice["_id"]), consumptionDevice["farmId"]),
                self.consumption_device_entity_collection.find({})))

        result = {device[0]: {} for device in consumption_devices}

        for consumption in consumptions:
            date = consumption[0]
            active_devices = consumption[1]
            farmId = consumption[2]
            for device in consumption_devices:
                deviceId = device[0]
                deviceFarmId = device[1]
                if deviceFarmId == farmId:
                    result[str(deviceId)][
                        date.strftime('%Y-%m-%dT%H:%M:%S.%f%z')] = True if deviceId in active_devices else False

        return result

    def get_all_devices_consumptions(self):
        return self.get_period_devices_consumption(datetime.datetime.min, datetime.datetime.max)

    def get_all_devices_measurements(self):
        return self.get_period_devices_measurements(datetime.datetime.min, datetime.datetime.max)

    def get_period_devices_measurements(self, start_date, end_date):
        measurements = list(map(lambda measurement:
                                (self.__datetime_to_datetime_without_seconds(measurement["date"]),
                                 measurement["measurements"]),
                                self.measurement_entity_collection
                                .find({"date": {'$lt': end_date, '$gt': start_date}})
                                .sort([("date", pymongo.ASCENDING)])))

        measurement_devices = list(map(lambda measurementDevice: str(measurementDevice["_id"]),
                                       self.measurement_device_entity_collection.find({})))

        result = {device: {} for device in measurement_devices}

        for measurement in measurements:
            date = measurement[0]
            for record in measurement[1].items():
                device = str(record[0])
                value = record[1]
                result[device][date.strftime('%Y-%m-%dT%H:%M:%S.%f%z')] = value

        return result

    def __datetime_to_datetime_without_seconds(self, date: dt.datetime):
        return dt.datetime(date.year, date.month, date.day, date.hour, date.minute, 0, 0, tzinfo=tz.UTC)
