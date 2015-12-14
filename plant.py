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


if __name__ == '__main__':
    pipe1 = Pipe()
    pump1 = Pump()
    pipe2 = Pipe()

    plant = [pipe1, pump1, pipe2]

    flow_to_plant = 5

    for i in range(10):
        inflow = flow_to_plant
        for asset in plant:
            outflow = asset.advance(inflow)
            
            print("{0} {1} ".format(inflow, asset.print()), end="")
            inflow = outflow
        print("{0}\n".format(outflow))
