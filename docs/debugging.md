# Debugging Guide

Advanced debugging techniques for when standard troubleshooting doesn't work.

## Equipment Needed

- Multimeter (basic)
- Oscilloscope (recommended)
- Function generator (helpful)
- Logic analyzer (for digital circuits)

## Systematic Debugging

### 1. Define the Problem

Document exactly what's wrong:
- What works?
- What doesn't work?
- When did it start?
- What changed?

### 2. Isolate the Issue

- Power supply problems?
- Specific circuit section?
- All channels or just one?

### 3. Signal Tracing

Use oscilloscope to follow signal path:

```
Input → Stage 1 → Stage 2 → Output
 OK?      OK?       OK?      Bad?
```

Find where signal disappears or distorts.

### 4. Component-Level Testing

Test individual components:

**Resistors:** Measure resistance (should match value ±5%)
**Capacitors:** Check for shorts, test capacitance
**Diodes:** Forward voltage ~0.6-0.7V
**Transistors:** Check all three terminals
**Op-amps:** Verify power, check input/output

## Common Debug Points

### Power Rails

Test at multiple locations:
- Power connector
- Decoupling caps
- IC power pins
- Far end of board

### Signal Path

Inject known signal, probe at:
- Input jack
- Input buffer output
- Processing stage outputs
- Output buffer
- Output jack

### Ground Integrity

- Verify continuity across ground plane
- Check for floating ground sections
- Measure ground noise

## Advanced Techniques

### Scope Triggering

Set up proper triggering to catch intermittent problems.

### Frequency Sweep

Sweep input frequency to find resonances or instabilities.

### Temperature Testing

- Cold spray to cool components
- Heat gun to warm components
- Find temperature-sensitive failures

### Component Substitution

Replace suspected components one at a time.

## Using Test Equipment

### Multimeter

- Continuity testing
- Voltage measurements
- Resistance checks

### Oscilloscope

- Waveform analysis
- Frequency measurement
- Phase relationships
- Noise analysis

### Function Generator

- Signal injection
- Frequency response testing
- Gain measurements

## Documentation

Keep notes of:
- Measurements taken
- Changes made
- Results observed

## When to Ask for Help

If stuck after trying:
- Visual inspection
- Continuity testing
- Component testing
- Signal tracing

Then post to forums with:
- Clear problem description
- Photos (top, bottom, close-ups)
- Measurements taken
- Schematic reference

See [Troubleshooting](troubleshooting.md) for common issues.
