## Getting Started  
  
This tutorial will help you get started with the basics of model management:  
* logging metrics only (aka “offline mode”)  
* downloading pretrained model for local training and inference  
* deploying pretrained models from the AI library onto the Dataloop platform  
  
### Logging metrics  
To export metrics for tracking model performance, you need to create a dummy package (with a dummy codebase reference) and model (including a valid dataset ID). Remember to replace <project_name> and <dataset_id> with the appropriate strings to reference your project and dataset.  
  

```python
import dtlpy as dl
import os
project = dl.projects.get(project_name='<project_id>')
package = project.packages.push(package_name='dummy-model-package',
                                codebase=dl.entities.LocalCodebase(os.getcwd()),
                                modules=[])
model = package.models.create(model_name='My Model',
                              description='model for offline model logging',
                              dataset_id='<dataset_id>',
                              labels=[])
```
  
Once you’ve created these two entities, metrics can be sent to the platform with the `model.add_log_samples` command.  
Here is an example:  

```python
epoch = np.linspace(0, 9, 10)
epoch_metric = np.linspace(0, 9, 10)
for x_metric, y_metric in zip(epoch, epoch_metric):
    model.add_log_samples(samples=dl.LogSample(figure='tutorial plot',
                                               legend='some metric',
                                               x=x_metric,
                                               y=y_metric),
                          dataset_id=model.dataset_id)
```
Metrics plots will appear under the “metrics” tab of your chosen model, and will look something like this:  
![Screenshot of model metrics plot](https://github.com/dataloop-ai/dtlpy-documentation/blob/model_mgmt_3/assets/images/model_management/metrics_example.png/)  
  
### Using pretrained models from the AI library  
  
The Dataloop AI library includes various architectures and pretrained models that can be used for inference or further training.  
  
To see available public models, filter all available packages:  
  

```python
filters = dl.Filters(resource=dl.FiltersResource.PACKAGE, use_defaults=False)
filters.add(field='scope', values='public')
dl.packages.list(filters=filters).print()
```
Public models can be downloaded to your machine for local training and inference, or they can be trained and deployed on the cloud for integration into the Dataloop platform.  
  
### Dataset Subsets  
Our public models use a train/validation split of the dataset for the training session. To avoid data leakage between training sessions and to make each training reproducible,  
we will determine the data subsets and save the split type to the dataset entity (using a DQL). Using DQL filters you can subset the data however you like.  
  
For example, if your dataset is split between folders, you can use this DQL to add metadata for all items in the dataset  

```python
dataset.metadata['system']['subsets'] = {
    'train': json.dumps(dl.Filters(field='dir', values='/train').prepare()),
    'validation': json.dumps(dl.Filters(field='dir', values='/validation').prepare()),
}
dataset.update(system_metadata=True)
```
This way, when the training starts, the sets will be downloaded using the DQL and any future training session on this dataset will have the same subsets of data.  
  
NOTE: In the future, this mechanism will be expanded to use a tagging system on items. This will allow more flexible data subsets and random data allocation.  
  
### Deploying a model remotely  
  
Download the model and package you want to copy it to your project. Since the public model is pretrained, it can be deployed without any further action.  
  

```python
public_model = dl.models.get(model_id="<model_id>")
model = project.models.clone(from_model=public_model,
                             model_name='remote_model',
                             project_id=project.id)
model.deploy()
```
If you want to customize the public model (for transfer-learning or fine-tuning), you can indicate the new dataset and labels for model training.  
  

```python
custom_model = dl.models.clone(from_model=public_model,
                               model_name='remote_custom_model',
                               dataset=dataset,
                               project_id=project.id,
                               labels=['label1', 'label2'])
model.train()
model.deploy()
```
A model can be trained with a new dataset with `model.train()`.  
  
A model can only be deployed after it's been trained. `model.deploy()` automatically creates a bot and service for the trained model.  
  
Now the model is deployed, you can create a UI slot to inference on individual data items on the platform, or call the model to inference in a FaaS.  
  
### Downloading a model for local training and inferencing  
  
For local training and inferecing, you need to download the package codebase to get build the model adapter that you need to run the train and predict methods. Follow the same steps as above to copy the public model to your project. Then download the model's package codebase to build and load the model adapter.  
  
