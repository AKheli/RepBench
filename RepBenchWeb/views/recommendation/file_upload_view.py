import csv
import io
import json

import pandas as pd
from django.core.files.uploadedfile import UploadedFile
from django.shortcuts import render, redirect
from RepBenchWeb.forms.file_upload import UploadFilesForm
from RepBenchWeb.ts_manager.HighchartsMapper import map_truth_data, map_repair_data
from recommendation.recommend import get_recommendation_non_containerized

from RepBenchWeb.utils.encoder import RepBenchJsonEncoder


def django_file_to_pandas(uploaded_file: UploadedFile) -> pd.DataFrame:
    # Check if the file is comma or whitespace-separated
    uploaded_file.open('r')
    dialect = csv.Sniffer().sniff(uploaded_file.readline().decode('utf-8'))
    uploaded_file.seek(0)
    delimiter: str = dialect.delimiter

    # Read the first few lines to infer if the first row contains column names or data
    first_line = uploaded_file.readline().decode('utf-8').strip()
    second_line = uploaded_file.readline().decode('utf-8').strip()
    uploaded_file.seek(0)

    has_header = csv.Sniffer().has_header(first_line + '\n' + second_line)

    # Read the file into a pandas DataFrame
    if has_header:
        df = pd.read_csv(uploaded_file, delimiter=delimiter)
    else:
        df = pd.read_csv(uploaded_file, delimiter=delimiter, header=None)

    return df


def upload_files(request):
    upload_form = UploadFilesForm()
    if request.method == 'POST':
        form = UploadFilesForm(request.POST, request.FILES)
        if form.is_valid():
            file1 = request.FILES['file1']
            file2 = request.FILES.get('file2', None)
            file3 = request.FILES.get('file3', None)
            column_for_recommendation = int(request.POST.get('column-id', -1))
            column_name = request.POST.get('column-name')

            # Process the files as needed
            # df = handle_uploaded_file(file1)
            df = django_file_to_pandas(file1)
            recommendation = get_recommendation_non_containerized(df,
                                                                  column_for_recommendation=column_for_recommendation)

            n, m = df.shape
            uploaded_file_name = file1.name.split(".")[0]
            data_info = {
                'column_name': column_name,
                'column_id': column_for_recommendation,
                'values': n * m,
                'file_name': uploaded_file_name,
                "ts_nbr": m,
                "ts_len": n,
            }

            highcharts_series = map_truth_data(df)
            highcharts_series[column_for_recommendation]['name'] = str(
                highcharts_series[column_for_recommendation]['name']) + "(reccomended)"

            repaired_series = [
                {
                    "id": "repair" + alg_name,
                    "name": alg_name,
                    "data": repaired_df.iloc[:, column_for_recommendation].tolist(),
                    "norm_data": repaired_df.iloc[:, column_for_recommendation].tolist(),
                    "series_type" : "repair",
                    "legendIndex": -1
                } for alg_name, repaired_df in recommendation["alg_repairs"].items()
            ]
            recommendation.pop("alg_repairs")
            highcharts_series += repaired_series
            highcharts_series = json.dumps(highcharts_series, cls=RepBenchJsonEncoder)
            recommendation_data = json.dumps(recommendation, cls=RepBenchJsonEncoder)
            return render(request, 'recommendation/user_recommendation.html',
                          {'data_info': data_info, "highcharts_series": highcharts_series,
                           "recommendation_data": recommendation_data})

        else:
            print("form is not valid")

    return render(request, 'recommendation/user_recommendation_start.html', {'upload_form': upload_form})
