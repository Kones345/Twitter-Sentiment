import csv
import TweetHandler
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from nltk.corpus import stopwords


# Class for performing linear regression
class RegressionModel:
    training_values = []
    training_outputs = []
    test_values = []
    test_outputs = []
    tweetCorpus = []

    REPLACE_NO_SPACE = re.compile(r"(\.)|(\;)|(\:)|(\!)|(\')|(\?)|(\,)|(\")|(\()|(\))|(\[)|(\])")

    classifier = None
    cv = None
    stop_words = set(stopwords.words('english'))

    # Cleans tweets
    def preprocess_data(self, data):
        data = [re.sub(
            r"(\.)|(\;)|(\:)|(\!)|(\')|(\?)|(\,)|(\")|(\()|(\))|(\[)|(\])|@(\w){1,15}|(<br\s*/><br\s*/>)|(\-)|(\/)"
            , "", line.lower()) for line in data]

        return data

    # Constructor to read tweets from csv file and train linear regression model
    def __init__(self):
        print('Text classifier created')
        with open('/home/ubuntu/Twitter-Sentiment/testout.csv', encoding='utf-8', errors='ignore') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                self.tweetCorpus.append(row[1])

        self.training_values = self.tweetCorpus[:35000]
        self.training_values.extend(self.tweetCorpus[50000:85000])

        self.test_values = self.tweetCorpus[35000:50000]
        self.test_values.extend(self.tweetCorpus[85000:100000])

        print("Processing starting")
        self.training_values = self.preprocess_data(self.training_values)
        print("Processing training data done")
        self.test_values = self.preprocess_data(self.test_values)
        print("Processing test values done")

        self.training_outputs = [0 if i < 35000 else 1 for i in range(70000)]
        self.test_outputs = [0 if i < 15000 else 1 for i in range(30000)]

        self.cv = CountVectorizer(binary=True)
        self.cv.fit(self.training_values)
        X = self.cv.transform(self.training_values)
        X_test = self.cv.transform(self.test_values)

        X_train, X_val, y_train, y_val = train_test_split(
            X, self.training_outputs, train_size=0.80
        )

        final_model = LogisticRegression(C=0.25)
        final_model.fit(X, self.training_outputs)
        self.classifier = final_model
        print("Final Accuracy: %s"
              % accuracy_score(self.test_outputs, final_model.predict(X_test)))

    # Predicts whether a tweet is positive or negative
    def classify_text(self, text):
        t = TweetHandler.clean_tweet(text)
        t = self.preprocess_data([t])
        text_matrix = self.cv.transform(t)
        result = self.classifier.predict(text_matrix)

        return result[0].item()


if __name__ == "__main__":
    l = RegressionModel()
    l.classify_text("I love you so much, you make me happy")
    l.classify_text("Jeremy corbyn is a crappy politician")
