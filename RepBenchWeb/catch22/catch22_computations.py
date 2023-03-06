def catch_22_features(df):
    context = {}
    ### catch22 features
    import pycatch22
    context["catch22"] = {}

    features_min_max = {}  # name: {min: min_val , max: max_val}
    for i, ts in enumerate(df.columns):
        ts_data = df[ts].values
        features = pycatch22.catch22_all(ts_data)
        if i == 0:
            features_min_max = {name: {} for name in features["names"]}
        features = {name: round(val, 4) for name, val in zip(features["names"], features["values"])}
        if i == 0:
            features_min_max = {name: {"min": val, "max": val} for name, val in features.items()}
        for name, val in features.items():
            if val < features_min_max[name].get("min"):
                features_min_max[name]["min"] = val
            if val > features_min_max[name].get("max"):
                features_min_max[name]["max"] = val
        context["catch22"][ts] = features
    for i, ts in enumerate(df.columns):
        for name, val in context["catch22"][ts].items():
            context["catch22"][ts][name] = {"value": val, "min": features_min_max[name]["min"],
                                            "max": features_min_max[name]["max"]}

    context["catch22_min_max"] = features_min_max
    return context
