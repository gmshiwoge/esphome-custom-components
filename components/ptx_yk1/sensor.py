import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor, esp32_ble_tracker
from esphome.const import (
    CONF_MAC_ADDRESS,
    CONF_TIMEOUT,
)

DEPENDENCIES = ["esp32_ble_tracker"]

ptx_yk1_ns = cg.esphome_ns.namespace("ptx_yk1")
PTXYK1Device = ptx_yk1_ns.class_(
    "PTXYK1Device",
    sensor.Sensor,
    cg.Component,
    esp32_ble_tracker.ESPBTDeviceListener,
)

CONFIG_SCHEMA = cv.All(
    sensor.sensor_schema(PTXYK1Device)  # 使用 sensor 而不是 binary_sensor
    .extend(
        {
            cv.Required(CONF_MAC_ADDRESS): cv.mac_address,
            cv.Optional(
                CONF_TIMEOUT, default="300ms"
            ): cv.positive_time_period_milliseconds,
        }
    )
    .extend(esp32_ble_tracker.ESP_BLE_DEVICE_SCHEMA)
    .extend(cv.COMPONENT_SCHEMA),
)


async def to_code(config):
    var = await sensor.new_sensor(config)  # 使用 sensor.new_sensor 而不是 binary_sensor
    await cg.register_component(var, config)
    await esp32_ble_tracker.register_ble_device(var, config)
    cg.add(var.set_address(config[CONF_MAC_ADDRESS].as_hex))
    cg.add(var.set_timeout_ms(config[CONF_TIMEOUT]))
