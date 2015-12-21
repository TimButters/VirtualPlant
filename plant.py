#!/usr/bin/python

import VirtualPlant.VirtualPlant as vp

if __name__ == '__main__':
    flow_to_plant = 5
    temp_in = 20

    plant = vp.Plant(flow_to_plant, temp_in)

    plant.add_asset(vp.Pipe())
    plant.add_asset(vp.Pump())
    plant.add_asset(vp.Pipe())
    plant.add_asset(vp.Furnace())

    for i in range(10):
        plant.advance_plant()
