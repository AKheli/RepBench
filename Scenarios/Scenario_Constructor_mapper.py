from Scenarios.AnomalyLengthScenario import AnomalyLengthScenario
from Scenarios.BaseScenario import BaseScenario
from Scenarios.TSLengthScenario import TSLengthScenario
from Scenarios.Scenario_Types import BASE_SCENARIO, VARY_TS_LENGTH, VARY_ANOMALY_SIZE


SCENARIO_CONSTRUCTORS = {BASE_SCENARIO : BaseScenario ,
                         VARY_TS_LENGTH:TSLengthScenario ,
                         VARY_ANOMALY_SIZE: AnomalyLengthScenario}