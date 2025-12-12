# netft_py

This is a Python API for RDT communication with ATI Force/Torque sensors using Net-F/T interface boxes. This library
supports requesting single measurements, streaming measurements, taring the sensor, _and gravity compensation_.

## Installation

Install via `pip install -e .` from repository root.

## Usage

```python
from netft_py import NetFT

netft = NetFT(ip="192.168.1.33")
```

The `NetFT` class can be used to get individual measurements or continuously stream:

#### Individual Measurements:
```python
wrench = netft.getMeasurement()  # Get single measurement
wrenches = netft.getMeasurements(n=5)  # Get multiple measurements

force = netft.getForce() # Get only force component
torque = netft.getTorque() # Get only torque component
```

#### Streaming Measurements:
```python
netft.startStreaming()

# Then read the latest wrench feedback using the following:
wrench = netft.measurement()
```

In practice, the data comes in at ~500Hz.

#### Taring the sensor:
```python
netft.tare(n=100)  # Tare using 100 samples
```

To "reset" the tare and return to raw measurements:
```python
netft.zero()
```

### Scripts:

You can use the `vis_netft.py` script in the `scripts/` folder to visualize wrench data in real-time.
```bash
python scripts/vis_netft.py 192.168.1.33
```

## Credit

This library forks and modifies code from the [NetFT](https://github.com/CameronDevine/NetFT) repository by 
Cameron Devine.
