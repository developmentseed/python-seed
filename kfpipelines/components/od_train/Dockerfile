FROM tensorflow/tensorflow:1.15.0-gpu-py3

####################
# Install google utils for accessing GCP per https://cloud.google.com/sdk/docs/quickstart-debian-ubuntu
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg  add - && apt-get update -y && apt-get install google-cloud-sdk -y

# Install wget (to make life easier below) and editors (to allow people to edit
# the files inside the container)
RUN apt-get install -y wget vim nano

####################
# Get the tensorflow models research directory, and move it into tensorflow
# source folder to match recommendation of installation
RUN apt-get update -y && apt-get install git -y
RUN mkdir -p /tensorflow/models
RUN git clone --progress --depth 1 https://github.com/tensorflow/models.git /tensorflow/models

# Install object detection api dependencies
RUN apt-get install -y protobuf-compiler python-pil python-lxml && \
    pip install Cython contextlib2 pillow lxml jupyter matplotlib
#RUN apt-get install python-tk -y

# Install pycocoapi for instance segmentation utils
RUN git clone https://github.com/cocodataset/cocoapi.git && \
	cd cocoapi/PythonAPI && \
	make && \
	cp -r pycocotools /tensorflow/models/research/ && \
	cd ../../ && \
	rm -rf cocoapi

# Run protoc on the object detection repo
RUN cd /tensorflow/models/research && \
    protoc object_detection/protos/*.proto --python_out=.

# Set the PYTHONPATH to finish installing the API
ENV PYTHONPATH $PYTHONPATH:/tensorflow/models/research:/tensorflow/models/research/slim

############################
# Update model export script with minor modifications

# Modify training code to allow us to keep many more checkpoints than the default of 5 
COPY src/model_main.py /tensorflow/models/research/object_detection/model_main.py
COPY src/model_lib.py /tensorflow/models/research/object_detection/model_lib.py

# Modify export code to allow us to export any checkpoint 
COPY src/exporter.py /tensorflow/models/research/object_detection/exporter.py

# Add our custom command-line launcher
COPY src/launch.py /launch.py

####################
WORKDIR /tensorflow