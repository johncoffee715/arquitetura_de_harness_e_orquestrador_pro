# Vega 20 — Referências Técnicas

## Hardware
- **GPU**: AMD Radeon VII (Vega 20)
- **Processo**: 7nm TSMC
- **Memória**: HBM2 16GB
- **TDP**: 310W (VBIOS limit)
- **Device Path**: `/sys/class/drm/card1/device`

## DPM Levels

### SCLK (GPU Clock)
| Level | Frequency |
|-------|-----------|
| 0 | 859 MHz |
| 1 | 860 MHz |
| 2 | 1153 MHz |
| 3 | 1316 MHz |
| 4 | 1425 MHz |
| 5 | 1514 MHz |
| 6 | 1583 MHz |
| 7 | 1654 MHz |
| 8 | 2010 MHz |

### MCLK (Memory Clock - HBM2)
| Level | Frequency |
|-------|-----------|
| 0 | 350 MHz |
| 1 | 800 MHz |
| 2 | 1300 MHz |

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

## Sysfs Interface

### Paths
```
/sys/class/drm/card1/device/pp_dpm_sclk
/sys/class/drm/card1/device/pp_dpm_mclk
/sys/class/drm/card1/device/pp_dpm_fclk
/sys/class/drm/card1/device/pp_dpm_socclk
/sys/class/drm/card1/device/power_dpm_force_performance_level
/sys/class/drm/card1/device/gpu_busy_percent
/sys/class/drm/card1/device/hwmon/hwmon0/temp1_input
/sys/class/drm/card1/device/hwmon/hwmon0/temp2_input
/sys/class/drm/card1/device/hwmon/hwmon0/power1_cap
/sys/class/drm/card1/device/hwmon/hwmon0/power1_cap_max
```

## Comandos Úteis

### Force Overclock
```bash
echo "manual" | sudo tee /sys/class/drm/card1/device/power_dpm_force_performance_level
echo "8" | sudo tee /sys/class/drm/card1/device/pp_dpm_sclk
echo "2" | sudo tee /sys/class/drm/card1/device/pp_dpm_mclk
echo "7" | sudo tee /sys/class/drm/card1/device/pp_dpm_fclk
echo "7" | sudo tee /sys/class/drm/card1/device/pp_dpm_socclk
```

### Verificar Status
```bash
cat /sys/class/drm/card1/device/pp_dpm_sclk
cat /sys/class/drm/card1/device/pp_dpm_mclk
cat /sys/class/drm/card1/device/pp_dpm_fclk
cat /sys/class/drm/card1/device/pp_dpm_socclk
cat /sys/class/drm/card1/device/gpu_busy_percent
```

### Temperaturas
```bash
cat /sys/class/drm/card1/device/hwmon/hwmon0/temp1_input  # Edge
cat /sys/class/drm/card1/device/hwmon/hwmon0/temp2_input  # Hotspot
```

## Limitações
1. **TDP**: 310W máximo (VBIOS)
2. **SOCCLK**: 971 MHz máximo (82.2% de FCLK)
3. **MCLK**: 1300 MHz máximo (DPM level 2)
4. **Hotspot**: Sensor com falsos positivos

## Tags
#vega20 #hardware #dpm-levels #sysfs #referencia
