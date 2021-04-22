# adaptor_docker_example

1. The container is build with

	```docker build --tag adaptor_challenge .```
2. The container is then run with

	```docker run -v "<input_folder>:/input" -v "<output_folder>:/output" adaptor_challenge /workspace/prediction.sh /input/<path_to_input_image> /output/<path_to_output_json> landmark_detection```  
or

	```docker run -v "<input_folder>:/input" -v "<output_folder>:/output" adaptor_challenge /workspace/prediction.sh /input/<path_to_input_image> /output/<path_to_output_image> domain_transformation```  