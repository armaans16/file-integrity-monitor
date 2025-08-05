
# File Integrity Monitor

**File Integrity Monitor** is a Python application designed to verify the integrity of files by generating and comparing cryptographic hashes. It helps detect file tampering or corruption by maintaining a secure baseline and offering both CLI and GUI modes for interaction.

![App Screenshot Placeholder](https://via.placeholder.com/800x200.png?text=File+Integrity+Monitor)

---

## 🔐 Features at a Glance

<table>
<tr>
<td align="center"><img src="https://via.placeholder.com/250x140.png?text=Hash+Generator" width="250"><br><b>Generate Hashes</b></td>
<td align="center"><img src="https://via.placeholder.com/250x140.png?text=Compare+Integrity" width="250"><br><b>Check File Integrity</b></td>
<td align="center"><img src="https://via.placeholder.com/250x140.png?text=GUI+Interface" width="250"><br><b>User-Friendly GUI</b></td>
</tr>
</table>

---

## 🧩 Versions

### 🔹 GUI Version (Recommended)
- Built using [Flet](https://flet.dev).
- **Full-featured** interface: hash generation, baseline saving/loading, and change detection.
- Intuitive layout for selecting files and visualizing results.

To run:

```bash
python mainGUI.py
```

### 🔸 CLI Version (Limited)
- Basic functionality: hashing and comparison.
- No baseline management or file selection via UI.
- Best used for quick checks or automation scripts.

To run:

```bash
python mainCLI.py
```

---

## 📦 Requirements

- Python 3.10+
- Install dependencies:

```bash
pip install flet
```

---

## 🧪 How It Works

1. **Hashing**: A SHA-256 hash of the file is generated.
2. **Baseline Creation**: Hashes are stored in `baseline.json`.
3. **Integrity Check**: Compares current file hash against baseline.
4. **Result**: Alerts user if file has been modified or is safe.

---

## 📚 Libraries Used

### Built-in Libraries
- `hashlib` – for generating SHA-256 hashes
- `json` – for storing and reading the baseline
- `os`, `sys` – for file operations

### External Libraries
- `flet` – for building the graphical user interface

---

## 📁 Folder Structure

```
file-integrity-monitor/
├── mainCLI.py           # Command-line interface (limited features)
├── mainGUI.py           # GUI interface using Flet (full-featured)
├── baseline.json        # Stores hashes of monitored files
├── test.txt             # Sample file for testing
├── __pycache__/         # Compiled Python files
└── .git/                # Git metadata
```

---

## 📃 License

This project is licensed under the [MIT License](LICENSE).
