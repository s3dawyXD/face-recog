
# Face Recognition Project

This is a Python-based face recognition project that uses a locally built `.whl` package (`NetSDK`) and a `.env` file for configuration. It is designed to run on Windows, optionally at system startup.

---

## ✅ Prerequisites

- Windows 10 or later
- Python 3.8+
- pip
- git (optional)
- Administrator privileges (for startup setup)

---

## 📦 Installation

1. **Clone or Download the Project**

   ```bash
   git clone https://github.com/yourusername/face-recog.git
   cd face-recog
   ```

   Or download the ZIP and extract it.

2. **Create Virtual Environment**

   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install Dependencies**

   Update `requirements.txt` to reference the full path to your `.whl` file:

   ```
   NetSDK @ file:///C:/path/to/face-recog/dist/NetSDK-2.0.0.1-py3-none-win_amd64.whl
   ```

   Then run:

   ```bash
   pip install -r requirements.txt
   ```

---

## 🔐 Environment Variables

Create a `.env` file in the root folder with any sensitive settings:

```
CHECK_IN_URL=backend url
IP=Dahua machine IP
PORT=Dahua machine port
USERNAME=Dahua machine username
PASSWORD=Dahua machine password
```

---

## ▶️ Running the Project

Activate the environment and run your main script:

```bash
venv\Scripts\activate
python main.py
```

---

## ⚙️ Run on System Startup (Task Scheduler)

### Step-by-Step:

1. **Open Task Scheduler** (search in Start Menu)

2. **Click "Create Task..."** (not basic task)

3. **General Tab**:
   - Name: `Run Face Recognition`
   - Check: `Run with highest privileges`

4. **Triggers Tab**:
   - Click **New**
   - Begin the task: `At startup`
   - Click OK

5. **Actions Tab**:
   - Click **New**
   - Action: `Start a program`
   - Program/script: `cmd.exe`
   - Add arguments:
     ```
     /c "C:\Users\HP\Downloads\face-recog\run_project.bat"
     ```
   - Click OK

6. **Conditions/Settings Tab**:
   - (Optional) Disable "Start task only if computer is on AC power"

7. **Save** and you're done!

---

## 🛠️ `run_project.bat` (example)

Create this file in the project root:

```bat
@echo off
cd /d C:\Users\HP\Downloads\face-recog
call venv\Scripts\activate.bat
python main.py
```

---

## 📁 Project Structure

```
face-recog/
├── .env
├── main.py
├── venv/
├── dist/
│   └── NetSDK-2.0.0.1-py3-none-win_amd64.whl
├── requirements.txt
└── run_project.bat
```

---