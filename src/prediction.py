import argparse
import os

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
    model_file = "/workspace/model.pt"

    if task == "domain_transformation":
        # Optional: TODO Add domain transformation code and create an image at the output file path
        quit()

    # Mandatory: TODO Add landmark detection code and create a json file at the output file path
    # The json file should have a imageFileName string attribute and a "points" array of dictionaries with "x" and "y" number attributes