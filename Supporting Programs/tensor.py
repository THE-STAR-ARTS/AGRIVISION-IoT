import tflite_runtime.interpreter as tflite
import machine
import time
import numpy as np

# Load TensorFlow Lite model
model_path = "weather_model.tflite"
interpreter = tflite.Interpreter(model_path=model_path)
interpreter.allocate_tensors()

# Get input and output details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Dummy input (replace with actual sensor data)
input_data = np.array([[30.0, 20.0, 35.0, 25.0, 27.0, 15.0, 80.0, 2.0, 50.0, 5.0, 90.0, 3.0, 10000.0, 500.0, 7.0, 29.0]], dtype=np.float32)

# Ensure input shape matches model requirements
input_data = input_data.reshape(input_details[0]['shape'])

# Load data into the model
interpreter.set_tensor(input_details[0]['index'], input_data)

# Run inference
interpreter.invoke()

# Get predictions
output_data = interpreter.get_tensor(output_details[0]['index'])

# Display results
print("Predicted Temp:", output_data[0][0])
print("Predicted Humidity:", output_data[0][1])
print("Predicted Precip:", output_data[0][2])

