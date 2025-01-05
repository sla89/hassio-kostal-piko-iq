from homeassistant.components.sensor import (SensorDeviceClass,
                                             SensorEntityDescription,
                                             SensorStateClass)

from homeassistant.const import (UnitOfEnergy, UnitOfMass)

class KostalSensorEntityDescription():
    """A class that describes Kostal entities."""

    description = None
    module_id = None
    value_id = None

    def __init__(self, description, module_id, value_id):
        self.description = description
        self.module_id = module_id
        self.value_id = value_id


SENSOR_DESCRIPTIONS: tuple[KostalSensorEntityDescription, ...] = (
    KostalSensorEntityDescription(
        description=SensorEntityDescription(
            key="kostal_generator",
            name="Kostal Generator",
            device_class=SensorDeviceClass.ENERGY,
            state_class=SensorStateClass.MEASUREMENT,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            icon="mdi:solar-panel"
        ),
        module_id="devices:local",
        value_id="Dc_P",
    ),
    KostalSensorEntityDescription(
        description=SensorEntityDescription(
            key="kostal_inverter",
            name="Kostal Inverter",
            device_class=SensorDeviceClass.ENERGY,
            state_class=SensorStateClass.MEASUREMENT,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            icon="mdi:solar-power"
        ),
        module_id="devices:local:ac",
        value_id="P",
    ),
    KostalSensorEntityDescription(
        description=SensorEntityDescription(
            key="kostal_yield_day",
            name="Kostal Yield Day",
            device_class=SensorDeviceClass.ENERGY,
            state_class=SensorStateClass.TOTAL_INCREASING,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            icon="mdi:power-plug"
        ),
        module_id="scb:statistic:EnergyFlow",
        value_id="Statistic:Yield:Day",
    ),
    KostalSensorEntityDescription(
        description=SensorEntityDescription(
            key="kostal_yield_month",
            name="Kostal Yield Month",
            device_class=SensorDeviceClass.ENERGY,
            state_class=SensorStateClass.TOTAL_INCREASING,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            icon="mdi:power-plug"
        ),
        module_id="scb:statistic:EnergyFlow",
        value_id="Statistic:Yield:Month",
    ),
    KostalSensorEntityDescription(
        description=SensorEntityDescription(
            key="kostal_yield_total",
            name="Kostal Yield Total",
            device_class=SensorDeviceClass.ENERGY,
            state_class=SensorStateClass.TOTAL_INCREASING,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            icon="mdi:power-plug"
        ),
        module_id="scb:statistic:EnergyFlow",
        value_id="Statistic:Yield:Total",
    ),
    KostalSensorEntityDescription(
        description=SensorEntityDescription(
            key="kostal_yield_year",
            name="Kostal Yield Year",
            device_class=SensorDeviceClass.ENERGY,
            state_class=SensorStateClass.TOTAL_INCREASING,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            icon="mdi:power-plug"
        ),
        module_id="scb:statistic:EnergyFlow",
        value_id="Statistic:Yield:Year",
    ),
    KostalSensorEntityDescription(
        description=SensorEntityDescription(
            key="kostal_co2_saving_day",
            name="Kostal CO2 Saving Day",
            device_class=SensorDeviceClass.CO2,
            state_class=SensorStateClass.TOTAL_INCREASING,
            native_unit_of_measurement=UnitOfMass.GRAMS,
            icon="mdi:molecule-co2"
        ),
        module_id="scb:statistic:EnergyFlow",
        value_id="Statistic:CO2Saving:Day",
    ),
    KostalSensorEntityDescription(
        description=SensorEntityDescription(
            key="kostal_co2_saving_month",
            name="Kostal CO2 Saving Month",
            device_class=SensorDeviceClass.CO2,
            state_class=SensorStateClass.TOTAL_INCREASING,
            native_unit_of_measurement=UnitOfMass.GRAMS,
            icon="mdi:molecule-co2"
        ),
        module_id="scb:statistic:EnergyFlow",
        value_id="Statistic:CO2Saving:Month",
    ),
    KostalSensorEntityDescription(
        description=SensorEntityDescription(
            key="kostal_co2_saving_year",
            name="Kostal CO2 Saving Year",
            device_class=SensorDeviceClass.CO2,
            state_class=SensorStateClass.TOTAL_INCREASING,
            native_unit_of_measurement=UnitOfMass.GRAMS,
            icon="mdi:molecule-co2"
        ),
        module_id="scb:statistic:EnergyFlow",
        value_id="Statistic:CO2Saving:Year",
    ),
    KostalSensorEntityDescription(
        description=SensorEntityDescription(
            key="kostal_co2_saving_total",
            name="Kostal CO2 Saving Total",
            device_class=SensorDeviceClass.CO2,
            state_class=SensorStateClass.TOTAL_INCREASING,
            native_unit_of_measurement=UnitOfMass.GRAMS,
            icon="mdi:molecule-co2"
        ),
        module_id="scb:statistic:EnergyFlow",
        value_id="Statistic:CO2Saving:Total",
    )
)
