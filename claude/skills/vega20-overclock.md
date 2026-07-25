# AMD Vega 20 GPU Overclock Knowledge Base

## GPU Specifications
- **Model**: AMD Radeon VII (Vega 20)
- **Process**: 7nm TSMC
- **Device Path**: `/sys/class/drm/card1/device`

## Clocks Achieved (Maximum)
- **SCLK**: 2140 MHz
- **MCLK**: 1340 MHz
- **FCLK**: 1180 MHz
- **SOCCLK**: 971 MHz (82.3% of FCLK)

## DPM Levels (Dynamic Power Management)

### SCLK (GPU Clock)
| Level | Frequency |
|-------|-----------|
| 0 | 852 MHz |
| 1 | 991 MHz |
| 2 | 1130 MHz |
| 3 | 1269 MHz |
| 4 | 1408 MHz |
| 5 | 1547 MHz |
| 6 | 1686 MHz |
| 7 | 1801 MHz |
| 8 | 2000 MHz |

### MCLK (Memory Clock - HBM2)
| Level | Frequency |
|-------|-----------|
| 0 | 400 MHz |
| 1 | 800 MHz |
| 2 | 1000 MHz |

### FCLK (Infinity Fabric Clock)
| Level | Frequency |
|-------|-----------|
| 0 | 550 MHz |
| 1 | 610 MHz |
| 2 | 690 MHz |
| 3 | 760 MHz |
| 4 | 870 MHz |
| 5 | 960 MHz |
| 6 | 1080 MHz |
| 7 | 1180 MHz |

### SOCCLK (SoC Clock)
| Level | Frequency |
|-------|-----------|
| 0 | 309 MHz |
| 1 | 523 MHz |
| 2 | 566 MHz |
| 3 | 618 MHz |
| 4 | 680 MHz |
| 5 | 755 MHz |
| 6 | 850 MHz |
| 7 | 971 MHz |

## Important Limitations

### SOCCLK vs FCLK Relationship
- **SOCCLK max**: 971 MHz (82.3% of FCLK)
- **FCLK max**: 1180 MHz
- **Theoretical 97.1%**: 1146 MHz (NOT achievable - firmware limitation)
- **Root cause**: VBIOS/SMU firmware hardcoded DPM table
- **Solution**: Would require VBIOS modification (brick risk)

### Temperature Limits
- **Hotspot sensor**: Unreliable - intermittent false positives
- **Hotspot limit**: 150°C (due to sensor unreliability)
- **Priority**: Edge temp and VRAM temp are more reliable

## Sysfs Interface

### Paths
```
/sys/class/drm/card1/device/pp_dpm_sclk        # SCLK DPM levels
/sys/class/drm/card1/device/pp_dpm_mclk        # MCLK DPM levels
/sys/class/drm/card1/device/pp_dpm_fclk        # FCLK DPM levels
/sys/class/drm/card1/device/pp_dpm_socclk      # SOCCLK DPM levels
/sys/class/drm/card1/device/power_dpm_force_performance_level  # Performance mode
/sys/class/drm/card1/device/gpu_busy_percent    # GPU load (0-100%)
```

### HWMON Temperature
```
/sys/class/drm/card1/device/hwmon/hwmon*/temp1_input  # Edge temp (millidegrees)
/sys/class/drm/card1/device/hwmon/hwmon*/temp2_input  # Hotspot temp (millidegrees)
```

## Commands

### Force Maximum Clocks (Persistent until reboot)
```bash
echo "manual" | sudo tee /sys/class/drm/card1/device/power_dpm_force_performance_level
echo "8" | sudo tee /sys/class/drm/card1/device/pp_dpm_sclk
echo "2" | sudo tee /sys/class/drm/card1/device/pp_dpm_mclk
echo "7" | sudo tee /sys/class/drm/card1/device/pp_dpm_fclk
echo "7" | sudo tee /sys/class/drm/card1/device/pp_dpm_socclk
sleep 2
echo "auto" | sudo tee /sys/class/drm/card1/device/power_dpm_force_performance_level
```

### Dynamic Scaler (Systemd Service)
- **Script**: `/usr/local/bin/vega20-scaler.sh`
- **Service**: `/etc/systemd/system/vega20-scaler.service`
- **Control**: `~/vega20-ctrl.sh {start|stop|restart|status|logs|install}`

## Profiles

| Profile | Load | SCLK | MCLK | FCLK | SOCCLK |
|---------|------|------|------|------|--------|
| idle | 0-4% | auto | auto | auto | auto |
| low | 5-30% | 1547 | 800 | 690 | 618 |
| medium | 31-60% | 1686 | 1000 | 960 | 755 |
| high | 61-85% | 1801 | 1180 | 1080 | 850 |
| max | 86-100% | 2000 | 1180 | 1180 | 971 |

## Thermal Protection
- **Threshold**: Hotspot > 100°C
- **Action**: Auto-reduce to low profile
- **Cooldown**: 5 seconds before re-evaluation

## Key Findings
1. SOCCLK is **firmware-limited** to 971 MHz (not silicon-limited)
2. FCLK and SOCCLK are **independent clock domains** on Vega 20
3. HBM2 memory has **3 DPM levels** (400/800/1000 MHz) + OC to 1340 MHz
4. Dynamic scaling requires **debounce** to prevent oscillation
5. **Manual mode** locks clocks; **auto** lets governor manage
6. **SCLK can reach 2140 MHz** but unstable - testing in progress
7. **MCLK can reach 1340 MHz** but unstable - testing in progress
8. **Hotspot sensor unreliable** - false positives, prioritize edge/VRAM temps

## Ideal Clock Ratios (Healthy Overclock)
```
SCLK ≈ 1.5× a 1.6× o MCLK
FCLK ≈ 1.0× o MCLK (sempre igual ou muito próximo)
SOCCLK ≈ 1.0× a 1.1× o MCLK (limitado a 971 MHz no firmware)
```

### Golden Rules
1. **FCLK = MCLK** (ou máximo 50MHz diferença)
2. **Nunca SOCCLK < MCLK** — controlador de memória precisa de clock suficiente
3. **SCLK é independente** — respeitar limites térmicos (< 85°C hotspot)
4. **Voltagem é inimigo da longevidade** — preferir under-volt + overclock moderado
5. **Testar com workloads reais** — benchmarks sintéticos podem mascarar instabilidade
