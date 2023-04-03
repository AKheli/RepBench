default_set = "BAFU"

data_sets_info = {
    "BAFU": {
        "title": "BAFU",
        "path": "train/bafu5k.csv",
        "ref_url": "https://www.bafu.admin.ch/bafu/en/home.html",
        "url_text":"Federal Office for the Environment",
        "description" : "Measurement of the water level in different rivers in Switzerland",
    },
    "Humidity": {
        "title": "Humidity",
        "path": "train/humidity.csv",
        "ref_url": "https://www.meteoswiss.admin.ch/",
        "url_text" : "MeteoSwiss",
        "description": "Humidity in different cities",

    },
    "SMD": {
        "title": "Server Machine Dataset",
        "path": "train/smd1_5.csv",
        "ref_url": "https://github.com/NetManAIOps/OmniAnomaly",
        "url_text": "Omni Anomaly",
         "description": "Measurement of different metrics like  the CPU and memory usage of a server machine",

},
    "Electricity": {
        "title": "Electricity",
        "path": "train/elec.csv",
        "ref_url": "https://archive.ics.uci.edu/ml/datasets/ElectricityLoadDiagrams20112014",
        "url_text": "UCI Machine Learning Repository",
    },

    "Tiny": {
        "title": "Tiny",
        "path": "train/tiny.csv",
        "ref_url": "-",
        "url_text": "",
        "description": "test data",
    },

    "MotorImagery_finger": {
        "title": "Tiny",
        "path": "train/MotorImagery_finger.csv",
        "ref_url": "-",
        "url_text": "",
        "description": "test data",
    },

    "MotorImagery_tongue": {
        "title": "Tiny",
        "path": "train/MotorImagery_tongue.csv",
        "ref_url": "-",
        "url_text": "",
        "description": "test data",
    },
}
