`convert_mapillary_instances.py` converts the instance images in the Mapillary dataset (containing both v1.2 and v2.0) into the label images I need, consisting of 9 classes (including background, excluding void). I manually inspected all of the original instances used to create the new labels. For instance, the classes 'Ground' and 'Traffic Island' in v2.0 are sometimes walkable and other times unwalkable, so I classify them as void. I include the sidewalk labels from v1.2 because v2.0 introduces a class 'Driveway' that often overwrites areas that were sidewalk in v1.2 and should be classified sidewalk.

`calculate_dataset_mean_std.py` calculates the mean and standard deviation of the images in the Mapillary dataset. I use these values during training, validation, and model deployment. See the comments in this file for the values.

I used these converted labels and dataset statistics to train a model using PaddleSeg.

For training:

`mapillary.py` should be placed in `paddleseg/datasets`. Then modify `paddleseg/datasets/__init__.py` by adding `from .mapillary import Mapillary` to the end of the file.

`pp_mobileseg_tiny_mapillary.yml` is a sample training config.

Training command:

`python tools/train.py --config configs/pp_mobileseg/pp_mobileseg_tiny_mapillary.yml`

Validation command (assuming the number of iterations is 225000):

`python tools/val.py --config configs/pp_mobileseg/pp_mobileseg_tiny_mapillary.yml --model_path output/iter_225000/model.pdparams`

Exporting (assuming 225000 iters and an intended model input shape of 480x480):

`python tools/export.py --config configs/pp_mobileseg/pp_mobileseg_tiny_mapillary.yml --model_path output/iter_225000/model.pdparams --input_shape 1 3 480 480`

Converting to onnx format:

`paddle2onnx --model_dir path_to_PaddleSeg_repository --model_filename output/inference_model/model.pdmodel --params_filename output/inference_model/model.pdiparams --save_file output/model.onnx --enable_dev_version True --opset_version 15`

***

After training, I convert the model to .onnx. This model doesn't have the mean/std normalization, so I manually add two layers to do this using [onnx-modifier](https://github.com/ZhangGe6/onnx-modifier).

Immediately after the input, add a subtraction layer with the following values:
```
[[[[0.4217]]
  [[0.4606]]
  [[0.4720]]]]
```
And the following type:
```
float32[1,3,1,1]
```
Then add a division layer after that with the following values and type:
```
[[[[0.2646]]
  [[0.2754]]
  [[0.3035]]]]
```
```
float32[1,3,1,1]
```
So if the original model begins with `input -> conv`, the modified version will be `input -> sub -> div -> conv`.