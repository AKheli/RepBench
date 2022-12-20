
let initScoreBoard = function (scores) {
    console.log("initScoreBoard")
    console.log(scores)
    RoundSliders.init(2);
    RoundSliders.updateValue("#RMSE-slider", scores.rmse, 0, scores.original_scores.rmse);
    RoundSliders.setTitle("#RMSE-slider", "RMSE");
    RoundSliders.updateValue("#MAE-slider", scores.mae, 0, scores.original_scores.mae);
    RoundSliders.setTitle("#MAE-slider", "MAE");
    RoundSliders.updateValue("#RMSE-Anomaly-slider", scores.partial_rmse, 0, 2);
    RoundSliders.setTitle("#RMSE-Anomaly-slider", "RMSE on Anomaly");
}
