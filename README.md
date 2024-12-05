```markdown
# 💵 MoneySense Backend

A Flask-based backend for **MoneySense**, a banknote recognition system that predicts the **authenticity** and **denomination** of Indonesian banknotes using machine learning.  

---

## 🗂️ Project Structure

- **Backend**: Flask app for handling API endpoints and serving the model.
- **Model**: TensorFlow/Keras model (`MoneyDetector.h5`) for banknote classification.
- **Database**: Google Firestore for storing prediction history.
- **Configuration**: Google service account stored in `/config/service-account.json`.

---

## 📋 Prerequisites

1. **Install dependencies**:
   ```bash
   pip install flask tensorflow pillow numpy google-cloud-firestore
   ```

2. **Set up Firestore**:
   - Enable **Firestore** in your Google Cloud project.
   - Create a collection named `predictions`.

3. **Service Account**:
   - Grant **Datastore Admin** permissions to your service account.
   - Save the service account JSON key as `config/service-account.json`.

4. **Set Environment Variable**:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS=config/service-account.json
   ```

5. **Prepare the Model**:
   - Place the trained TensorFlow model file (`MoneyDetector.h5`) in the root directory.

---

## 🚀 How to Run

1. Ensure all prerequisites are completed.
2. Start the server:
   ```bash
   python app.py
   ```
3. Access the server at `http://<your-server-ip>:8000`.

---

## 📡 API Endpoints

### 1. 🧾 Predict Currency Authenticity and Denomination  
**Endpoint**: `POST /predict`  

- **Headers**:  
  - `apikey`: Your valid API key (e.g., `12345`).  

- **Body** (multipart/form-data):  
  - `input`: Image file of the banknote (e.g., JPEG, PNG).  
  - `userId`: Unique user identifier.  

- **Response**:  
   Success:
   ```json
   {
     "status": "success",
     "data": {
       "id": "prediction_id",
       "userId": "user_id",
       "currency": "Rp50.000",
       "authenticity": "Asli",
       "authenticity_confidence": 0.97,
       "nominal_confidence": 0.95,
       "createdAt": "timestamp"
     }
   }
   ```  
   Failure (e.g., missing API key or image):  
   ```json
   {
     "status": "fail",
     "message": "Error description."
   }
   ```

---

### 2. 📜 Get Prediction History  
**Endpoint**: `GET /history`  

- **Headers**:  
  - `apikey`: Your valid API key (e.g., `12345`).  

- **Query Parameters**:  
  - `userId`: Unique user identifier.  

- **Response**:  
   Success:
   ```json
   {
     "status": "success",
     "data": [
       {
         "id": "prediction_id",
         "userId": "user_id",
         "currency": "Rp50.000",
         "authenticity": "Asli",
         "nominal_confidence": 0.95,
         "authenticity_confidence": 0.97,
         "createdAt": "timestamp"
       },
       ...
     ]
   }
   ```  
   Failure (e.g., missing userId):  
   ```json
   {
     "status": "fail",
     "message": "userId is required."
   }
   ```

---

### 3. 🏠 Home Endpoint  
**Endpoint**: `GET /` or `GET /index`  

- **Response**:  
   ```json
   {
     "message": "Aplikasi deteksi uang berjalan.."
   }
   ```

---

## 📂 Folder Structure  

- `/config`: Contains the Google Cloud service account file (`service-account.json`).  

---

## 🌐 Additional Information  

- **Database**:  
  - **Firestore** collection: `predictions`.  
  - Stores details like user ID, currency, authenticity, confidence scores, and timestamps.  

- **Permissions**:  
  - The service account requires **Datastore Admin** permissions for Firestore operations.  

- **API Documentation**:  
  Full API documentation is available on [Postman Documentation](#).  

---

## ✨ Features  

1. **Currency Detection**:  
   - Recognizes the authenticity (`Asli` or `Palsu`) and denomination (e.g., `Rp50.000`) of uploaded banknotes.  

2. **Prediction Storage**:  
   - Saves prediction history for each user in Firestore, including metadata like confidence scores and timestamps.  

3. **Secure Access**:  
   - API access is protected using an API key.  

---  

For more questions or issues, feel free to reach out to the team! 📧
