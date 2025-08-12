import io
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import matplotlib.pyplot as plt
import base64
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import matplotlib
matplotlib.use('Agg')  # Use a non-GUI backend for Django
import matplotlib.pyplot as plt




# Define class names
class_folder_names = [
    'adenocarcinoma_left.lower.lobe_T2_N0_M0_Ib',
    'large.cell.carcinoma_left.hilum_T2_N2_M0_IIIa',
    'normal',
    'squamous.cell.carcinoma_left.hilum_T1_N2_M0_IIIa',
]


# Load the trained model
import os
import pickle
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'best_model.pkl')
with open(MODEL_PATH, 'rb') as file:
        loaded_model = pickle.load(file)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'detection/register.html', {'form': form})


@login_required
def predict_image(request):
    if request.method == 'POST' and request.FILES['image']:
        # Handle the uploaded file
        uploaded_image = request.FILES['image']


        # Convert the uploaded file to a BytesIO object
        image_bytes = io.BytesIO(uploaded_image.read())


        # Preprocess the image
        target_size = (224, 224)
        random_image = load_img(image_bytes, target_size=target_size)
        random_img_array = img_to_array(random_image)
        flattend_img_array = random_img_array.reshape(1, -1)


        # Make predictions
        predictions = loaded_model.predict(flattend_img_array)
        predicted_class = class_folder_names[predictions[0]]
        if predicted_class == "normal":
            messages.error(request, "Error: The uploaded image is not related to lung cancer.")
            return redirect('/detection/predict/')  # Redirect using the full path  


        # Convert the image to Base64 for rendering in HTML
        plt.imshow(random_image)
        plt.title(f"Predicted class: {predicted_class}")
        plt.axis('off')
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        image_base64 = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()


        context = {
            'predicted_class': predicted_class,
            'image_base64': image_base64,
        }
        return render(request, 'detection/result.html', context)


    return render(request, 'detection/predict.html')


