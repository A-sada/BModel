from Vehicle_Task import Task,Vehicle
from negmas import SAOMechanism
from negmas.utilities import UtilityFunction
from negmas.outcomes import Outcome

def Nego1(vehicleA,vehicleB):
    outcomes = [{"AgentA": vehicleA, "AgentB" :vehicleB, "taskA": taskA, "taskB": taskB} for taskA in vehicleA.tasks for taskB in vehicleB.tasks]
    mechanism = SAOMechanism(
        outcomes=outcomes,
        n_steps=10
    )
    mechanism.add(vehicleA)
    mechanism.add(vehicleB)
    result = mechanism.run()
    return result


