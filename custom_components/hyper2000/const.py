DOMAIN = "hyper2000"

READ_ONLY_KEYS = [
    "solarInputPower",
    "solarPower1",
    "solarPower2",
    "outputPackPower",
    "packInputPower",
]

WRITABLE_KEYS = {
    "acMode": {"min": 1, "max": 2},
    "inverseMaxPower": {"min": 0, "max": 1200},
    "inputLimit": {"min": 0, "max": 5000},
    "outputLimit": {"min": 0, "max": 5000},
}
