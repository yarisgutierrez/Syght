Create binaries for Linux/Mac/Windows:
Install the pip package pyinstaller.
Then from the project directory run:
pyinstaller --onefile specs.py
This will create a dist/specs binary that can be distributed for the arch with all the libs. One file. 

