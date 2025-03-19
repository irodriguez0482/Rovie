# 🚀 Rovie: Lunar Rover Pathing & Navigation
### **Autonomous Rover for Clearing Rocks from the Lunar Terrain**  
[![GitHub repo](https://img.shields.io/badge/GitHub-Rovie-blue?style=flat&logo=github)](https://github.com/irodriguez0482/Rovie)

## 📌 Project Overview
Rovie is a **surface modification rover** designed for **autonomous navigation and rcoc clearing**.  
This project aims to create a **fully autonomous system** capable of efficiently clearing a **3m x 3m** area from intrusive rock.  

---

## 📁 Repository Structure
```
/rover-project
├── /configs
│   ├── README.md
├── /deployment
│   ├── README.md
├── /docs
│   ├── README.md
├── /hardware
│   ├── README.md
│   ├── MotorCommunication.ino
│   ├── Capstone Motor Wiring and Test Code Zip
├── /logs
│   ├── README.md
│   ├── /navigation-logs
├── /software
│   ├── /e-stop
│   ├── /motors
│   ├── /pathing
│   ├── /sensors
│   ├── README.md
├── /testing
│   ├── README.md
├── .gitignore           # Ignored files
├── requirements.txt     # Python dependencies
├── README.md
└── LICENSE              # License information
```

---

## 🛠 Features
- ✅ **Autonomous Pathing** – Uses GPS & IMU for navigation  
- ✅ **Obstacle Avoidance** – Detects large rocks & reroutes  
- ✅ **Motor Control** – Smooth movement and turning logic  
- ✅ **Plow System** – Vibrating motors to clear regolith  
- ✅ **Force Sensor Integration** – Adjusts movement based on resistance  

---

## 📦 Getting Started

### 🔧 Prerequisites
- Raspberry Pi (or another microcontroller)
- Arduino (for motor control)
- GPS Module (e.g., u-blox NEO-6M)
- IMU Sensor (e.g., MPU6050)
- Motor drivers
- Python 3.x installed

### 📥 Installation

1️⃣ **Clone the Repository**  
```bash
git clone git@github.com:irodriguez0482/Rovie.git
cd Rovie
```
2️⃣ **Install Dependencies**  
```bash
pip install -r requirements.txt
```
3️⃣ **Run the Rover Control Script**  
```bash
python main.py
```

---

## ⚡ Hardware & Sensor Setup

| Component  | Purpose |
|------------|---------|
| **Raspberry Pi**  | Controls pathing & sensors |
| **Arduino**  | Motor control |
| **GPS Module**  | Provides location data |
| **IMU Sensor**  | Detects tilt and movement |
| **Force Sensor** | Adjusts plowing force |

---

## 🔬 Testing & Debugging
- **Run unit tests**:  

- **View system logs**:  
  ```bash
  tail -f logs/system.log
  ```
- **Simulate pathing in a virtual environment**:  


---

## 🛠 Contributing

Want to help? Here’s how:

1. **Fork the repo**  
2. **Create a feature branch**:  
   ```bash
   git checkout -b feature/new-pathing
   ```
3. **Commit changes**:  
   ```bash
   git commit -m "Added new obstacle detection logic"
   ```
4. **Push to GitHub**:  
   ```bash
   git push origin feature/new-pathing
   ```
5. **Create a pull request** 🎉  

---

## 📅 Project Tasks & Issues
🚀 **Want to see what’s next?** Check out our [GitHub Issues](https://github.com/irodriguez0482/Rovie/issues) for ongoing tasks.

---

## 📜 License
This project is licensed under the

---

## 👥 Team Members
| Name | Role |
|------|------|
| **Eva Rodriguez** | Integration Specialist |
| **Cate Holt** | Hardware Specialist |
| **Alex Go** | Software Developer |

---

## 🔗 Useful Resources
- 📖 **[Project Docs](docs/README.md)**
- 🛠 **[Hardware Setup Guide](docs/hardware.md)**
- 🚀 **[Software Overview](docs/software.md)**

---

## 📌 Next Steps
- [ ] **Finish motor control integration**
- [ ] **Refine pathing algorithm**
- [ ] **Test force sensor integration**
- [ ] **Improve WiFi/GPS stability**

---
