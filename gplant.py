#!/usr/bin/python

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import VirtualPlant.VirtualPlant as vp


if __name__ == '__main__':
    flow_to_plant = 5
    temp_in = 20

    plant = vp.Plant(flow_to_plant, temp_in, True)

    plant.add_asset(vp.Pipe())
    plant.add_asset(vp.Pump())
    plant.add_asset(vp.Pipe())
    plant.add_asset(vp.Furnace())

    # win = MyWindow()
    plant.connect("delete-event", Gtk.main_quit)
    plant.show_all()
    Gtk.main()

    # for i in range(10):
    #     plant.assets[2].integrity = 1-(i/100)
    #     plant.advance_plant()
