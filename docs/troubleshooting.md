# Troubleshooting

Common issues and how to fix them.

## No Power / LED Doesn't Light

**Symptoms:**
- Power LED doesn't light
- No voltage on rails
- Module appears dead

**Possible Causes:**

1. **Power cable reversed**
   - Check red stripe orientation (-12V side)
   - Verify pin 1 marking on connector

2. **Power cable not fully seated**
   - Press connector firmly into header
   - Check for bent pins

3. **Faulty power supply**
   - Test eurorack power with multimeter
   - Verify ±12V present on bus board

4. **Solder bridge on power connector**
   - Inspect J1 solder joints for bridges
   - Use continuity tester between pins

5. **Wrong LED polarity**
   - LED is polarized - longer lead is positive
   - Check orientation against silkscreen

**How to Fix:**
- Recheck power cable orientation
- Inspect and reflow solder joints on power connector
- Test power rails with multimeter
- Flip LED if installed backwards

## High Current Draw / Power Supply Shuts Down

**Symptoms:**
- Excessive current consumption
- Power supply goes into protection mode
- Module gets hot

**Possible Causes:**

1. **Solder bridge creating short circuit**
   - Most common issue
   - Check between power rails

2. **IC installed backwards**
   - Check notch orientation
   - Verify pin 1 location

3. **Wrong component value**
   - Resistor value too low
   - Shorted capacitor

4. **Damaged IC**
   - IC may have failed during soldering

**How to Fix:**
1. Disconnect module immediately
2. Visual inspection for bridges
3. Measure resistance between rails (should be >1kΩ)
4. Remove ICs and test again
5. Use magnifier to inspect for tiny bridges
6. Reflow suspicious solder joints

## No Output Signal

**Symptoms:**
- Module powers on
- Controls move but no output
- DC voltages present but no signal

**Possible Causes:**

1. **No input signal**
   - Verify input is actually connected
   - Test input cable

2. **Bad solder joint in signal path**
   - Cold solder joint on IC pin
   - Broken trace

3. **Wrong IC type**
   - Verify correct IC part number
   - Check datasheet

4. **IC in socket backwards**
   - Check notch orientation

5. **Missing component in signal path**
   - Review BOM against installed parts

**How to Fix:**
- Use oscilloscope to trace signal path
- Start at input, follow to output
- Find where signal disappears
- Reflow solder joints in that section
- Replace suspected components

## Distorted or Noisy Output

**Symptoms:**
- Signal present but distorted
- Excessive noise or hum
- Crackling sounds

**Possible Causes:**

1. **Bad op-amp**
   - Damaged during installation
   - Wrong part number

2. **Missing decoupling capacitors**
   - Insufficient power filtering
   - IC oscillating

3. **Input signal too hot**
   - Signal exceeds input range
   - Clipping at rails

4. **Poor grounding**
   - Ground loop
   - Insufficient ground connections

5. **Cold solder joint**
   - Intermittent connection
   - High resistance joint

**How to Fix:**
- Check input signal level (should be < ±5V typically)
- Verify all decoupling caps installed
- Replace op-amp with known good part
- Reflow all solder joints in audio path
- Check ground continuity

## Controls Don't Work

**Symptoms:**
- Potentiometer has no effect
- Switch doesn't change behavior
- Full range not achieved

**Possible Causes:**

1. **Pot not soldered properly**
   - Pins not making contact
   - Cold joint

2. **Wrong potentiometer value**
   - 10kΩ vs 100kΩ makes big difference
   - Linear vs logarithmic taper

3. **Wiring error**
   - Pot connected to wrong pins
   - Missing connection

4. **Faulty potentiometer**
   - Damaged during installation
   - Worn out (if used)

**How to Fix:**
- Test pot with multimeter (ohms mode)
- Rotate and watch resistance change
- Reflow solder joints on pot pins
- Verify correct pot value per BOM
- Replace if faulty

## Calibration Won't Hold

**Symptoms:**
- Offset drifts after calibration
- Tracking wanders
- Unstable tuning (oscillators)

**Possible Causes:**

1. **Thermal drift**
   - Components warming up
   - Need warm-up time

2. **Poor quality trim pots**
   - Cheap multi-turn pots drift
   - Replace with better quality

3. **Noisy power supply**
   - Switching noise affecting reference
   - Add filtering

4. **Component tolerance**
   - Resistors have wide tolerance
   - Use precision resistors for critical circuits

**How to Fix:**
- Let module warm up 15 minutes before calibrating
- Use 1% metal film resistors in critical paths
- Add extra power filtering
- Upgrade to precision trim pots

## Oscillation / Instability

**Symptoms:**
- High frequency oscillation on output
- Squealing sound
- Scope shows HF noise

**Possible Causes:**

1. **Missing decoupling capacitors**
   - IC power pins not bypassed
   - Insufficient local filtering

2. **Feedback capacitor missing**
   - Op-amp stage unstable
   - Check C_FB in schematic

3. **Long wires acting as antenna**
   - Panel wiring picking up noise
   - Poor shielding

4. **Op-amp oscillating**
   - Incorrect feedback network
   - Missing compensation capacitor

**How to Fix:**
- Add 100nF ceramic caps to all IC power pins
- Keep power and ground traces short
- Add feedback compensation capacitor (try 10-100pF)
- Use shielded cable for inputs
- Check layout for long traces

## Multi-Board Issues

For multi-board designs:

**Misalignment:**
- Check standoff heights
- Verify connector orientation
- Ensure boards are parallel

**Inter-board Connection Problems:**
- Verify pin headers fully inserted
- Check for bent pins
- Test continuity between boards

**Mechanical Stress:**
- Don't overtighten screws
- Use proper standoff spacing
- Support boards at all mounting points

## Diagnostic Procedures

### Systematic Signal Tracing

1. Inject known signal at input
2. Probe with oscilloscope at each stage:
   - Input jack
   - First op-amp output
   - Second op-amp output
   - Final output
3. Find where signal disappears or distorts
4. Focus troubleshooting on that section

### Power Rail Verification

1. Check voltage at each IC:
   - Pin 8 (or V+): should be +12V
   - Pin 4 (or V-): should be -12V
2. If voltage is wrong at specific IC:
   - Check trace continuity
   - Look for solder bridges
   - Verify decoupling caps

### Component Testing

Remove and test suspicious components:
- **Resistors**: Measure with multimeter
- **Capacitors**: Test with capacitance meter
- **Diodes**: Check forward voltage drop (~0.6V)
- **ICs**: Replace with known good part

## Getting Help

If you're still stuck:

1. **Check the design files**
   - Review schematic carefully
   - Compare with working reference designs

2. **Take clear photos**
   - Top and bottom of board
   - Close-ups of suspicious areas
   - Well-lit, in focus

3. **Document the problem**
   - Exact symptoms
   - What you've tried
   - Measurements taken

4. **Ask for help**
   - [GitHub Issues](https://github.com/your-repo/issues)
   - Eurorack DIY forums
   - ModWiggler forum
   - /r/synthdiy on Reddit

## Prevention Tips

**To avoid issues:**
- Use a good quality temperature-controlled soldering iron
- Take your time - rushing leads to mistakes
- Double-check component orientation before soldering
- Test resistance between power rails before applying power
- Install ICs last (after testing power)
- Use IC sockets for expensive or hard-to-find chips
- Keep workspace clean and organized
- Good lighting is essential

!!! tip "When in Doubt..."
    If something doesn't seem right, stop and investigate. It's easier to fix issues during assembly than after everything is soldered!
