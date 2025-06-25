import json
import logging
from homeassistant.components.mqtt import async_subscribe
from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN, READ_ONLY_KEYS

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    device_id = entry.data["device_id"]
    topic = f"/Hyper2000/{device_id}/properties/report"

    sensors = [Hyper2000Sensor(device_id, key) for key in READ_ONLY_KEYS]
    async_add_entities(sensors)

    async def message_received(msg):
        _LOGGER.debug("MQTT report received: %s", msg.payload)
        payload = json.loads(msg.payload)
        props = payload.get("properties", {})
        for sensor in sensors:
            if sensor._key in props:
                sensor.update_value(props[sensor._key])

    await async_subscribe(hass, topic, message_received)

class Hyper2000Sensor(SensorEntity):
    def __init__(self, device_id, key):
        self._device_id = device_id
        self._key = key
        self._state = None
        self._attr_name = f"Hyper2000 {key}"

    @property
    def state(self):
        return self._state

    def update_value(self, value):
        self._state = value
        self.schedule_update_ha_state()
