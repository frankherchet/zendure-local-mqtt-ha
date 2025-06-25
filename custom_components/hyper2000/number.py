import json
import logging
from homeassistant.components.mqtt import async_publish, async_subscribe
from homeassistant.components.number import NumberEntity
from .const import DOMAIN, WRITABLE_KEYS

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    device_id = entry.data["device_id"]
    topic_reply = f"/Hyper2000/{device_id}/properties/write/reply"

    numbers = [Hyper2000Number(hass, device_id, key, meta["min"], meta["max"]) for key, meta in WRITABLE_KEYS.items()]
    async_add_entities(numbers)

    async def message_received(msg):
        _LOGGER.debug("MQTT write reply: %s", msg.payload)

    await async_subscribe(hass, topic_reply, message_received)

class Hyper2000Number(NumberEntity):
    def __init__(self, hass, device_id, key, min_val, max_val):
        self.hass = hass
        self._device_id = device_id
        self._key = key
        self._state = None
        self._attr_min_value = min_val
        self._attr_max_value = max_val
        self._attr_name = f"Hyper2000 {key}"

    @property
    def value(self):
        return self._state

    async def async_set_value(self, value):
        self._state = value
        topic = f"iot/Hyper2000/{self._device_id}/properties/write"
        payload = json.dumps({"properties": {self._key: value}})
        _LOGGER.debug("Publishing to %s: %s", topic, payload)
        await async_publish(self.hass, topic, payload, qos=1, retain=False)
        self.async_write_ha_state()
