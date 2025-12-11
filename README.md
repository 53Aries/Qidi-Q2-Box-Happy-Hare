# QIDI Q2 Box with Happy-Hare MMU Configuration

This repository contains the complete Klipper configuration for a QIDI Q2 3D printer with Happy-Hare multi-material unit (MMU). 
The display screen will no longer function. Changes to klippy.py and klippy/extras to remove Qidi box systems.

## Hardware

- **Printer**: QIDI Q2
- **Host**: MKS board running Linaro ALIP Linux
- **Z-Probe**: Load cell
- **MMU**: Happy-Hare for Qidi Box

## Features

- **Adaptive Bed Meshing**: Klipper adaptive meshing support (`ADAPTIVE=1`)
- **Enhanced Nozzle Cleaning**: Dual-pattern brush cleaning (full-width + circular)
- **MMU Control**: Full Happy-Hare integration with purge/wipe system

## System Optimizations

**Critical Performance Fixes Applied:**
- `lightdm` service **masked** (was causing crash loop)
- `makerbase-client` service **disabled** (was respawning continuously)
These fixes reduced system load from 5.6 to 1.4-2.0, with 80-87% CPU idle. **Do not re-enable these services** without careful monitoring.


This configuration was backed up on 2025-12-10 from a working system with stable performance.

## License

Configuration files licensed under the same terms as their respective source projects (Klipper, Happy-Hare).
