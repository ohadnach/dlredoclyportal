def func1():
    from dtlpy.utilities import DatasetGenerator
    import dtlpy as dl
    dataset = dl.datasets.get(dataset_id='611b86e647fe2f865323007a')
    datagen = DatasetGenerator(data_path='train',
                               dataset_entity=dataset,
                               annotation_type=dl.AnnotationType.BOX)


def func2():
    for i in range(5):
        datagen.visualize()


def func3():
    for i in range(5):
        datagen.visualize(10)


def func4():
    from imgaug import augmenters as iaa
    import numpy as np

    augmentation = iaa.Sequential([
        iaa.Resize({"height": 256, "width": 256}),
        # iaa.Superpixels(p_replace=(0, 0.5), n_segments=(10, 50)),
        iaa.flip.Fliplr(p=0.5),
        iaa.flip.Flipud(p=0.5),
        iaa.GaussianBlur(sigma=(0.0, 0.8)),
    ])
    tfs = [
        augmentation,
        np.copy,
        # transforms.ToTensor()
    ]

    datagen = DatasetGenerator(data_path='train',
                               dataset_entity=dataset,
                               annotation_type=dl.AnnotationType.BOX,
                               transforms=tfs)
    datagen.visualize()
    datagen.visualize(10)


def func5():
    print(list(datagen[0].keys()))


def func6():
    import matplotlib.pyplot as plt
    datagen = DatasetGenerator(data_path='train',
                               dataset_entity=dataset,
                               annotation_type=dl.AnnotationType.BOX,
                               return_originals=True,
                               shuffle=False,
                               transforms=tfs)
    fig, ax = plt.subplots(2, 2)

    for i in range(2):
        item_element = datagen[np.random.randint(len(datagen))]
        ax[i, 0].imshow(item_element['image'])
        ax[i, 0].set_title('After Augmentations')
        ax[i, 1].imshow(item_element['orig_image'])
        ax[i, 1].set_title('Before Augmentations')


def func7():
    dataset = dl.datasets.get(dataset_id='6197985a104eb81cb728e4ac')
    datagen = DatasetGenerator(data_path='semantic',
                               dataset_entity=dataset,
                               transforms=tfs,
                               return_originals=True,
                               annotation_type=dl.AnnotationType.SEGMENTATION)
    for i in range(5):
        datagen.visualize()


def func8():
    fig, ax = plt.subplots(2, 4)
    for i in range(2):
        item_element = datagen[np.random.randint(len(datagen))]
        ax[i, 0].imshow(item_element['orig_image'])
        ax[i, 0].set_title('Original Image')
        ax[i, 1].imshow(item_element['orig_annotations'])
        ax[i, 1].set_title('Original Annotations')
        ax[i, 2].imshow(item_element['image'])
        ax[i, 2].set_title('Augmented Image')
        ax[i, 3].imshow(item_element['annotations'])
        ax[i, 3].set_title('Augmented Annotations')


def func9():
    item_element = datagen[np.random.randint(len(datagen))]
    annotations = item_element['annotations']
    unique_labels = np.unique(annotations)
    one_hot_annotations = np.arange(len(datagen.id_to_label_map)) == annotations[..., None]
    print('unique label indices in the item: {}'.format(unique_labels))
    print('unique labels in the item: {}'.format([datagen.id_to_label_map[i] for i in unique_labels]))
    plt.figure()
    plt.imshow(item_element['image'])
    fig = plt.figure()
    for i_label_ind, label_ind in enumerate(unique_labels[:8]):
        ax = fig.add_subplot(2, 4, i_label_ind + 1)
        ax.imshow(one_hot_annotations[:, :, label_ind])
        ax.set_title(datagen.id_to_label_map[label_ind])


def func10():
    # project = dl.projects.get(project_name='Semantic')
    # dataset = project.datasets.get(dataset_name='Hamster')
    # dataset.items.upload(local_path='assets/images/hamster.jpg',
    #                      local_annotations_path='assets/images/hamster.json')
    dataset = dl.datasets.get(dataset_id='621ddc855c2a3d151451ec58')
    datagen = DatasetGenerator(data_path='semantic',
                               dataset_entity=dataset,
                               return_originals=True,
                               overwrite=True,
                               annotation_type=dl.AnnotationType.SEGMENTATION)
    datagen.visualize()
    data_item = datagen[0]
    plt.imshow(data_item['annotations'])
    print('BG value: {}'.format(data_item['annotations'][0, 0]))


def func11():
    dataset = dl.datasets.get(dataset_id='6197985a104eb81cb728e4ac')
    label_to_id_map = {'cat': 1,
                       'dog': 1,
                       '$default': 0}
    dataloader = DatasetGenerator(data_path='semantic',
                                  dataset_entity=dataset,
                                  transforms=tfs,
                                  return_originals=True,
                                  label_to_id_map=label_to_id_map,
                                  annotation_type=dl.AnnotationType.SEGMENTATION)
    for i in range(5):
        dataloader.visualize()


def func12():
    dataset = dl.datasets.get(dataset_id='611b86e647fe2f865323007a')
    datagen = DatasetGenerator(data_path='train',
                               dataset_entity=dataset,
                               batch_size=10,
                               annotation_type=dl.AnnotationType.BOX)
    batch = datagen[0]
    print('type: {}, len: {}'.format(type(batch), len(batch)))
    print('single element in the list: {}'.format(batch[0]['image']))
    # with collate
    from dtlpy.utilities.dataset_generators import collate_default
    datagen = DatasetGenerator(data_path='train',
                               dataset_entity=dataset,
                               collate_fn=collate_default,
                               batch_size=10,
                               annotation_type=dl.AnnotationType.BOX)
    batch = datagen[0]
    print('type: {}, len: {}, shape: {}'.format(type(batch['images']), len(batch['images']), batch['images'].shape))
