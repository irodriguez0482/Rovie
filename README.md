# 🚀 Rovie: Lunar Rover Pathing & Navigation
### **Autonomous Rover for Clearing Rocks from the Lunar Terrain**  
[![GitHub repo](https://img.shields.io/badge/GitHub-Rovie-blue?style=flat&logo=github)](https://github.com/irodriguez0482/Rovie)

## 📌 Project Overview
Rovie is a **surface modification rover** designed for **autonomous navigation and rcoc clearing**.  
This project aims to create a **fully autonomous system** capable of efficiently clearing a **3m x 3m** area from intrusive rock.  

---

## 📁 Repository Structure
```
rover_project/
├── main.py                       # Main entry point (handles mode switching)
├── config/
│   ├── constants.py              # All project-wide constants (distances, thresholds)
│   └── pins.py                   # GPIO pin mappings for Raspberry Pi
│   └── test_scenarios.py         # Testing Scenarios for when mocking hardware testing
│   └── README.md
├── core/                         # Core logic for behavior and modes
│   ├── autonomous.py             # 3x3 path clearing logic
│   ├── obstacle_avoidance.py     # Force button logic and rerouting
│   ├── state_machine.py          # Handles transitions between behaviors
│   └── arm_control_logic.py      # Decision logic for when to move arm
├── hardware/                     # Interfaces for sensors and actuators
│   ├── gps.py                    # GPS interface
│   ├── motors.py                 # Send commands to Arduino
│   ├── arm.py                    # Vibration + up/down arm control
│   ├── force_button.py           # Read obstacle sensor
│   ├── estop.py                  # Emergency stop button logic
│   └── README.md
│   └── mock/                     # Mock versions of above (for testing without hardware)
│       ├── gps.py
│       ├── motors.py
│       └── arm.py
│       └── estop.py
│       └── force_button.py
├── utils/
│   ├── logger.py                 # Logging GPS data, sensor events, errors
│   ├── coordinate_utils.py       # Haversine + coordinate math
│   └── timer.py                  # For timeouts, delays, safety checks
├── logs/                         # All generated logs saved here
│   ├── gps/
│   ├── sensors/
│   ├── flags/
│   └── errors/
│   └── README.md
├── arduino/                      # C++ Arduino code
│   ├── MotorCommunication.ino
│   └── README.md                 # Flashing instructions, serial protocol docs
├── testing/                        # Unit and integration tests
│   ├── test_gps.py               # Runs GPS code in isolation
│   ├── test_force_button.py
│   ├── test_pathing_straight.py # Can run on real hardware or mock
│   └── ...
└── README.md                     # Project overview and setup instructions

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