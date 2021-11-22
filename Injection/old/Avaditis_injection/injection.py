from Injection.old.Avaditis_injection.amplitude_shift_injector import AmplitudeShiftInjector
from Injection.old.Avaditis_injection.distortion_injector import DistortionInjector
from Injection.old.Avaditis_injection.growth_injector import GrowthInjector
from Injection.old.Avaditis_injection.missing_values_injector import MissingValuesInjector
from Injection.old.Avaditis_injection.point_injector import ExtremeValueInjector
from base import get_datasets_from_json
from myparameters import ANOMALY_TYPE_POINT, ANOMALY_TYPE_AMPLITUDE_SHIFT, ANOMALY_TYPE_DISTORTION, \
    ANOMALY_TYPE_GROWTH_CHANGE, ANOMALY_TYPE_MISSING_VALUES


def anomaly_injection(validated_data):

    anomaly_type = validated_data['anomaly_type']

    if anomaly_type == ANOMALY_TYPE_POINT:
        injector = ExtremeValueInjector(validated_data)
        injector.inject_outliers()
        return injector.get_injection_datasets()

    elif anomaly_type == ANOMALY_TYPE_AMPLITUDE_SHIFT:
        injector = AmplitudeShiftInjector(validated_data)
        injector.inject_outliers()
        return injector.get_injection_datasets()

    elif anomaly_type == ANOMALY_TYPE_GROWTH_CHANGE:
        injector = GrowthInjector(validated_data)
        injector.inject_outliers()
        return injector.get_injection_datasets()

    elif anomaly_type == ANOMALY_TYPE_DISTORTION:
        injector = DistortionInjector(validated_data)
        injector.inject_outliers()
        return injector.get_injection_datasets()

    elif anomaly_type == ANOMALY_TYPE_MISSING_VALUES:
        injector = MissingValuesInjector(validated_data)
        injector.inject_outliers()
        return injector.get_injection_datasets()

    else:
        #logging.error("Unknown anomaly type, will return original datasets")
        df_from_json, df_class_from_json = get_datasets_from_json(validated_data['dataset_series_json'])
        return df_from_json, df_class_from_json
