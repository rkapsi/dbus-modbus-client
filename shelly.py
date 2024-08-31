import logging

import device
import probe
from register import *

class Shelly_Meter(device.CustomName, device.EnergyMeter):
    vendor_id = 'shelly'
    vendor_name = 'Shelly'

    min_timeout = 0.5
    default_access = 'input'

    def device_init(self):
        self.info_regs = [
            Reg_text(0, 6, '/Serial', little=True),
            Reg_text(6, 10, '/ProductName', little=True),
        ]

        self.data_regs = [
            Reg_f32l(1162, '/Ac/Energy/Forward', 1000, '%.1f kWh'),
            Reg_f32l(1164, '/Ac/Energy/Reverse', 1000, '%.1f kWh'),
            Reg_f32l(1013, '/Ac/Power', 1, '%.1f W'),

            Reg_f32l(1020, '/Ac/L1/Voltage', 1, '%.1f V'),
            Reg_f32l(1022, '/Ac/L1/Current', 1, '%.1f A'),

        ]
        
    def get_ident(self):
        return 'shelly_{}'.format(self.info['/Serial'])


class Shelly_Pro_3EM(Shelly_Meter):
    productname = 'Shelly Pro 3EM'
    productid = 0xFFFF
    nr_phases = 3

    def device_init(self):
        super().device_init()

        self.data_regs += [
            Reg_f32l(1182, '/Ac/L1/Energy/Forward', 1000, '%.1f kWh'),
            Reg_f32l(1184, '/Ac/L1/Energy/Reverse', 1000, '%.1f kWh'),
            Reg_f32l(1024, '/Ac/L1/Power', 1, '%.1f W'),

            Reg_f32l(1040, '/Ac/L2/Voltage', 1, '%.1f V'),
            Reg_f32l(1042, '/Ac/L2/Current', 1, '%.1f A'),
            Reg_f32l(1202, '/Ac/L2/Energy/Forward', 1000, '%.1f kWh'),
            Reg_f32l(1204, '/Ac/L2/Energy/Reverse', 1000, '%.1f kWh'),
            Reg_f32l(1044, '/Ac/L2/Power', 1, '%.1f W'),

            Reg_f32l(1060, '/Ac/L3/Voltage', 1, '%.1f V'),
            Reg_f32l(1062, '/Ac/L3/Current', 1, '%.1f A'),
            Reg_f32l(1222, '/Ac/L3/Energy/Forward', 1000, '%.1f kWh'),
            Reg_f32l(1224, '/Ac/L3/Energy/Reverse', 1000, '%.1f kWh'),
            Reg_f32l(1064, '/Ac/L3/Power', 1, '%.1f W'),
        ]

models = {
    Shelly_Pro_3EM.productid: {
        'model':    'SPEM-003CEBEU',
        'handler':  Shelly_Pro_3EM,
    },
}

probe.add_handler(probe.ModelRegister(Reg_u16(0x2000), models,
                                      methods=['tcp'],
                                      units=[1]))
