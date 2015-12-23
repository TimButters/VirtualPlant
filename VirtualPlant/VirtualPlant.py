import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import numpy as np


class Pipe:
    """A simple pipe model"""
    display_width = 200.0
    display_height = 40.0

    inflow = 0
    outflow = 0
    integrity = 1

    def print(self):
        return "========"

    def display_asset(self, cr, x, y):
        return cr.rectangle(x, y, self.display_width, self.display_height)

    def advance(self, inflow, intemp):
        return inflow*self.integrity, intemp


class Pump:
    """A simple pump model"""
    display_width = 40

    def __init__(self, power=10):
        self.power = power

    def print(self):
        return "|__|"

    def display_asset(self, cr, x, y):
        return cr.arc(x, y, self.display_width, 0, 2*np.pi)

    def advance(self, inflow, intemp):
        return self.power*inflow, intemp


class Furnace:
    """A simple furnace model"""
    display_width = 150
    display_height = 300

    # stef_boltz_const = 5.67037E-8
    # emissivity = 0.9  # Between 0 and 1
    length = 20  # metres
    density_h20 = 0.804  # kg/m3
    furnace_flow = 30  # m3/h
    heat_capacity_h20 = 4181.3  # J/kg/K - Of the exchanger substance (water)
    heat_capacity_pro = 2191.0  # J/kg/K - Of process substance (Methane)
    density_pro = 0.668  # kg/m3 Methane

    def __init__(self, temperature=500):
        self.temperature = temperature

    def print(self):
        return "-{F}-"

    def display_asset(self, cr, x, y):
        return cr.rectangle(x, y, self.display_width, self.display_height)

    def advance(self, flow_in, temp_in):
        temp_in = temp_in + 273.15  # Convert from degC to K
        furnace_temp = self.temperature + 273.15

        # Mass per unit time converting m3/h to m3/sec
        mass_per_unit_time_h20 = (self.furnace_flow/3600.0) * self.density_h20
        mass_per_unit_time_pro = (flow_in/3600.0) * self.density_pro

# "Thermal Connection Constant" Don't know what this should be?? Units are 1/m
        gamma = 1
        k1 = gamma/(self.heat_capacity_h20*mass_per_unit_time_h20)
        k2 = gamma/(self.heat_capacity_pro*mass_per_unit_time_pro)
        k = k1 + k2

        temp_out = ((temp_in*k1 + furnace_temp*k2)/k +
                    (((temp_in - furnace_temp)*k2)/k) * np.exp(-k*self.length))

        # Convert K to degC
        return flow_in, (temp_out - 273.15)


class Plant(Gtk.Window):
    """
    A Plant is a collection of assets that are automaticaly
    linked together
    """
    def __init__(self, inflow, intemp, visualise=True):
        self.inflow = inflow
        self.intemp = intemp
        self.assets = []

        if visualise:
            Gtk.Window.__init__(self, title="Virtual Plant")

            self.set_border_width(10)

            grid = Gtk.Grid()
            self.add(grid)

            # Advance Button
            self.button_advance = Gtk.Button.new_with_label("Advance")
            self.button_advance.connect("clicked", self.advance_plant)

            # Fault Button
            self.button_fault = Gtk.Button.new_with_label("Introduce Fault")
            self.button_fault.connect("clicked", self.advance_plant)

            # Drawing Area
            self.da = Gtk.DrawingArea()
            self.da.set_size_request(1000, 600)
            self.da.connect("draw", self.expose)

            # Arrange items in a grid
            grid.add(self.da)
            grid.attach_next_to(self.button_fault, self.da,
                                Gtk.PositionType.BOTTOM, 1, 1)
            grid.attach_next_to(self.button_advance, self.button_fault,
                                Gtk.PositionType.BOTTOM, 1, 1)

    def expose(self, widget, event):
        cr = widget.get_property("window").cairo_create()
        cr.set_source_rgb(0.6, 0.6, 0.6)

        x_padding = 50
        x = x_padding
        for i, each in enumerate(self.assets):
            each.display_asset(cr, x, 50)
            x += each.display_width + x_padding
        cr.fill()

    def add_asset(self, asset):
        self.assets.append(asset)

    def advance_plant(self, terminal_display=True):
        inflow = self.inflow
        intemp = self.intemp

        variables = []

        for asset in self.assets:
            outflow, outtemp = asset.advance(inflow, intemp)
            variables.append([outflow, outtemp])

            if terminal_display:
                print("{0:.2f}/{1:.2f} {2} ".format(inflow, intemp,
                                                    asset.print()), end="")
            inflow = outflow
            intemp = outtemp

        if terminal_display:
            print("{0:.2f}/{1:.2f}\n".format(outflow, outtemp))

        return variables
