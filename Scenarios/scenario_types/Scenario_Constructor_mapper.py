from Scenarios.scenario_types.AnomalyRate import AnomalyRateScenario
from Scenarios.scenario_types.ContaminatedTSNumber import ContaminatedNumberOfTSScenario
from Scenarios.scenario_types.NumberOfTimeSeries import NumberOfTSScenario
from Scenarios.ScenarioConfig import *
from Scenarios.scenario_types.AnomalyLengthScenario import AnomalyLengthScenario
from Scenarios.scenario_types.BaseScenario import BaseScenario
from Scenarios.scenario_types.TSLengthScenario import TSLengthScenario

SCENARIO_CONSTRUCTORS = {BASE_SCENARIO: BaseScenario,
                         TS_LENGTH: TSLengthScenario,
                         ANOMALY_SIZE: AnomalyLengthScenario,
                         ANOMALY_RATE: AnomalyRateScenario,
                         TS_NBR: NumberOfTSScenario,
                         CTS_NBR: ContaminatedNumberOfTSScenario
                         }
