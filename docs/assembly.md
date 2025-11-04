# Assembly Instructions

This guide will walk you through assembling the module step-by-step.

## Required Tools

- Soldering iron (temperature controlled recommended)
- Solder (60/40 or 63/37 leaded, or lead-free)
- Flush cutters
- Needle-nose pliers
- Multimeter
- Solder wick or desoldering pump (for mistakes)

## Before You Start

!!! warning "Safety First"
    - Work in a well-ventilated area
    - Use safety glasses
    - Be careful with hot soldering iron
    - ESD precautions recommended for sensitive ICs

!!! tip "Assembly Tips"
    - Solder components from shortest to tallest
    - Double-check component orientation before soldering
    - Use the interactive BOM to locate components
    - Test the power supply circuit before adding sensitive ICs

## Assembly Order

### Step 1: Power Supply Components

Start with the power supply section to ensure clean power before adding other components.

![Power section assembly](generated/assembly/placeholder_assembly_top.svg){ width="600" }

**Components to install:**

- [ ] **D1, D2** - Power protection diodes (1N5819)
  - **Polarity:** Black band toward the power rails (see silkscreen)
- [ ] **C1, C2** - Bulk filtering caps (100µF electrolytic)
  - **Polarity:** Longer lead is positive (+), match with silkscreen
- [ ] **C3, C4** - Ceramic decoupling caps (100nF)
  - **No polarity**
- [ ] **J1** - Power connector (2x5 shrouded header)
  - **Orientation:** Notch matches silkscreen, pin 1 marked

!!! danger "Critical Check"
    **Before proceeding:** Use multimeter to verify:

    - +12V rail has no shorts to GND
    - -12V rail has no shorts to GND
    - +12V and -12V rails do not short to each other

### Step 2: Resistors

Install all resistors. **Resistors have no polarity.**

- [ ] All resistors per BOM
  - Check color codes or measure with multimeter
  - Bend leads, insert, solder, trim

### Step 3: Ceramic Capacitors

Install all small ceramic capacitors. **No polarity.**

- [ ] All ceramic caps (marked 104, 103, etc.)

### Step 4: Transistors and Diodes

- [ ] Signal diodes (1N4148)
  - **Polarity:** Black band matches silkscreen
- [ ] Transistors (2N3904, 2N3906, etc.)
  - **Orientation:** Flat side matches silkscreen

### Step 5: IC Sockets (Recommended)

!!! tip "Use IC Sockets"
    Using sockets allows you to replace ICs if they fail and protects them from soldering heat.

- [ ] All IC sockets
  - **Orientation:** Notch matches silkscreen
  - Solder one corner pin first, check alignment, then solder rest

### Step 6: Electrolytic Capacitors

- [ ] All polarized electrolytic caps
  - **Polarity:** Longer lead is positive, white stripe is negative
  - Match with + symbol on silkscreen

### Step 7: Connectors

- [ ] Audio jacks (PJ301M or similar)
- [ ] Potentiometers (mount to panel first if applicable)
- [ ] Switches
- [ ] Other connectors per BOM

!!! tip "Test Fit with Panel"
    Before soldering panel-mounted components, test fit with front panel to ensure proper alignment.

### Step 8: Insert ICs

**Only after complete assembly and power testing!**

- [ ] Insert ICs into sockets
  - **Orientation:** Notch or dot marks pin 1
  - Gently bend pins if needed to fit socket
  - Press firmly but gently

## Visual Guide

### Top View

![Assembly top view](generated/assembly/placeholder_assembly_top.svg)
*Component placement on top side*

### Bottom View

![Assembly bottom view](generated/assembly/placeholder_assembly_bottom.svg)
*Component placement on bottom side (if applicable)*

## Board Stack Assembly

If this is a multi-board design:

1. Assemble each board individually
2. Test each board separately if possible
3. Install inter-board connectors
4. Stack boards and secure with standoffs
5. Install panel-mounted components
6. Connect boards together

## Quality Checks

After assembly, inspect your work:

- [ ] All solder joints are shiny and smooth (not cold/dull)
- [ ] No solder bridges between adjacent pins/pads
- [ ] All components are flat against board
- [ ] Correct component orientation (polarized parts)
- [ ] No missing components

## Next Steps

After assembly is complete:

1. [Visual inspection](testing.md#visual-inspection)
2. [Power-on testing](testing.md#power-on-test)
3. [Calibration](calibration.md)
4. [Final testing](testing.md#functional-test)

!!! success "Congratulations!"
    If you've completed assembly, proceed to the [Testing](testing.md) page.
