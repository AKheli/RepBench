from __future__ import absolute_import, unicode_literals
import os
import logging
import numpy as np
import pandas as pd
from celery import Celery, shared_task
from contextlib import redirect_stdout
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RepBenchWeb.settings')

app = Celery('RepBenchWeb')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

from flaml import AutoML
import sys
import warnings
import os
from django.core.cache import cache



logger = logging.getLogger(__name__)


def revoke_task(task_id):
    from celery.contrib.abortable import AbortableAsyncResult
    task = AbortableAsyncResult(task_id)
    task.abort()
    task.revoke(terminate=True)


from sklearn.metrics import f1_score ,accuracy_score
metrics = {
    "accuracy" : accuracy_score,
    "micro_f1" : lambda y_true, y_pred : f1_score(y_true, y_pred, average='micro'),
    "macro_f1" : lambda y_true, y_pred : f1_score(y_true, y_pred, average='macro')
}


@shared_task(bind=True)
def flaml_search_task(self, automl_settings, X_train_dict, y_train_list, my_task_id):

    from RepBenchWeb.models import TaskData
    task_data = TaskData(task_id=my_task_id, data_type="flaml" , celery_task_id=self.request.id)
    task_data.save()

    X_train = pd.DataFrame.from_dict(X_train_dict)
    y_train = np.array(y_train_list)
    automl = AutoML(**automl_settings)
    normal_write = sys.stdout.write
    setting_metric = automl_settings["metric"]

    def custom_metric(
            X_val, y_val, estimator, labels,
            X_train, y_train, weight_val=None, weight_train=None,
            *args,
    ):
        import time
        start = time.time()
        pred_time = (time.time() - start) / len(X_val)
        y_pred = estimator.predict(X_train)
        print("score parameters" , y_train,y_pred)

        score = metrics[setting_metric](y_train, y_pred)
        task_data.add_data({"score": score , "pred_time": pred_time , "estimator": estimator.__class__.__name__})
        return score, {"pred_time": pred_time}


    # Initialize FLAML with custom metric
    automl = AutoML()

    automl_settings["metric"] = custom_metric
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        automl.fit(X_train=X_train, y_train=y_train,  **automl_settings, n_jobs=3 , verbose=-3)

    task_data.set_autoML(automl)
    task_data.set_done()


