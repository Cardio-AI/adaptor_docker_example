import argparse
import os
import json
import cv2
from pathlib import Path
from array import array

def get_corresponding_path(input_path, input_directory, output_directory):
    """
    Get the corresponding path to an input path by replacing the 
    input-directory-beginning of the input path with the 
    output-directory-beginning

    :param input_path: the path in the input directory
    :param input_directory: the input directory
    :param output_directory: the output directory

    :returns: the corresponding output path in the output directory
    """
    parts = list(Path(input_path).parts)
    input_parts = list(Path(input_directory).parts)
    output_parts = list(Path(output_directory).parts)
    parts_without_input_parts = [part for (index, part) in enumerate(parts) if len(input_parts) <= index or input_parts[index] != part]
    output_parts += parts_without_input_parts
    output_path = output_parts[0]
    for part in output_parts[1:]:
        output_path = os.path.join(output_path, part)
    return output_path

if __name__ == "__main__":

    # Specify command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", required=True, type=str,
                        choices=["landmark_detection", "domain_transformation"])

    # Parse and get all arguments
    args = parser.parse_args()

    # The mounted directories in the docker container
    input_directory = "/input"
    output_directory = "/output"

    # The task specifies whether the goal of this program
    # should be to detect landmarks or do a domain transformation
    task = args.task

    # Access any other file in the folder of the Dockerfile or its
    # subfolders by using "/workspace/<relative_path_from_dockerfile_folder>"
    # i.e.: model_file = "/workspace/model.pt"

    if task == "domain_transformation":
        # Optional: TODO Import and call domain transformation code and create images in the output directory

        # To test this example run
        # "docker --gpus all run -v "<absolute_host_input_directory>:/input" -v "<absolute_host_output_directory>:/output" adaptor_challenge /workspace/prediction.sh domain_transformation"
        # example images read
        for dirpath, dirname, filenames in os.walk(input_directory):
            for filename in filenames:
                if ".png" in filename:
                # example read input image
                    input_file_path = os.path.join(dirpath, filename)
                    input_img = cv2.imread(input_file_path)
                    # example operation on image
                    inverted_input_img = cv2.bitwise_not(input_img)
                    # example get corresponding output path
                    output_file_path = os.path.join(get_corresponding_path(input_file_path, input_directory, output_directory), filename)
                    # example create the output subfolders if they not exist
                    if not os.path.exists(os.path.dirname(output_file_path)):
                        os.makedirs(os.path.dirname(output_file_path))
                    # example writing of image
                    cv2.imwrite(output_file_path, inverted_input_img)
        quit()

    # Mandatory: TODO Import and call landmark detection code and create a json file at the output file path
    # The json files structure can be found in the synapse wiki

    # To test this example run
    # "docker --gpus all run -v "<absolute_host_input_directory>:/input" -v "<absolute_host_output_directory>:/output" adaptor_challenge /workspace/prediction.sh landmark_detection"

    # example images read
    for dirpath, dirname, filenames in os.walk(input_directory):
        for filename in filenames:
            if ".png" in filename:
                # example read input image
                input_file_path = os.path.join(dirpath, filename)
                input_img = cv2.imread(input_file_path)
                # example create json from image
                labels = {
                    "folderName": Path(input_file_path).parent.parent.name,
                    "subfolderName": Path(input_file_path).parent.name,
                    "imageFileName": Path(input_file_path).name,
                    "points": [{
                        "x": input_img.shape[1],
                        "y": input_img.shape[0]
                    }]
                }
                # example get corresponding output path
                output_file_path = os.path.join(get_corresponding_path(input_file_path, input_directory, output_directory), Path(filename).stem + ".json")
                # example create the output subfolders if they not exist
                if not os.path.exists(os.path.dirname(output_file_path)):
                    os.makedirs(os.path.dirname(output_file_path))
                # example write the json file
                output_file = open(output_file_path, "w")
                json.dump(labels, output_file, indent=4)