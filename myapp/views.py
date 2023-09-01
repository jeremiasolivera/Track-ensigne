from django.shortcuts import render,redirect,get_object_or_404
import cv2
import os
import face_recognition
from .models import Paciente
from django.contrib.auth.decorators import login_required
from .form import PacienteForm

@login_required
def extract_faces(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        patient_age = int(request.POST.get('patient_age'))
        patient_report = request.POST.get('patient_report')
        patient_name = request.POST.get('patient_name')  # Obtén el nombre del paciente del formulario
        imagesPath = "C:/Users/alexi/OneDrive/Escritorio/Programming/django_recognition/core/faces"

        if not os.path.exists(imagesPath):
            os.makedirs(imagesPath)
            print("Nueva carpeta: faces")

        image_path = os.path.join(imagesPath, f"{patient_name}.jpg")  # Usa el nombre del paciente como nombre de archivo
        with open(image_path, 'wb') as f:
            for chunk in image.chunks():
                f.write(chunk)
        paciente = Paciente(nombre=patient_name, imagen=image, edad=patient_age, informe_medico=patient_report)
        paciente.save()
        # Código para el procesamiento de imágenes y extracción de rostros
        faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

        image = cv2.imread(image_path)
        faces = faceClassif.detectMultiScale(image, 1.1, 5)
        for (x, y, w, h) in faces:
            face = image[y:y + h, x:x + w]
            face = cv2.resize(face, (150, 150))
            new_face_filename = f"{patient_name}.jpg"  # Usa el nombre del paciente como nombre de archivo
            cv2.imwrite(os.path.join(imagesPath, new_face_filename), face)

        # return redirect('recognition')  # Redirige a la vista de reconocimiento

    return render(request, 'extract_faces.html')




@login_required
def recognition(request):
        imageFacesPath = "C:/Users/alexi/OneDrive/Escritorio/Programming/django_recognition/core/faces"

        facesEncodings = []
        facesNames = []
        for file_name in os.listdir(imageFacesPath):
            image = cv2.imread(os.path.join(imageFacesPath, file_name))
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            f_coding = face_recognition.face_encodings(image, known_face_locations=[(0, 150, 150, 0)])[0]
            facesEncodings.append(f_coding)
            facesNames.append(file_name.split(".")[0])

        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        # Detector facial
        faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.flip(frame, 1)
            orig = frame.copy()
            faces = faceClassif.detectMultiScale(frame, 1.1, 5)

            for (x, y, w, h) in faces:
                face = orig[y:y + h, x:x + w]
                face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
                actual_face_encoding = face_recognition.face_encodings(face, known_face_locations=[(0, w, h, 0)])[0]
                result = face_recognition.compare_faces(facesEncodings, actual_face_encoding)
                if True in result:
                    index = result.index(True)
                    name = facesNames[index]
                    color = (125, 220, 0)
                else:
                    name = "Desconocido"
                    color = (50, 50, 255)

                cv2.rectangle(frame, (x, y + h), (x + w, y + h + 30), color, -1)
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv2.putText(frame, name, (x, y + h + 25), 2, 1, (255, 255, 255), 2, cv2.LINE_AA)

            cv2.imshow("Frame", frame)
            k = cv2.waitKey(1)
            if k == 27:  # Presiona "ESC" para salir
                break
        
        cap.release()
        cv2.destroyAllWindows()

        # Devuelve los resultados a la plantilla
        context = {
            'result': result,  # Agrega los resultados del reconocimiento
        }
        return render(request, 'recognition.html', context)



@login_required
def patients_details(request):

    patients = Paciente.objects.all()

    context = {
        'patients': patients
    }

    return render(request, 'pages/detalles_pacientes.html', context)

@login_required
def patients_delete(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)

    if request.method == 'POST':
        try:
            paciente.delete()
            return redirect('pacientes')
        except Exception as e:
            print.error(request, "Ocurrió un error al eliminar paciente")

    return render(request, 'pages/eliminar_paciente.html', {'paciente':paciente})

@login_required
def patients_update(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)

    if request.method == 'POST':
        form = PacienteForm(request.POST,request.FILES, instance=paciente)  # Cambia "request.post" a "request.POST"

        if form.is_valid():
            form.save()
            return redirect('pacientes')
    else:
        form = PacienteForm(instance=paciente)

    return render(request, 'pages/actualizar_paciente.html', {'form': form})