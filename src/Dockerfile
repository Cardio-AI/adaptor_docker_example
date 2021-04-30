# Either use pytorch as the base image, installed with "docker pull pytorch/pytorch"
FROM pytorch/pytorch
# Or use any other docker base image like tensorflow - installed with "docker pull tensorflow/tensorflow"
# FROM tensorflow/tensorflow

# keep index up to date
RUN apt-get update

# Install all required packages with "RUN <command>"

# Copy the folder of the Dockerfile and all its subfolders to the workspace folder and its subfolders in the container
ADD . /workspace/
WORKDIR /workspace