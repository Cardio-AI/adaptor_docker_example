# adaptor_docker_example

1. The container is build with

```
docker build --tag adaptor_challenge ./src/
```

2. The container is then run with

```
docker run --gpus all -v "<absolute_host_input_directory>:/input" -v "<absolute_host_output_directory>:/output" adaptor_challenge /workspace/prediction.sh /input/<path_to_input_image> /output/<path_to_output_json> landmark_detection
```  

or

```
docker run --gpus all -v "<absolute_host_input_directory>:/input" -v "<absolute_host_output_directory>:/output" adaptor_challenge /workspace/prediction.sh /input/<path_to_input_image> /output/<path_to_output_image> domain_transformation
```  


## This working example can be run with

```
docker run --gpus all -v "<absolute_host_input_directory>:/input" -v "<absolute_host_output_directory>:/output" adaptor_challenge /workspace/prediction.sh /input/example_folder/example_subfolder/AdaptOR.png /output/example_folder/example_subfolder/AdaptOR.json landmark_detection
```  

or

```
docker run --gpus all -v "<absolute_host_input_directory>:/input" -v "<absolute_host_output_directory>:/output" adaptor_challenge /workspace/prediction.sh /input/example_folder/example_subfolder/AdaptOR.png /output/example_folder/example_subfolder/AdaptOR.png domain_transformation
```  