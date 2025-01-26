# IFFT v1.0 🚀
An advanced tool designed to remind developers of dependencies between code blocks across multiple files, helping maintain consistency and reducing errors in large-scale projects.

**Brief Summary**: Reminds developers that a set of files should be edited together.
![ifft](https://github.com/thiagosantos0/TCC-UFMG/assets/55515126/efe3052e-ad43-4b7a-a8e7-fe708a9595b9)

---

## ✨ Key Features  
### 1. **Output Viewer** 📄  
A structured table interface showcasing:  
- Modified blocks and their associated files.  
- Links to view detailed changes.  
- Options to download metadata in **JSON** or **CSV** format.  
![output_viewer](https://i.postimg.cc/tRDLZ4RJ/Captura-de-tela-2025-01-20-142536.png)

### 2. **Graph Visualization** 🌐  
An interactive directed graph to visualize relationships between files and dependencies.  
- Hover over nodes to display file names or block labels.  
- Use drag-and-drop to organize nodes for better clarity.  
- Distinct color coding for files and blocks.  
![graph-viewer](https://i.postimg.cc/4NypvstB/Captura-de-tela-2025-01-26-105946.png)

### 3. **Configurable Settings** ⚙️  
User-friendly web-based settings management to:  
- Enable/disable auto mode.  
- Define project root directory and excluded folders.  
- Toggle debug mode and active block visibility.  
- Configure IFFT block extraction and restoration preferences.  
![settings](https://i.postimg.cc/tCrt8DFR/Captura-de-tela-2025-01-26-110447.png)

---

## 🛠️ Installation
Install IFFT using the `requirements.txt` file:
```bash
git clone https://github.com/thiagosantos0/IFFT.git
cd IFFT
python3 -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
```

## 🚀 Usage
Run IFFT manually:
```bash
python3 ifft.py
```

*Please follow the instructions on documentation (https://thiagosantos0.github.io/IFFT/) for guidance on how to use IFFT `automode`*

## 🌟 Planned Enhancements
### GitHub Actions
Integrate IFFT into CI/CD pipelines for seamless dependecy tracking during code pushes.

```yaml
name: IFFT  
on: [push]  
jobs:  
  ifft_check:  
    runs-on: ubuntu-latest  
    steps:  
      - uses: actions/checkout@v4  
      - run: ifft run  
```

**Note:** *Please follow the instructions on [documentation](https://thiagosantos0.github.io/IFFT/) for guidance on how to use IFFT `automode`*

## 📚 Documentation
Detailed documentation is hosted [here](https://thiagosantos0.github.io/IFFT/). It includes:
    - A quick start guide.
    - Techincal details about each feature.
    - Instructions for customization and debugging.


## 🤝 Acknowledgments
This project was developed as part of a term paper for the UFMG Computer Science program.

