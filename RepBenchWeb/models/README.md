# Django Model Manipulation

This document contains instructions for common tasks involving Django models.

## Deleting a Model Instance

To delete a model instance via Django shell, follow these steps:

1. Open the Django shell by running this command in your terminal:

```bash
python3 manage.py shell
```

2. Import the model you want to manipulate. For example, if we want to delete an instance of `InjectedContainer`, we would use:
3. (Optional) View all instances of your model to help identify the one you want to delete. For `InjectedContainer`, you can do this with:
4. Delete the desired instance. For example, to delete `InjectedContainer` instances with the title "test", use:
```python
from RepBenchWeb.models import InjectedContainer
InjectedContainer.objects.all()
InjectedContainer.objects.filter(title="test").delete()

```




## Adding a New Field Without Reinitializing the Whole Table

Django's migration system allows you to add new fields to models without having to delete and recreate the entire table. The following StackOverflow post provides a detailed guide: 

[How to add a new field to a model with new Django migrations](https://stackoverflow.com/questions/24311993/how-to-add-a-new-field-to-a-model-with-new-django-migrations)