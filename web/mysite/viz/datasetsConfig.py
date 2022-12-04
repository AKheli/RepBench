default_set = "BAFU"

data_sets_info = {
    "BAFU": {
        "name": "BAFU",
        "path": "train/bafu5k.csv",
        "ref_url": "https://www.bafu.admin.ch/bafu/en/home.html",
        "url_text":"Federal Office for the Environment",
    },
    "Humidity": {
        "name": "Humidity",
        "path": "train/humidity.csv",
        "ref_url": "https://www.meteoswiss.admin.ch/",
        "url_text" : "MeteoSwiss",

    },
    "SMD": {
        "name": "Server Machine Dataset",
        "path": "train/smd1_5.csv",
        "ref_url": "https://github.com/NetManAIOps/OmniAnomaly",
        "url_text": "Omni Anomaly"
    },
    "Electricity": {
        "name": "Electricity",
        "path": "train/elec.csv",
        "ref_url": "https://archive.ics.uci.edu/ml/datasets/ElectricityLoadDiagrams20112014",
        "url_text": "UCI Machine Learning Repository"
    },

    "Tiny": {
        "name": "Tiny",
        "path": "train/tiny.csv",
        "ref_url": "-",
        "url_text": ""
    },
}
