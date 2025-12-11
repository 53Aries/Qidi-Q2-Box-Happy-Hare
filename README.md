# QIDI Q2 Box with Happy-Hare MMU Configuration

This repository contains the complete Klipper configuration for a QIDI Q2 3D printer with Happy-Hare multi-material unit (MMU).

## Hardware

- **Printer**: QIDI Q2
- **Host**: MKS board running Linaro ALIP Linux
- **Stepper Drivers**: TMC2240 with sensorless homing
- **Z-Probe**: Load cell
- **MMU**: Happy-Hare multi-material unit
- **Brush**: 23mm × 6mm cleaning brush at Y=280

## Features

- **Adaptive Bed Meshing**: Klipper adaptive meshing support (`ADAPTIVE=1`)
- **Sensorless Homing**: TMC2240 current reduction (0.9A) for X/Y homing
- **Temperature Management**: Heater state preservation during Z homing
- **Enhanced Nozzle Cleaning**: Dual-pattern brush cleaning (full-width + circular)
- **Emergency Shutdown**: Macro to disable all heaters and fans
- **MMU Control**: Full Happy-Hare integration with purge/wipe system

## System Optimizations

**Critical Performance Fixes Applied:**
- `lightdm` service **masked** (was causing crash loop)
- `makerbase-client` service **disabled** (was respawning continuously)

These fixes reduced system load from 5.6 to 1.4-2.0, with 80-87% CPU idle. **Do not re-enable these services** without careful monitoring.

## Configuration Structure

```
printer_data/
├── config/              # Main printer configuration
│   ├── printer.cfg      # Primary config file
│   ├── MCU_ID.cfg       # MCU identifiers
│   └── mmu/             # Happy-Hare MMU configuration
│       ├── base/        # Core MMU configs
│       ├── addons/      # Optional MMU features
│       └── optional/    # Additional modules
├── macros/              # Custom G-code macros
│   ├── homing.cfg       # Sensorless homing with temp management
│   ├── disable_heaters_fans.cfg  # Emergency shutdown
│   ├── clean_nozzle.cfg # Brush cleaning
│   └── ...
└── gcodes/              # Uploaded G-code files

klipper/                 # Klipper firmware
└── klippy/              # Python modules (pyudev import guarded)

Happy-Hare/              # MMU firmware components
├── extras/              # MMU Klipper modules
├── config/              # MMU configuration templates
└── components/          # Server-side components
```

## Key Configuration Files

### Homing (`printer_data/macros/homing.cfg`)
- **Lines 82-111**: Temperature save/restore in Z homing
- **Lines 116-146**: `_HOME_X` and `_HOME_Y` macros with TMC2240 current reduction
- **Lines 147-151**: `_HOME_XY` sequence

### Nozzle Cleaning (`printer_data/config/mmu/base/PARK_PURGE_WIPE.cfg`)
- **Line 34**: `variable_brush_y_position: 280` (front edge coordinate)
- **Lines 315-340**: Dual-pattern cleaning (full-width wipes + circular motion)

### Emergency Shutdown (`printer_data/macros/disable_heaters_fans.cfg`)
- `DISABLE_ALL_HEATERS_FANS` macro
- Uses type-specific fan commands for all cooling systems

## Network Access

- **SSH**: `mks@192.168.0.114`
- **Password**: `makerbase`
- **Moonraker API**: Port 7125
- **Web Interface**: Port 80

## Important Notes

1. **Variable Naming**: Use lowercase with underscores (e.g., `brush_y_position`)
2. **Brush Coordinates**: `brush_y_position` is the front edge, not center
3. **Service Management**: Do not re-enable `lightdm` or `makerbase-client` without testing
4. **Adaptive Meshing**: Use `BED_MESH_CALIBRATE ADAPTIVE=1 ADAPTIVE_MARGIN=5`

## Backup Information

This configuration was backed up on 2025-12-10 from a working system with stable performance.

## License

Configuration files licensed under the same terms as their respective source projects (Klipper, Happy-Hare).
