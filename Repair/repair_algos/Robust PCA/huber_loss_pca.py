import pandas as pd
from sklearn.model_selection import train_test_split
import loss
from m_est_rpca import MRobustPCA
import numpy as np

def df_anomaly_instances(df_class):
    df_class_instances = pd.DataFrame(index=df_class.index)
    df_class_instances['class'] = False

    indexes = []
    for index, row in df_class.iterrows():
        for column in df_class.columns:
            if row[column] == 1:
                indexes.append(index)
                break
    print('Number of anomaly instances: %d', len(indexes))

    for index in indexes:
        df_class_instances.loc[index, 'class'] = True

    return df_class_instances

def get_train_valid_sets(df_train, train_size=0.5, random_seed=10):
    """
    Splits the training dataset into a train and validation set. Use this method for semi supervised techniques
    as those models should be trained with only normal data.
    :param df_train: training data set with normal and anomalous data, should contain a "class" column to indicate anomalies
    :param train_size: the proportion of the dataset to include in the split
    :param random_seed: the seed used by the random number generator
    :return: a train set of normal data, a validation test set of normal and anomalous data
    """
    normal = df_train[df_train['class'] == False]
    anomalous = df_train[df_train['class'] == True]

    train, normal_test, _, _ = train_test_split(normal, normal,
                                                train_size=train_size,
                                                random_state=random_seed)

    normal_valid, _, _, _ = train_test_split(normal_test, normal_test,
                                             train_size=train_size,
                                             random_state=random_seed)

    anomalous_valid, _, _, _ = train_test_split(anomalous, anomalous,
                                                train_size=train_size,
                                                random_state=random_seed)

    valid = normal_valid.append(anomalous_valid).sample(frac=1, random_state=random_seed)

    print('Train shape: %s' % repr(train.shape))
    print('Valid shape: %s' % repr(valid.shape))
    print('Proportion of anomaly in validation set: %.2f\n' % valid['class'].mean())

    return train, valid


"expects a common class for all ts"
def robust_pca_huber_loss(df, df_train ,  delta=1, n_components=2, maximize_score='F1-Score', train_size=0.5, random_seed=10):

    class_truth = df["class"]


    # for supervised detection(!) - stratify parameter makes a split so that the proportion of values in the sample produced will be the same as the proportion of values provided to parameter stratify
    #X_train, X_test, y_train, y_test = train_test_split(df_train, df_train_common_class, train_size=train_size, random_state=random_seed, stratify=df_train_common_class)

    train, valid = get_train_valid_sets(df_train, train_size=train_size, random_seed=random_seed)

    X_train = train.drop('class', axis=1)
    X_test = valid.drop('class', axis=1)

    # Dimensionality reduction with Robust PCA and Huber Loss Function
    huber_loss = loss.HuberLoss(delta=delta)
    M_rpca = MRobustPCA(n_components, huber_loss)

    # Fit R-PCA on Train Set
    M_rpca.fit(X_train)

    # R-PCA on Test Set
    X_test_reduced = M_rpca.transform(X_test)
    X_test_reduced = pd.DataFrame(data=X_test_reduced, index=X_test.index)
    X_test_reconstructed = M_rpca.inverse_transform(X_test_reduced)
    X_test_reconstructed = pd.DataFrame(data=X_test_reconstructed, index=X_test.index)

    # y_test_scores = normalized_anomaly_scores(X_test, X_test_reconstructed)
    # y_test_scores = np.round(y_test_scores, 7)  # round scores

    # computed scores are always in between 0-1 due to min max normalization
    thresholds = np.linspace(0, 1, 200)
    thresholds = np.round(thresholds, 7)  # round thresholds

    # training_threshold_scores = get_threshold_scores(thresholds, y_test_scores, valid['class'], upper_boundary=True) # or replace valid['class'] with y_test for supervised detection
    # selected_index = get_max_score_index_for_score_type(training_threshold_scores, maximize_score)
    # selected_threshold = thresholds[selected_index]

    # Run on Dataset
    X_df_reduced = M_rpca.transform(df)
    X_df_reduced = pd.DataFrame(data=X_df_reduced, index=df.index)
    X_df_reconstructed = M_rpca.inverse_transform(X_df_reduced)
    X_df_reconstructed = pd.DataFrame(data=X_df_reconstructed, index=df.index)

    # detection on dataset
    # scores = normalized_anomaly_scores(df, X_df_reconstructed)
    # scores = np.round(scores, 7)  # round scores

    # y_hat_results = (scores > selected_threshold).astype(int)
    # y_truth = df_common_class.values.astype(int)
    # detection_threshold_scores = get_threshold_scores(thresholds, scores, df_common_class['class'], upper_boundary=True)
    # info = get_detection_meta(selected_threshold, y_hat_results, y_truth, upper_boundary=True)
    #
    # info['thresholds'] = thresholds.tolist()
    # info['training_threshold_scores'] = training_threshold_scores.tolist()
    # info['detection_threshold_scores'] = detection_threshold_scores.tolist()

    return X_df_reconstructed # df_common_class, # info


# def normalized_anomaly_scores(df_original, df_reconstructed):
#     """
#     The reconstruction error is the sum of the squared differences between the original and the reconstructed dataset.
#     The sum of the squared differences is scaled by the max-min range of the sum of the squared differences,
#     so that all reconstruction errors are within a range of 0 to 1 (normalized). In consequence, normal data
#     should have a low score whereas anomalies have higher scores.
#     :param df_original: the original dataset as dataframe
#     :param df_reconstructed: the reconstructed dataset from rpca
#     :return: anomaly scores as series with range 0 to 1
#     """
#
#     diff = np.sum((np.array(df_original) - np.array(df_reconstructed)) ** 2, axis=1)
#     diff = pd.Series(data=diff, index=df_original.index)
#
#     return min_max_normalization(diff)