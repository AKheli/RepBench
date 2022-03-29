from Scenarios.scenario_types.AnomalyFactor import AnomalyFactorScenario
from Scenarios.scenario_types.NumberOfTimeSeries import NumberOfTSScenario
from Scenarios.scenario_types.Scenario_Types import *
from Scenarios.scenario_types.AnomalyLengthScenario import AnomalyLengthScenario
from Scenarios.scenario_types.BaseScenario import BaseScenario
from Scenarios.scenario_types.MiniScenario import MiniScenario
from Scenarios.scenario_types.TSLengthScenario import TSLengthScenario
from Scenarios.scenario_types.Position_scenario import AnomalyPositionScenario

SCENARIO_CONSTRUCTORS = {BASE_SCENARIO : BaseScenario ,
                         TS_LENGTH:TSLengthScenario ,
                         ANOMALY_SIZE: AnomalyLengthScenario,
                         MINI_SCENARIO : MiniScenario,
                         ANOMALY_POSITION : AnomalyPositionScenario,
                         ANOMALY_FACTOR : AnomalyFactorScenario,
                         TS_NBR : NumberOfTSScenario}


