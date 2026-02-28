from fastapi import FastAPI
from pydantic import BaseModel
import tensorflow as tf
import numpy as np

# Initialize FastAPI app
app = FastAPI()

# Load the TFLite model
interpreter = tf.lite.Interpreter(model_path='mnist_model.tflite')
interpreter.allocate_tensors()

# Get input and output details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Define Pydantic model for request body
class ImageData(BaseModel):
    pixels: list[float]

@app.post("/predict")
async def predict(data: ImageData):
    # Convert input pixels to a NumPy array
    input_array = np.array(data.pixels, dtype=np.float32)

    # Reshape to the expected input format (1, 28, 28, 1)
    # The model was trained with normalized images, so ensure input is normalized if not already.
    # In this case, the model expects normalized pixel values (0-1), assuming the input 'pixels' are already normalized.
    input_shape = input_details[0]['shape']
    if len(input_array) != input_shape[1] * input_shape[2]:
        return {"error": "Input pixel count does not match expected image size (28x28)"}

    input_data = input_array.reshape(input_shape)

    # Set the tensor
    interpreter.set_tensor(input_details[0]['index'], input_data)

    # Invoke the interpreter
    interpreter.invoke()

    # Retrieve output tensor
    output_data = interpreter.get_tensor(output_details[0]['index'])

    # Get the predicted class (index with highest probability)
    predicted_class = np.argmax(output_data[0]).item()

    return {"predicted_class": predicted_class, "probabilities": output_data[0].tolist()}


