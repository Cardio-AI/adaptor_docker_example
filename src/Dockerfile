# This Dockerfile can be individually configured as seen in https://docs.docker.com/engine/reference/builder/
# all neccessary functionalities of the image and container generated with this file can be found in the synapse wiki

# Either use a base image like pytorch "FROM pytorch/pytorch" (installed with "docker pull pytorch/pytorch") 
# or tensorflow "FROM tensorflow/tensorflow" (installed with "docker pull tensorflow/tensorflow")
# or use miniconda3 and install the used ML-Framework as a dependency
FROM continuumio/miniconda3

# keep index up to date
RUN apt-get update

# copy requirements files to container
# pip_requirements.txt can be generated with "pip freeze >> pip_requirements.txt"
COPY pip_requirements.txt /workspace/pip_requirements.txt
# conda_requirements.txt can be generated with "conda list -e >> conda_requirements.txt"
# remove this line if conda is not used
COPY conda_requirements.txt /workspace/conda_requirements.txt

# install the requirements
RUN pip install -r /workspace/pip_requirements.txt
# remove this line if conda is not used
RUN conda install -n base --file /workspace/conda_requirements.txt

# install additional requirements
# remove this line if openCV2 is not used
RUN apt-get install ffmpeg libsm6 libxext6 -y

# copy the folder of the Dockerfile and all its subfolders to the workspace folder and its subfolders in the container
ADD . /workspace/
RUN chmod +x /workspace/prediction.sh
