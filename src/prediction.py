import os
import cv2
from pathlib import Path

def get_corresponding_path(input_path, input_directory, output_directory):
    """
    Get the corresponding path to an input path by replacing the 
    input-directory-beginning of the input path with the 
    output-directory-beginning

    :param input_path: the directory path in the input directory
    :param input_directory: the input directory
    :param output_directory: the output directory

    :returns: the corresponding output directory path in the output directory
    """
    # make sure the given input path is a directory
    if Path(input_path).is_dir():
        parts = list(Path(input_path).parts)
    else:
        parts = list(Path(input_path).parts[:-1])

    # get the input path parts
    input_parts = list(Path(input_directory).parts)
    
    # get the output path parts
    output_parts = list(Path(output_directory).parts)

    # remove the input path parts
    parts_without_input_parts = [
        part for (index, part) in enumerate(parts)
        if len(input_parts) <= index or input_parts[index] != part
    ]

    # add the output path parts
    output_parts += parts_without_input_parts

    # create the output path
    output_path = output_parts[0]
    for part in output_parts[1:]:
        output_path = os.path.join(output_path, part)

    return output_path


if __name__ == "__main__":

    # The mounted directories in the docker container
    input_directory = "/input"
    output_directory = "/output"

    # Access any other file in the folder of the Dockerfile or its
    # subfolders by using "/workspace/<relative_path_from_dockerfile_folder>"
    # i.e.: model_file = "/workspace/model.pt"

    # To test this example run
    # "docker --gpus all run -v "<absolute_host_input_directory>:/input" -v "<absolute_host_output_directory>:/output \
    # adaptor_challenge /workspace/prediction.sh domain_transformation"
    # example images read
    for dirpath, dirname, filenames in os.walk(input_directory):
        for filename in filenames:
            if filename.endswith(".png"):
                # example read input image
                input_file_path = os.path.join(dirpath, filename)
                input_img = cv2.imread(input_file_path)
                # example operation on image
                inverted_input_img = cv2.bitwise_not(input_img)
                # example get corresponding output path
                output_file_path = os.path.join(get_corresponding_path(dirpath, input_directory, output_directory),
                                                filename)
                # example create the output subfolders if they not exist
                if not os.path.exists(os.path.dirname(output_file_path)):
                    os.makedirs(os.path.dirname(output_file_path))
                # example writing of image
                cv2.imwrite(output_file_path, inverted_input_img)
    print("Prediction of novel views completed. The predicted images can now be found in the host output directory.")
    quit()