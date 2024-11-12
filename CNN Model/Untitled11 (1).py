#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().system('pip install tensorflow keras numpy matplotlib')
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import VGG16  # Import VGG16 here
from tensorflow.keras import models, layers
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing import image

get_ipython().system('pip install pillow pillow-heif')


# Load VGG16 without the top layers
base_model = VGG16(weights='imagenet', include_top=False, input_shape=(150, 150, 3))
base_model.trainable = False

# Add custom layers
model = models.Sequential([
    base_model,
    layers.Flatten(),
    layers.Dense(512, activation='relu'), 
    layers.Dropout(0.5),
    layers.Dense(1, activation='sigmoid')  # Binary classification
])

# Compile the model
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.00005),
              loss='binary_crossentropy', metrics=['accuracy'])

# Data augmentation
train_datagen = ImageDataGenerator(
    rescale=1./255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
)
test_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    'C:/Users/shah/Desktop/AIS Project/Dataset/Train',
    target_size=(150, 150),
    batch_size=16,
    class_mode='binary'
)
test_generator = test_datagen.flow_from_directory(
    'C:/Users/shah/Desktop/AIS Project/Dataset/Test',
    target_size=(150, 150),
    batch_size=16,
    class_mode='binary',
    shuffle=False
)

# Wrapping generators in tf.data.Dataset and adding repeat()
train_dataset = tf.data.Dataset.from_generator(
    lambda: train_generator,
    output_signature=(
        tf.TensorSpec(shape=(None, 150, 150, 3), dtype=tf.float32),
        tf.TensorSpec(shape=(None,), dtype=tf.float32)
    )
).repeat()

test_dataset = tf.data.Dataset.from_generator(
    lambda: test_generator,
    output_signature=(
        tf.TensorSpec(shape=(None, 150, 150, 3), dtype=tf.float32),
        tf.TensorSpec(shape=(None,), dtype=tf.float32)
    )
).repeat()

# Calculate steps per epoch
steps_per_epoch = np.ceil(train_generator.samples / train_generator.batch_size).astype(int)
validation_steps = np.ceil(test_generator.samples / test_generator.batch_size).astype(int)

# Train the model
history = model.fit(
    train_dataset,
    steps_per_epoch=steps_per_epoch,
    epochs=50,
    validation_data=test_dataset,
    validation_steps=validation_steps
)

# Save the trained model in the Keras format (.keras)
model.save('real_vs_fake_vgg16_model.keras')

# Evaluate the model
test_loss, test_acc = model.evaluate(test_dataset, steps=validation_steps)
print(f'Test Accuracy: {test_acc * 100:.2f}%')

# Load the trained model
model = tf.keras.models.load_model('real_vs_fake_vgg16_model.keras')

# Function to load and preprocess the input image
def load_and_preprocess_image(img_path, target_size=(150, 150)):
    # Load the image from the file path
    img = image.load_img(img_path, target_size=target_size)
    
    # Convert the image to a numpy array
    img_array = image.img_to_array(img)
    
    # Expand dimensions to match the model's input shape (add batch dimension)
    img_array = np.expand_dims(img_array, axis=0)
    
    # Rescale the image to match the training data (normalization)
    img_array /= 255.0
    
    return img_array

# Function to predict whether the image is Real or Fake
def predict_image(img_path):
    # Preprocess the image
    preprocessed_image = load_and_preprocess_image(img_path)
    
    # Make prediction
    prediction = model.predict(preprocessed_image)
    # Show the image
    img = image.load_img(img_path)
    plt.imshow(img)
    plt.axis('off')  # Hide the axis
    plt.show()
    
    # Interpret the result
    if prediction[0] > 0.5:
        print(f'The image is predicted as: Real (Probability: {prediction[0][0]})')
    else:
        print(f'The image is predicted as: Fake (Probability: {prediction[0][0]})')

# Example usage: Input the file path of an image you want to predict
img_path = r'C:\Users\shah\Desktop\AIS Project\Real Airpods\IMG_8426.jpg'  # Replace with your image path
predict_image(img_path)





# In[ ]:




