


let scoreBoardLoadeer = function () {}
const createScoreBoard = function () {
    RoundSliders.init(2);
    RoundSliders.updateValue("#RMSE-slider", 0, 0, 0);
    RoundSliders.setTitle("#RMSE-slider", "RMSE");
    RoundSliders.updateValue("#MAE-slider", 0, 0, 0);
    RoundSliders.setTitle("#MAE-slider", "MAE");
    RoundSliders.updateValue("#RMSE-Anomaly-slider", 0, 0);
    RoundSliders.setTitle("#RMSE-Anomaly-slider", "RMSE on Anomaly");
    scoreBoardLoadeer = setDivLoading("score_container");
}

const updateScoreBoard = function (scores) {
    RoundSliders.init(2);
    RoundSliders.updateValue("#RMSE-slider", scores.rmse, 0, scores.original_scores.rmse);
    RoundSliders.setTitle("#RMSE-slider", "RMSE");
    RoundSliders.updateValue("#MAE-slider", scores.mae, 0, scores.original_scores.mae);
    RoundSliders.setTitle("#MAE-slider", "MAE");
    RoundSliders.updateValue("#RMSE-Anomaly-slider", scores.partial_rmse, 0, 2);
    RoundSliders.setTitle("#RMSE-Anomaly-slider", "RMSE on Anomaly");
    scoreBoardLoadeer();
}

