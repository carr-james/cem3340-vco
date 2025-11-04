# Bill of Materials

This page lists all components needed to build the module.

## PCB

| Item | Quantity | Notes |
|------|----------|-------|
| PCB | 1 | Order from [JLCPCB](https://jlcpcb.com) or similar |

## Components

!!! tip "Generated BOM"
    The interactive BOM below is automatically generated from the KiCad project.
    You can use it to identify component locations during assembly.

### Interactive BOM

<!-- Auto-generated iBOM will be embedded here -->
<iframe src="../generated/ibom/placeholder_interactive_bom.html" width="100%" height="800px" frameborder="0"></iframe>

[Download iBOM HTML](../generated/ibom/placeholder_interactive_bom.html){ .md-button }

### BOM Table

<!-- Auto-generated HTML BOM table will be inserted here -->

Alternatively, download the BOM as:

- [CSV Format](../generated/bom/placeholder_bom_jlc.csv) - For JLCPCB assembly
- [HTML Format](../generated/bom/placeholder_bom.html) - Human-readable version

## Cost Estimate

| Board | Quantity | Unit Cost | Total |
|-------|----------|-----------|-------|
| PCB (min 5) | 5 | $2 | $10 |
| Components | 1 set | ~$15 | $15 |
| Panel (optional) | 1 | ~$5 | $5 |
| **Total per module** | | | **~$30** |

*Costs are approximate and vary by supplier and order quantity.*

## Sourcing Notes

### Recommended Suppliers

**USA:**
- [Mouser](https://www.mouser.com) - General components
- [Digikey](https://www.digikey.com) - General components
- [Thonk](https://www.thonk.co.uk) - Eurorack-specific parts

**International:**
- [LCSC](https://www.lcsc.com) - Cheap components, integrates with JLCPCB
- [Tayda Electronics](https://www.taydaelectronics.com) - Budget components
- [AliExpress](https://www.aliexpress.com) - Lowest cost (long shipping)

### Critical Components

!!! warning "Hard to Find Parts"
    The following components may require special attention:

    - **Part XYZ**: Only available from specific suppliers
    - **Part ABC**: Long lead time, order early

### Substitutions

Some components can be substituted:

| Original Part | Substitute | Notes |
|---------------|------------|-------|
| TL072 | TL082, NE5532 | Pin-compatible op-amps |
| 1N4148 | 1N914 | General purpose diodes |

## PCB Manufacturing

### Recommended Settings for JLCPCB

| Parameter | Value |
|-----------|-------|
| Layers | 2 |
| Dimensions | [auto-calculated] |
| PCB Thickness | 1.6mm |
| PCB Color | Green (or your preference) |
| Surface Finish | HASL or ENIG |
| Copper Weight | 1oz |
| Material | FR-4 |
| Min Track/Spacing | 6/6 mil |

Upload the gerber ZIP file from [Downloads](downloads.md) page.

## Assembly Service

If using JLCPCB assembly service:

1. Upload gerber files
2. Upload BOM CSV file (JLCPCB format)
3. Upload CPL (component placement) file
4. Review and confirm part selections
5. Order!

!!! tip "Cost Savings"
    JLCPCB offers free assembly for basic components. Only "extended" components incur extra fees.
