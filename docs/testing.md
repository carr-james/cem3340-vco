# Testing

Procedures for testing the completed module.

## Visual Inspection

Before powering on, carefully inspect:

- [ ] All solder joints are shiny and smooth
- [ ] No solder bridges between pads
- [ ] All polarized components oriented correctly
- [ ] No missing components
- [ ] Board is clean (no flux residue if desired)

## Power-On Test

See [Calibration - Power-On Test](calibration.md#power-on-test) for detailed procedure.

## Functional Testing

### Audio Path

1. Apply test signal to input
2. Verify signal at output
3. Check all processing stages
4. Verify controls affect signal

### Control Voltage

1. Apply CV to inputs
2. Verify expected response
3. Test full range of controls

## Performance Testing

### Frequency Response

Test frequency response across audio range (20Hz - 20kHz).

### Signal-to-Noise Ratio

Measure noise floor with no input signal.

### Distortion

Check THD+N at various levels.

## Final Checks

- [ ] All inputs and outputs working
- [ ] Controls responsive
- [ ] No unexpected noise or oscillation
- [ ] Proper integration with eurorack system

See [Calibration](calibration.md) for calibration procedures.
