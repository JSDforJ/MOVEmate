.\.venv\Scripts\pyinstaller.exe main.py --hidden-import mediapipe.tasks.c

mkdir dist/main/_internal/mediapipe/tasks/c

copy libmediapipe.dll dist/main/_internal/mediapipe/tasks/c/