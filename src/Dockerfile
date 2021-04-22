# Either use pytorch as the base image, install first with "docker pull pytorch/pytorch"
FROM pytorch/pytorch
# OR use any other docker base image like tensorflow - installed with "docker pull tensorflow/tensorflow"
# FROM tensorflow/tensorflow

# Use latest package versions
RUN apt-get update

# Get all required packages for opencv2
RUN apt-get install ffmpeg libsm6 libxext6 -y
RUN pip install opencv-python
# Add other needed packages

# Copy all the folder of the Dockerfile and all its subfolders to the workspace folder and its subfolders in the container
ADD . /workspace/

# Make the code executable
RUN chmod +x /workspace/*.sh
RUN chmod +x /workspace/*.py

# Create input and output directory in container
RUN mkdir /input
RUN mkdir /output