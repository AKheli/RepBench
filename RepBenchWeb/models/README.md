# Django Model Manipulation


## Accessing the Django Shell
```bash
 sudo docker exec -it repbench-web-1 python3 manage.py shell
```
Remark that `repbench-web-1` is the name of the container running the Django web server. You can find the name of your container by running `sudo docker ps` and looking for the container with the `repbench_web` image.


## Store a Dataset
Add the data set to [models](RepBenchWeb/models/datasetsConfig.py)
The store folder root is the data folder.

In the shell:
```python
from RepBenchWeb.models.populateDB import *
```

## Deleting a Model Instance

To delete a model instance via Django shell, follow these steps:

1. Import the model you want to manipulate. For example, if we want to delete an instance of `InjectedContainer`, we would use:
2. (Optional) View all instances of your model to help identify the one you want to delete. For `InjectedContainer`, you can do this with:
3. Delete the desired instance. For example, to delete `InjectedContainer` instances with the title "test", use:
```python
from RepBenchWeb.models import InjectedContainer
InjectedContainer.objects.all()
InjectedContainer.objects.filter(title="test").delete()

```

## Updating Feature Values

```python
from RepBenchWeb.models.data_models import DataSet
[d.compute_features() for d in DataSet.objects.all()]
```




## Adding a New Field Without Reinitializing the Whole Table

Django's migration system allows you to add new fields to models without having to delete and recreate the entire table. The following StackOverflow post provides a detailed guide: 

[How to add a new field to a model with new Django migrations](https://stackoverflow.com/questions/24311993/how-to-add-a-new-field-to-a-model-with-new-django-migrations)