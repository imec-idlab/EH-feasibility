import wireless
import storage
import plot

# LoRaWAN - see wireless.py for configuration
sodaq_expl_off = wireless.lora_class_a("LoRaWAN Class A - SODAQ Explorer off idle",8,125000,7,51,0.8,1,0,0.134,0.166,2.2,0.456,13,0.00000108)
sodaq_expl_sleep = wireless.lora_class_a("LoRaWAN Class A - SODAQ Explorer sleep idle",8,125000,7,51,0.8,1,0,0.134,0.166,2.2,0,0,0.00929)

# BLE - see wireless.py for configuration
nrf52840_devkit = wireless.ble_lpn("BLE LPN - nRF52840 devkit",0.255,345600,0.255,100000,1,0.0164,0.0156,0.0000161,0.0000062,0.000282,0.000016128)

# 6TiSCH - see wireless.py for configuration
cc1200 = wireless.sixtisch_leaf("6TiSCH leaf node - CC1200",1,1,0.015,96,16,0.000001873,0.0006821,0.001884,0.001076)
cc2538 = wireless.sixtisch_leaf("6TiSCH leaf node - CC2538",1,1,0.015,96,16,0.000000174,0.0003365,0.0009706,0.000180)

# Capacitor - see storage.py for configuration
capacitor = storage.storage_tech(0,2.8,4.5,1.2,0.8,0.000045)

# Interval vs pharv
plot.plot_interval_vs_pharv(10, 250000, sodaq_expl_off, capacitor, 20, 0.05, 0.01)
plot.plot_interval_vs_pharv(10, 250000, sodaq_expl_sleep, capacitor, 20, 0.05, 0.01)
plot.plot_interval_vs_pharv(10, 250000, nrf52840_devkit, capacitor, 20, 0.05, 0.01)
plot.plot_interval_vs_pharv(10, 250000, cc1200, capacitor, 20, 0.05, 0.01)
plot.plot_interval_vs_pharv(10, 250000, cc2538, capacitor, 20, 0.05, 0.01)

# Latency vs payload
plot.plot_latency_vs_pl(0, 200, sodaq_expl_off)
plot.plot_latency_vs_pl(0, 200, sodaq_expl_sleep)
plot.plot_latency_vs_pl(0, 200, nrf52840_devkit)

# Latency vs pharv (6TiSCH)
plot.plot_latency_vs_pharv(10, 250000, cc1200, capacitor, 20, 0.05, 0.01)
plot.plot_latency_vs_pharv(10, 250000, cc2538, capacitor, 20, 0.05, 0.01)