import os
import json
import argparse
import math
from tqdm import tqdm
from pathlib import Path


def evaluate(predictions, labels, radius):
    """
    Evaluate an array of predictions based on an array of labels and their given radius

    True positive gets calculated by matching predictions with labels from shortest distance to longest distance.
    False positive are all predictions without a label.
    False negative are all label without a prediction.

    :param predictions: an array of predictions with x and y coordinates
    :param labels: an array of labels with x and y coordinates
    :param radius: the radius around the labels within which a prediction is still correct

    :returns: the amount of true positive (TP) (label with prediction), false positive (FP) (prediction with no label) and false negative (FN) (label with no prediction) labels
    """
    # count all labels in radius of each prediction
    labels_in_radius_of_all_predictions = []

    # iterate all predictions
    for prediction_index, prediction in enumerate(predictions):
        labels_in_radius_of_prediction = []

        # for each label
        for label_index, label in enumerate(labels):

            # get the distance to all close labels for each prediction
            distance = abs(math.sqrt(
                (label["x"] - prediction["x"])**2 + (label["y"] - prediction["y"])**2))

            # save all close labels of the prediction
            if distance <= radius:
                labels_in_radius_of_prediction.append(
                    {"prediction_index": prediction_index, "label_index": label_index, "distance": distance})

        labels_in_radius_of_all_predictions.append(
            labels_in_radius_of_prediction)

    # all true positive predictions with labels and distance
    true_positive_predictions = []

    # check if any predictions have close labels
    # find all matching pairs of predictions and labels starting with the closest pair
    while max([len(_) for _ in labels_in_radius_of_all_predictions], default=0) >= 1:

        # the closest pair of any prediction and any label
        closest_prediction_label_pair = None

        # iterate the predictions
        for labels_in_radius_of_prediction in labels_in_radius_of_all_predictions:
            # choose the prediction and label with the shortest distance
            for close_label in labels_in_radius_of_prediction:
                if closest_prediction_label_pair == None or close_label["distance"] <= closest_prediction_label_pair["distance"]:
                    closest_prediction_label_pair = close_label

        # the best prediction is a true positive prediction
        true_positive_predictions.append(closest_prediction_label_pair)

        # make sure this prediction does not get picked again
        labels_in_radius_of_all_predictions[closest_prediction_label_pair["prediction_index"]] = [
        ]

        # make sure this label does not get picked again
        for index, labels_in_radius_of_prediction in enumerate(labels_in_radius_of_all_predictions):
            # remove the label of the best prediction from all other predictions
            labels_in_radius_of_all_predictions[index] = [
                close_label for close_label in labels_in_radius_of_prediction if close_label["label_index"] != closest_prediction_label_pair["label_index"]]

    # the amount of true positives is just the amount of found predictions and labels matches
    true_positive = len(true_positive_predictions)
    # the amount of false positives is the amount of predictions not found in the predictions and labels matches
    false_positive = len([prediction for index, prediction in enumerate(predictions) if len(
        [tp_prediction for tp_prediction in true_positive_predictions if tp_prediction["prediction_index"] == index]) == 0])
    # the amount of false negatives is the amount of labels not found in the predictions and labels matches
    false_negative = len([label for index, label in enumerate(labels) if len(
        [tp_prediction for tp_prediction in true_positive_predictions if tp_prediction["label_index"] == index]) == 0])

    return true_positive, false_positive, false_negative


def find_relative_path_in_directory(directory, relative_path):
    """
    Find the absolute path of a file or folder in a directory
    based on a relative path.

    E.g. find "/aicm1/VID000_0/point_labels/000000.json" by searching through 
    the directory and it's subdirectory for the "aicm1" directory 
    with a "VID000_0" subdirectory which has a "point_labels" subdirectory and 
    return the absolute path of the "000000.json" json file.

    :param directory: the absolute path to a directory
    :param relative_path: the relative path that is supposed to be found in the directory
    :return: the absolute path
    """
    relative_path = Path(relative_path)
    # iterate directories in the directory
    for dirpath, dirnames, filenames in os.walk(directory):
        # check if this subdirectory path joined with the relative path exists, then return it
        path = os.path.join(dirpath, relative_path)
        if Path(path).exists():
            return path
    raise Exception("File {} not found in directory {}".format(
        relative_path, directory))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Evaluate all json files in a directory or subdirectories by comparing them to manually labelled files')
    parser.add_argument('predictions', type=str,
                        help='the absolute path of the directory with the predicted json files')
    parser.add_argument('labels', type=str,
                        help='the absolute path of the directory with the manually labelled json files')

    args = parser.parse_args()
    label_folder_path = args.predictions
    prediction_folder_path = args.labels

    # count the total amount of evaluated files
    amount_files = 0

    # calculate sensitivity/recall (TPR), precision (PPV) and the balanced F-score (F1 score)
    sensitivity = 0
    precision = 0
    f1_score = 0

    # count all true positives, false positives and false negatives for all files for later calculations
    true_positive_all_files = 0
    false_positive_all_files = 0
    false_negative_all_files = 0

    # iterate the json files in the folder
    for dirpath, dirnames, filenames in os.walk(prediction_folder_path):
        # find all json files in the current directory
        json_files = [
            filename for filename in filenames if filename.endswith(".json")]
        # make sure there are json files in this directory
        if len(json_files) > 0:
            # evaluate all json files
            for prediction_filename in tqdm(json_files):
                amount_files += 1

                # read json data
                prediction_file_path = os.path.join(
                    dirpath, prediction_filename)
                prediction_file = open(prediction_file_path, "r")
                prediction_data = json.load(prediction_file)

                try:
                    # get corresponding file in label folder
                    label_file_path = find_relative_path_in_directory(label_folder_path, os.path.join(Path(
                        dirpath).parent.parent.name, Path(dirpath).parent.name, Path(dirpath).name, prediction_filename))
                except Exception as ex:
                    print(ex)
                    continue
                label_file = open(label_file_path, "r")
                label_data = json.load(label_file)

                # calculate TP (label and prediction), FP (prediction but no label) and FN (label but no prediction) from points
                true_positive, false_positive, false_negative = evaluate(
                    prediction_data["points"], label_data["points"], radius=6)

                # count all true positives, false positives and false negatives for all files for later calculations
                true_positive_all_files += true_positive
                false_positive_all_files += false_positive
                false_negative_all_files += false_negative

    # sensitivity (SEN) = TP + P
    sensitivity = true_positive_all_files / \
        (true_positive_all_files + false_negative_all_files)

    # precision (PPV) = TP / PP
    precision = true_positive_all_files / \
        (true_positive_all_files + false_positive_all_files)

    # F1 score = (2 * PPV * SEN) / (PPV + SEN)
    f1_score = (2 * precision * sensitivity) / (precision + sensitivity)

    # output information about the evaluated files and the final scores
    print("Total files:     ", amount_files)
    print("True positive:   ", true_positive_all_files)
    print("False positive:  ", false_positive_all_files)
    print("False negative:  ", false_negative_all_files)
    print("Sensitivity:     ", sensitivity)
    print("Precision:       ", precision)
    print("F1 score:        ", f1_score)
