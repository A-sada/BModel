from Task import Task,Offer,Nego
# 車両（エージェント）クラス
from negmas import AspirationNegotiator, ResponseType,SAONegotiator

from negmas import SAOMechanism, AspirationNegotiator, Issue, ResponseType
from typing import Optional, List
from VRPTW_functions import euclidean_distance
import copy
import math
from Vehicle_Base import Vehicle_Base

class Vehicle (Vehicle_Base):
    def propose(self, state) :
        
        return super().propose(state)