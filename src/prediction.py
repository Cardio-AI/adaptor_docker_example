import argparse
import os
import json
import cv2
from pathlib import Path

if __name__ == "__main__":

    # Specify command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", required=True, type=str)
    parser.add_argument("--output_file", required=True, type=str)
    parser.add_argument("--task", required=True, type=str, choices=["landmark_detection", "domain_transformation"])

    # Parse and get all arguments
    args = parser.parse_args()

    # The input file path is a file path of an image file in the /input folder or a subfolder
    input_file_path = args.input_file

    # The output file path is a file path of either a json file if the task is landmark_detection
    # or an image file path if the task is domain_transformation in the /output folder or a subfolder
    output_file_path = args.output_file

    # The task specifies whether the goal of this program 
    # should be to detect landmarks or do a domain transformation
    task = args.task

    # Access any other file in the folder of the Dockerfile or its 
    # subfolders by using "/workspace/<relative_path_from_dockerfile_folder>"
    # i.e.: model_file = "/workspace/model.pt"

    if task == "domain_transformation":
        # Optional: TODO Import and call domain transformation code and create an image at the output file path

        # To test this example run 
        # "docker run -v "<absolute_host_input_directory>:/input" -v "<absolute_host_output_directory>:/output" adaptor_challenge /workspace/prediction.sh /input/example_folder/example_subfolder/AdaptOR.png /output/example_folder/example_subfolder/AdaptOR.png domain_transformation"
        # example image read
        input_img = cv2.imread(input_file_path)
        # example operation on image
        inverted_input_img = cv2.bitwise_not(input_img)
        # example create the folders if they not exist
        if not os.path.exists(os.path.dirname(output_file_path)):
            os.makedirs(os.path.dirname(output_file_path))
        # example writing of image
        cv2.imwrite(output_file_path, inverted_input_img)
        quit()

    # Mandatory: TODO Import and call landmark detection code and create a json file at the output file path
    # The json files structure can be found in the synapse wiki
    
    # To test this example run
    # "docker run -v "<absolute_host_input_directory>:/input" -v "<absolute_host_output_directory>:/output" adaptor_challenge /workspace/prediction.sh /input/example_folder/example_subfolder/AdaptOR.png /output/example_folder/example_subfolder/AdaptOR_points.json landmark_detection"

    # example image read
    input_img = cv2.imread(input_file_path)
    # example create json
    labels = {
        "folderName": Path(input_file_path).parent.parent.name,
	    "subfolderName": Path(input_file_path).parent.name,
	    "imageFileName": Path(input_file_path).name,
        "points": [{
            "x": input_img.shape[1],
            "y": input_img.shape[0]
        }]
    }
    # example create the folders if they not exist
    if not os.path.exists(os.path.dirname(output_file_path)):
        os.makedirs(os.path.dirname(output_file_path))
    output_file = open(output_file_path, "w")
    # example write the json file
    json.dump(labels, output_file, indent=4)