from Scenarios.scenario_types.Scenario_Types import *
from Scenarios.scenario_types.AnomalyLengthScenario import AnomalyLengthScenario
from Scenarios.scenario_types.BaseScenario import BaseScenario
from Scenarios.scenario_types.MiniScenario import MiniScenario
from Scenarios.scenario_types.TSLengthScenario import TSLengthScenario
from Scenarios.scenario_types.Position_scenario import AnomalyPositionScenario

SCENARIO_CONSTRUCTORS = {BASE_SCENARIO : BaseScenario ,
                         VARY_TS_LENGTH:TSLengthScenario ,
                         VARY_ANOMALY_SIZE: AnomalyLengthScenario,
                         MINI_SCENARIO : MiniScenario,
                         ANOMALY_POSITION : AnomalyPositionScenario}


