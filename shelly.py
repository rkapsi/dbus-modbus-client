import logging

import device
import probe
from register import *

log = logging.getLogger(__name__)


class ShellyEnergyMeter(device.CustomName, device.EnergyMeter):
    # Define mandatory properties so the device gets saved
    productid = 0xFFFF
    productname = 'Shelly Energy Meter'

    def __init__(self, spec, modbus, model):
        super().__init__(spec, modbus, model)
        # Increase default timeout
        self.min_timeout = 0.5
        # Shelly Modbus devices oddly use input registers for everything
        self.default_access = 'input'
        self.nr_phases = 3

    def device_init(self):
        log.info('Initializing Shelly energy meter using connection "%s"', self.connection())

        self.info_regs = [
            Reg_text(0, 6, '/Serial', little=True),
            Reg_text(6, 10, '/ProductName', little=True),
        ]

        self.data_regs = [
            Reg_f32l(1162, '/Ac/Energy/Forward', 1000, '%.1f kWh'),
            Reg_f32l(1164, '/Ac/Energy/Reverse', 1000, '%.1f kWh'),
            Reg_f32l(1013, '/Ac/Power', 1, '%.1f W'),
            Reg_f32l(1182, '/Ac/L1/Energy/Forward', 1000, '%.1f kWh'),
            Reg_f32l(1184, '/Ac/L1/Energy/Reverse', 1000, '%.1f kWh'),
            Reg_f32l(1020, '/Ac/L1/Voltage', 1, '%.1f V'),
            Reg_f32l(1022, '/Ac/L1/Current', 1, '%.1f A'),
            Reg_f32l(1024, '/Ac/L1/Power', 1, '%.1f W'),
            Reg_f32l(1202, '/Ac/L2/Energy/Forward', 1000, '%.1f kWh'),
            Reg_f32l(1204, '/Ac/L2/Energy/Reverse', 1000, '%.1f kWh'),
            Reg_f32l(1040, '/Ac/L2/Voltage', 1, '%.1f V'),
            Reg_f32l(1042, '/Ac/L2/Current', 1, '%.1f A'),
            Reg_f32l(1044, '/Ac/L2/Power', 1, '%.1f W'),
            Reg_f32l(1222, '/Ac/L3/Energy/Forward', 1000, '%.1f kWh'),
            Reg_f32l(1224, '/Ac/L3/Energy/Reverse', 1000, '%.1f kWh'),
            Reg_f32l(1060, '/Ac/L3/Voltage', 1, '%.1f V'),
            Reg_f32l(1062, '/Ac/L3/Current', 1, '%.1f A'),
            Reg_f32l(1064, '/Ac/L3/Power', 1, '%.1f W'),
        ]
        
    def get_ident(self):
        return 'shelly_{}'.format(self.info['/Serial'])


class ShellyModelRegister(probe.ModelRegister):
    def __init__(self, **args):
        super().__init__(None, [], **args)

    def probe(self, spec, modbus, timeout=None):
        return ShellyEnergyMeter(spec, modbus, 'SPEM-003CE')


probe.add_handler(ShellyModelRegister(methods=['tcp'], units=[1]))
