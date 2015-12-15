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
    def __init__(self, temperature=500):
        self.temperature = temperature


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
