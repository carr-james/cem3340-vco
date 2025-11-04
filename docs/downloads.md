# Downloads

All files needed to build, modify, or manufacture the module.

## Manufacturing Files

### PCB Fabrication

[Download Gerber Files (ZIP)](generated/production/placeholder_gerbers_jlcpcb.zip){ .md-button .md-button--primary }

Upload this ZIP file directly to JLCPCB or your preferred PCB manufacturer.

**Included files:**
- Copper layers (F.Cu, B.Cu, and inner layers if applicable)
- Silkscreen (F.SilkS, B.SilkS)
- Soldermask (F.Mask, B.Mask)
- Board outline (Edge.Cuts)
- Drill files (PTH and NPTH)

### Assembly Files

For automated assembly services:

- [BOM for JLCPCB](generated/bom/placeholder_bom_jlc.csv) - Component list in JLCPCB format
- [Position File](generated/position/placeholder_cpl_jlc.csv) - Component placement coordinates
- [BOM (HTML)](generated/bom/placeholder_bom.html) - Human-readable parts list

## Documentation

[Download Complete Documentation (ZIP)](generated/production/placeholder_documentation.zip){ .md-button }

**Includes:**
- Full schematic PDF
- PCB fabrication drawings
- 3D renders (all views)
- Assembly guides
- Bill of materials

### Individual Documents

- [Schematic PDF](generated/schematics/placeholder_schematic.pdf)
- [PCB Fabrication Drawing](generated/pcb/placeholder_pcb_fabrication.pdf)
- [Board Dimensions](generated/pcb/placeholder_dimensions.svg)

## Design Files

### KiCad Project

The full KiCad project files are available in the GitHub repository:

[View on GitHub](https://github.com/your-username/your-repo){ .md-button }

Clone with:
```bash
git clone --recursive https://github.com/your-username/your-repo.git
```

**Note:** Use `--recursive` to also clone the shared component library.

### 3D Models

- [STEP File](generated/mechanical/placeholder.step) - For mechanical CAD integration

## Interactive Tools

### Interactive BOM

[Open Interactive BOM](generated/ibom/placeholder_interactive_bom.html){ .md-button }

Use the interactive BOM during assembly to:
- Locate components on the board
- Check off assembled parts
- View component values and footprints
- Navigate between top and bottom sides

## Design Reports

Quality assurance reports from the build process:

- [Design Rule Check (DRC)](generated/reports/placeholder_drc.txt)
- [Electrical Rule Check (ERC)](generated/reports/placeholder_erc.txt)

## Version History

### Current Version

**v1.0.0** - YYYY-MM-DD
- Initial release
- [Release notes](https://github.com/your-username/your-repo/releases/tag/v1.0.0)

### Previous Versions

See [all releases](https://github.com/your-username/your-repo/releases) on GitHub.

## License

All files are released under [Your License Here].

You are free to:
- Build the module for personal use
- Modify the design
- Share improvements

Please:
- Give credit to the original designer
- Share modifications under the same license
- Don't sell as a commercial product without permission

## File Formats

| Extension | Type | Opens With |
|-----------|------|------------|
| .zip | Archive | Windows/Mac/Linux |
| .pdf | Document | Any PDF reader |
| .svg | Vector Image | Web browser, Inkscape |
| .png | Raster Image | Any image viewer |
| .csv | Spreadsheet | Excel, Google Sheets |
| .html | Web Page | Any web browser |
| .step | 3D Model | FreeCAD, Fusion 360 |
| .kicad_pro | KiCad Project | KiCad 8.0+ |
| .kicad_sch | KiCad Schematic | KiCad 8.0+ |
| .kicad_pcb | KiCad PCB | KiCad 8.0+ |

## Build Support

Need help with your build?

- [Troubleshooting Guide](troubleshooting.md)
- [GitHub Issues](https://github.com/your-username/your-repo/issues)
- [Discussion Forum](https://github.com/your-username/your-repo/discussions)

## Updates

Files are automatically generated from the latest design. Last updated: [AUTO-GENERATED DATE]

To get notified of updates:
- Watch the GitHub repository
- Subscribe to releases
- Follow on [social media]
