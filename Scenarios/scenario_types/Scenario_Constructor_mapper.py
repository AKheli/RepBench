from Scenarios.scenario_types.AnomalyLengthScenario import AnomalyLengthScenario
from Scenarios.scenario_types.BaseScenario import BaseScenario
from Scenarios.scenario_types.TSLengthScenario import TSLengthScenario
from Scenarios.scenario_types.Scenario_Types import BASE_SCENARIO, VARY_TS_LENGTH, VARY_ANOMALY_SIZE


SCENARIO_CONSTRUCTORS = {BASE_SCENARIO : BaseScenario ,
                         VARY_TS_LENGTH:TSLengthScenario ,
                         VARY_ANOMALY_SIZE: AnomalyLengthScenario}