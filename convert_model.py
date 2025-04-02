# filepath: c:\Users\adamr\OneDrive\Documents\GitHub\No sTeP oN sNeK!\convert_model.py
from tensorflow import keras
from keras.losses import MeanSquaredError

# Register the 'mse' function as a serializable object
keras.utils.get_custom_objects()['mse'] = MeanSquaredError()

# Convert existing HDF5 model to .keras format
model = keras.models.load_model('snake_ai_model_grinder.h5')  # Load the .h5 model
model.save('snake_ai_model_grinder.keras')  # Save it in .keras format
print("Model successfully converted to .keras format!")