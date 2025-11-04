# Schematics

Technical circuit diagrams for the module.

## Full Schematic

<!-- Auto-generated schematic PDF embedded here -->
[Download Full Schematic PDF](generated/schematics/placeholder_schematic.pdf){ .md-button .md-button--primary }

### Schematic Pages

<!-- If multi-page schematic, individual SVG pages can be shown here -->

![Schematic Page 1](generated/schematics/placeholder_schematic_01.svg)

## Circuit Sections

### Power Supply

Description of power supply circuit:
- Input filtering
- Reverse polarity protection
- Voltage regulation (if any)
- Decoupling

### Main Signal Path

Description of how signals flow through the module.

### Control Voltage Processing

How CV inputs are processed.

## Design Notes

### Component Selection

**Op-Amps:**
The design uses TL072 dual op-amps for:
- Low noise
- Wide bandwidth
- Commonly available
- Inexpensive

**Diodes:**
1N4148 signal diodes for:
- Fast switching
- Low forward voltage drop

**Capacitors:**
- 100nF ceramics for decoupling
- 100µF electrolytics for bulk filtering
- Film caps for audio coupling (if used)

### Signal Levels

| Signal Type | Range | Impedance |
|-------------|-------|-----------|
| Audio Input | ±5V | 100kΩ |
| CV Input | 0-5V | 100kΩ |
| Audio Output | ±10V | 1kΩ |
| CV Output | 0-10V | 1kΩ |

### Modifications

Possible circuit modifications:

**Gain Adjustment:**
- Change R10 to modify gain
- Typical values: 10kΩ - 100kΩ

**Frequency Response:**
- Adjust C5 to change cutoff frequency
- Formula: fc = 1/(2πRC)

## Reference Designs

This design is based on/inspired by:
- [Reference 1]
- [Reference 2]

## Download Formats

- [PDF Format](generated/schematics/placeholder_schematic.pdf) - For printing
- [SVG Format](generated/schematics/placeholder_schematic_01.svg) - For editing
