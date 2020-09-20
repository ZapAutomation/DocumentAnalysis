# ZappyAI Contract Analysis

A Linux machine with a decent GPU is required. Make sure the latest NVIDIA CUDA GPU drivers are installed on it (https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html)

Follow the steps below to get the site running on a virtual machine:

1. Install Python 3.7+ if not installed (https://www.python.org/downloads/).

2. Make sure pip is installed on the system (https://pip.pypa.io/en/stable/installing/).

3. Install virtualenv and create a virtual environment for the installation- run command: "pip install virtualenv" for installation (without quotes) on the system terminal. Then, create a virtual environment, which can be named "venv" (https://docs.python.org/3/library/venv.html#creating-virtual-environments). Activate the virtual environment- run command: source <VIRT_ENV_NAME>/bin/activate (replace <VIRT_ENV_NAME> with the name of your virtual environment). (Recommended)

4. Clone this repository in a convenient folder (https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository).

5. Change working directory to inside the cloned repository folder – run command: cd nlpDocumentAnalysis

6. Grant execute permissions to the bash scripts – run command: sudo chmod +x *.sh

7. Run the setup – run command: sudo bash setup.sh
   This may take a while.

8. Run the main.py file to serve the website — run command: sudo nohup python main.py

9. Open the site on a browser using the system's external IP address. Follow the documentation (https://drive.google.com/file/d/1VwVW-CQfKW9Me-xgVKN1q6skkUrUYO3a/view?usp=sharing) for instructions on using it.
