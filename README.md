# HackyAIMod
This repository contains the source code of HackyAIMod.

# Deployment
## Using Docker
1. Download the ![Dockerfile](https://github.com/dkvc/HackyAIMod/blob/main/Dockerfile) from repository.
2. Build the image:
```
docker build -t HackyAI
```
3. Turn off access control for Docker to your X11 server.
```
xhost +local:docker
```
4. If you have Nvidia GPU installed:
```
docker run -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY --security-opt=label=disable --runtime=nvidia -d --name HackyAIMod -i HackyAI
```

> If you don't have Nvidia GPU installed:
> ```
> docker run --security-opt=label=disable -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY -d --name HackyAIMod -i HackyAI
> ```

## Without using Docker [Recommended]
> Recommended Python Version: 3.11.x

1. Clone the git repository.
```
git clone https://github.com/dkvc/HackyAI.git
```

2. Install required dependencies from requirements.txt
```
cd HackyAIMod
pip install -r requirements.txt
```

3. To test the model, use the following command.
```
python test_model.py
```

4. To test the Chat UI, use the following command.
```
python test_ui.py
```