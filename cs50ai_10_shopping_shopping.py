import csv
import sys
import calendar

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    # raise NotImplementedError
    calMonths = {calMonth: calIndex-1 for calIndex, calMonth in enumerate(calendar.month_abbr) if calIndex}
    calMonths['June'] = calMonths.pop('Jun')

    proof = []
    titles = []

    with open(filename, 'r') as file:
        calRead = csv.DictReader(file)
        for calRow in calRead:
            proof.append([
                int(calRow['Administrative']),
                float(calRow['Administrative_Duration']),
                int(calRow['Informational']),
                float(calRow['Informational_Duration']),
                int(calRow['ProductRelated']),
                float(calRow['ProductRelated_Duration']),
                float(calRow['BounceRates']),
                float(calRow['ExitRates']),
                float(calRow['PageValues']),
                float(calRow['SpecialDay']),
                calMonths[calRow['Month']],
                int(calRow['OperatingSystems']),
                int(calRow['Browser']),
                int(calRow['Region']),
                int(calRow['TrafficType']),
                1 if calRow['VisitorType'] == 'Returning_Visitor' else 0,
                1 if calRow['Weekend'] == 'TRUE' else 0
            ])
            titles.append(1 if calRow['Revenue'] == 'TRUE' else 0)

    return (proof, titles)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    # raise NotImplementedError
    return KNeighborsClassifier(n_neighbors=1).fit(evidence, labels)

def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    # raise NotImplementedError
    tNeg, fPos, fNeg, tPos = confusion_matrix(labels, predictions).ravel()
    calSens = tPos / (tPos + fNeg)
    calSpec = tNeg / (tNeg + fPos)

    return (calSens, calSpec)


if __name__ == "__main__":
    main()
