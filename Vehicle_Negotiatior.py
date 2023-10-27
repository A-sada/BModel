from negmas import AspirationNegotiator, ResponseType,SAONegotiator
from negmas.negotiators import Controller
from negmas.preferences.base_ufun import BaseUtilityFunction
from negmas.preferences.preferences import Preferences
from negmas.situated import Agent
from Vehicle import Vehicle_Base
class negotiator(SAONegotiator):
    def __init__(self, owner : Vehicle_Base  ,rout : list):
        self.owner = owner
        self.rout = 