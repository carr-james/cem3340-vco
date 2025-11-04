# Calibration and Testing

This page describes how to calibrate and test the module after assembly.

## Required Equipment

- Eurorack power supply or bench power supply (±12V)
- Multimeter
- Oscilloscope (recommended)
- Audio signal generator (optional)
- Patch cables

## Power-On Test

!!! danger "First Power-Up"
    Before connecting the module to your eurorack case, perform these checks!

### Visual Inspection

- [ ] Check all solder joints for bridges or cold joints
- [ ] Verify all polarized components are oriented correctly
- [ ] Ensure no components are touching or creating shorts
- [ ] Check that all IC pins are properly seated in sockets

### Power Supply Check

1. **Set up bench power supply:**
   - Configure for ±12V output
   - Set current limit to 100mA per rail (protection)
   - DO NOT connect yet

2. **Measure resistance:**
   - Module unpowered, disconnected
   - Measure resistance between +12V and GND (should be >1kΩ)
   - Measure resistance between -12V and GND (should be >1kΩ)
   - Measure resistance between +12V and -12V (should be >1kΩ)

3. **Connect power:**
   - Connect power cable (RED STRIPE = -12V side)
   - Watch for smoke or excessive current draw
   - Module should draw < 100mA per rail

4. **Measure voltages:**
   - Measure +12V rail at test point or IC pin (should be 11.5-12.5V)
   - Measure -12V rail at test point or IC pin (should be -11.5 to -12.5V)
   - Measure GND reference

## Functional Tests

### Test 1: Power Indicator

- [ ] Power LED lights up (if present)
- [ ] LED is not excessively bright (indicates correct current limiting)

### Test 2: DC Offset Check

With no input signals connected:

1. Power on module
2. Measure DC voltage at each output
3. Should be close to 0V (< 100mV offset acceptable)

If offset is high:
- Check for solder bridges
- Verify op-amp orientation
- Check coupling capacitors

### Test 3: Signal Path

#### Audio Test

1. Connect signal generator to input
2. Set to 440Hz, 1Vpp sine wave
3. Connect oscilloscope to output
4. Verify clean sine wave appears at output
5. Measure amplitude and compare to expected gain

#### Control Voltage Test

1. Apply DC voltage to CV input (e.g., 2V)
2. Measure CV output
3. Verify expected response

### Test 4: Controls

Test each control (pots, switches):

- [ ] Pot 1: Verify smooth adjustment, full range
- [ ] Pot 2: Verify smooth adjustment, full range
- [ ] Switch 1: Verify audible/measurable effect

## Calibration Procedures

### Offset Calibration

If trimmer pots are provided for offset adjustment:

1. Remove all input signals
2. Measure output voltage with multimeter
3. Adjust offset trim pot until output reads 0.000V
4. Repeat for each channel

### Gain Calibration

If gain trim pots are provided:

1. Apply known reference voltage to input (e.g., 1.000V)
2. Measure output voltage
3. Adjust gain trim pot to achieve desired output
4. For unity gain: output should equal input
5. For 2x gain: output should be 2x input

### V/Oct Calibration (for oscillators)

If module has V/Oct tracking:

1. Apply 0V to V/Oct input
2. Adjust offset so output is exactly 440Hz (A4)
3. Apply 1V to V/Oct input
4. Adjust scale so output is exactly 880Hz (A5)
5. Repeat steps 2-4 until both are accurate
6. Test at different octaves to verify tracking

## Typical Measurements

### Current Draw

Expected current consumption:

| Rail | Typical | Maximum |
|------|---------|---------|
| +12V | 45mA | 60mA |
| -12V | 40mA | 55mA |
| +5V  | 0mA | 0mA |

If current draw is significantly higher:
- Check for shorts
- Verify IC orientation
- Check for damaged components

### Frequency Response

If applicable, measure frequency response:

1. Sweep sine wave from 20Hz to 20kHz
2. Measure output amplitude at each frequency
3. Should be flat ±1dB across audio range

### Noise Floor

With no input signal:

1. Measure output with oscilloscope or AC voltmeter
2. Noise should be < 1mV RMS

## Troubleshooting Calibration Issues

**Offset won't adjust to zero:**
- Check reference voltage at trim pot
- Verify op-amp is not oscillating
- Check for damaged trim pot

**Gain is incorrect:**
- Verify resistor values in gain circuit
- Check for cold solder joints
- Measure op-amp supply voltages

**Unstable measurements:**
- Check power supply quality
- Add more decoupling capacitors
- Check ground connections

## Final Verification

- [ ] All power rails stable
- [ ] Current draw within specifications
- [ ] DC offsets < 100mV
- [ ] All controls functional
- [ ] Signal path clean
- [ ] No oscillation or instability

!!! success "Calibration Complete"
    If all tests pass, the module is ready to use! See [Troubleshooting](troubleshooting.md) if you encounter issues.
