# AdaptOR2021 MICCAI Challenge Docker Example

A docker example repository to support participants in creating submissions for
the [AdaptOR2021 MICCAI Challenge](https://www.synapse.org/AdaptOR_Challenge_2021_MICCAI).

## Setup

1. The container can be built with

```
docker build --tag adaptor_challenge ./src/
```

2. The container can be run with
```
docker run --gpus all -v "<absolute_host_input_directory>:/input" -v "<absolute_host_output_directory>:/output" adaptor_challenge /workspace/prediction.sh landmark_detection
```  

or

```
docker run --gpus all -v "<absolute_host_input_directory>:/input" -v "<absolute_host_output_directory>:/output" adaptor_challenge /workspace/prediction.sh domain_transformation
```
