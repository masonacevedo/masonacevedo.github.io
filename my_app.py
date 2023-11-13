import flask
import flask_cors
import torch
import torchvision
import PIL
import io
import pathlib


from fastai.vision.all import *

app = flask.Flask(__name__)

posix_backup = pathlib.PosixPath
try:
    pathlib.PosixPath = pathlib.WindowsPath
    model_path = pathlib.Path("C:/Users/undoc/Desktop/Fun_Stuff/Code/Github_Stuff/masonacevedo.github.io/fast_ai_model_with_normalization_with_architecture.pkl")
                            
    model = load_learner(model_path)
finally:
    pathlib.PosixPath = posix_backup


flask_cors.CORS(app, origins=["https://masonacevedo.github.io"])

@app.route('/check-for-bird', methods = ["POST"])
def check_for_bird():

    image = flask.request.files.get("user_image")
    if image is None:
        return flask.jsonify(error = "No image provided"),400

    print("Image:")
    print(image)

    PIL_image_object = Image.open(io.BytesIO(image.read()))
    PIL_image_object.save("C:/Users/undoc/Downloads/pil_image.jpg")
    fastai_image = PILImage.create(PIL_image_object)
    fastai_image.save("C:/Users/undoc/Downloads/fast_image.jpg")

    prediction, probability = categorize_image(fastai_image)
    return flask.jsonify(prediction = (prediction), probability = (probability))


def categorize_image(im):
    print("type(im)",type(im))
    resized_image = Resize(192, method = 'squish')(im)

    mean = [0.4771, 0.4596, 0.4162]
    stddev = [0.2288, 0.2205, 0.2198]

    normalized_resized_image = Normalize.from_stats(mean, stddev)(resized_image)

    prediction = model.predict(normalized_resized_image)

    category = str(prediction[0])
    if category == "bird":
        probability = prediction[2][2].item()
    else:
        probability = 1 - prediction[2][2].item()
    
    return category, probability