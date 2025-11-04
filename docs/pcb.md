# PCB Layout

Technical information about the PCB design.

## Board Specifications

| Parameter | Value |
|-----------|-------|
| Layers | 2 (or 4) |
| Dimensions | See [3D Renders](renders.md) |
| Thickness | 1.6mm |
| Copper Weight | 1oz (35µm) |
| Surface Finish | HASL or ENIG |
| Minimum Track Width | 0.15mm (6 mil) |
| Minimum Clearance | 0.15mm (6 mil) |

## Layer Stack

### 2-Layer Configuration

1. Top Copper (F.Cu) - Signal, power distribution
2. Bottom Copper (B.Cu) - Ground plane, signals

### 4-Layer Configuration (if applicable)

1. Top Copper (F.Cu) - Signal routing
2. Inner Layer 1 (In1.Cu) - Ground plane
3. Inner Layer 2 (In2.Cu) - Power planes (+12V, -12V)
4. Bottom Copper (B.Cu) - Signal routing

## Design Considerations

### Ground Plane

- Solid ground pour on bottom layer
- Minimizes noise and EMI
- Provides low-impedance return path

### Power Distribution

- Wide traces for power (0.5mm minimum)
- Star grounding topology
- Local decoupling at each IC

### Signal Routing

- Audio signals kept short and direct
- Sensitive inputs shielded
- CV traces separated from digital

## Manufacturing Notes

Designed for standard JLCPCB specifications:

- 6/6 mil track/spacing
- 0.3mm minimum drill size
- NPTH and PTH separate files
- No blind or buried vias

## Design Files

[Download KiCad PCB](https://github.com/your-username/your-repo)

[View Gerbers](downloads.md#pcb-fabrication)
