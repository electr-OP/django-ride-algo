# **🚗 Ride-Sharing Backend – Microservices with Django**  

## **📌 Overview**  
This project is a backend implementation for a ride-sharing algo. It provides APIs for:  
- **Ride Management** (Passenger Booking, Driver Ride Offering, Real-time Ride Tracking)  
- **Navigation & Routing** (Optimized Routes, Live Location Updates with WebSockets)  

---

## **⚙️ Tech Stack**  
- **Backend:** Python (Django REST Framework, FastAPI)  
- **Database:** PostgreSQL with PostGIS for geospatial data  
- **Caching & Task Scheduling:** Redis  
- **Realtime Communication:** WebSockets (Django Channels)  
- **Infrastructure:** AWS EKS (Kubernetes), Docker 
- **APIs:** Google Maps API,  

---

## **🚀 Features**  
### **1️⃣ Ride Matching Algorithm**  
- Matches passengers with the most suitable drivers  
- Factors considered:  
  - Distance, ETA, Traffic Conditions  
  - Passenger Preferences (Music, Smoking, Pets)  
  - Driver Ratings & Availability  
- Uses a **weighted scoring system** for fairness  

### **2️⃣ Ride Navigation Algorithm**  
- Finds the **optimal route** for a ride  
- Fetches **real-time traffic data** (Google Maps API)  
- Updates **live locations** using WebSockets  

---

## **🛠️ Setup & Installation**  
### **1️⃣ Clone the Repository**  
```bash  
git clone https://github.com/your-username/django-ride-algo.git  
cd ride-sharing-backend  
```

### **2️⃣ Create & Activate Virtual Environment**  
```bash  
python -m venv venv  
source venv/bin/activate   # On macOS/Linux  
venv\Scripts\activate      # On Windows  
```

### **3️⃣ Install Dependencies**  
```bash  
pip install -r requirements.txt  
```

### **4️⃣ Set Up Database & Migrations**  
```bash  
docker-compose up -d  # Start PostgreSQL & Redis  
python manage.py migrate  
```

### **5️⃣ Run the Server**  
```bash  
python manage.py runserver  
```

---

## **🛠️ Dockerized Deployment**  
```bash  
docker-compose up --build -d  
```

---

## **📡 WebSocket Live Ride Tracking**  
```javascript  
const socket = new WebSocket("wss://yourdomain.com/ws/ride-tracking/");  
socket.onmessage = (event) => console.log("Live update:", event.data);  
```

---

## **📌 API Documentation**  
Swagger Docs: `http://localhost:8060/docs/`  
ReDoc: `http://localhost:8000/redoc/`

---

## **📄 License**  
MIT License  
