import flask
import flask_cors
import torch
import torchvision
import PIL
import io
import pathlib

from fastai.vision.all import *
from fastai.callback.core import Callback

class MyVerboseCallback(Callback):
    def after_batch(self):
        if self.iter % 100 == 0:
            print(f"Batch: {self.iter}, Training Loss: {self.loss}")


posix_backup = pathlib.PosixPath
try:
    pathlib.PosixPath = pathlib.WindowsPath
    model_path = pathlib.Path("C:/Users/undoc/Desktop/Fun_Stuff/Code/Github_Stuff/masonacevedo.github.io/fast_ai_model_with_normalization_with_architecture.pkl")
    learn_inf = load_learner(model_path)
finally:
    pathlib.PosixPath = posix_backup

app = flask.Flask(__name__)
flask_cors.CORS(app, origins=["https://masonacevedo.github.io"])

@app.route('/check-for-bird', methods = ["POST"])
def check_for_bird():
    image = flask.request.files.get("user_image")
    if image is None:
        return flask.jsonify(error = "No image provided"),400
    
    # uploaded image -> PIL image object.
    PIL_image_obj = PIL.Image.open(io.BytesIO(image.read()))

    # Convert PIL image to PyTorch Tensor
    transform_obj = torchvision.transforms.ToTensor()
    tensor_image = transform_obj(PIL_image_obj)

    # get metadata
    num_channels, height, width = tensor_image.shape

    

    return flask.jsonify(width = (width), height = (height))