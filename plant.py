#!/usr/bin/python

import numpy as np


class Pipe:
    """A simple pipe model"""
    inflow = 0
    outflow = 0
    integrity = 1

    def print(self):
        return "========"

    def advance(self, inflow):
        return inflow*self.integrity


class Pump:
    """A simple pump model"""
    def __init__(self, power=10):
        self.power = power

    def print(self):
        return "|__|"

    def advance(self, inflow):
        return self.power*inflow


class Furnace:
    """A simple furnace model"""
    # stef_boltz_const = 5.67037E-8
    # emissivity = 0.9 # Between 0 and 1
    length = 20 # metres
    density_h20 = 0.804 # kg/m3
    furnace_flow = 30 # m3/h
    heat_capacity_h20 = 4181.3 # J/kg/K - Of the exchanger substance (water)
    heat_capacity_pro = 2191.0 # J/kg/K - Of process substance (Methane)
    density_pro = 0.668 # kg/m3 Methane
    def __init__(self, temperature=500):
        self.temperature = temperature
        
    def print(self):
        return "-{F}-"

    def advance(self, temp_in, flow_in):
        temp_in = temp_in + 273.15 # Convert from degC to K
        furnace_temp = self.temperature + 273.15
        
        # Mass per unit time converting m3/h to m3/sec
        mass_per_unit_time_h20 = (furnace_flow/3600.0) * density_h20
        mass_per_unit_time_pro = (flow_in/3600.0) * density_pro

        gamma = 1 # Don't know what this should be?? Units are 1/m
        k1 = gamma/(heat_capacity_h20*mass_per_unit_flow_h20)
        k2 = gamma/(heat_capacity_pro*mass_per_unit_flow_pro)
        k = k1 + k2

        temp_out = ((temp_in*k1 + furnace_temp*k2)/k +
                   (((temp_in - furnace_temp)*k2)/k) * np.exp(-k*self.length))
 
        # Convert K to degC
        return temp_out - 273.15


class Plant:
    """
    A Plant is a collection of assets that are automaticaly
    linked together
    """
    def __init__(self):
        self.assets = []

    def add_asset(self, asset):
        self.assets.append(asset)

    def advance_plant(self, flow_to_plant, display=True):
        inflow = flow_to_plant
        for asset in self.assets:
            outflow = asset.advance(inflow)

            if display:
                print("{0} {1} ".format(inflow, asset.print()), end="")
            inflow = outflow

        if display:
            print("{0}\n".format(outflow))



if __name__ == '__main__':
    plant = Plant()

    plant.add_asset(Pipe())
    plant.add_asset(Pump())
    plant.add_asset(Pipe())

    flow_to_plant = 5

    for i in range(10):
        plant.advance_plant(flow_to_plant)
