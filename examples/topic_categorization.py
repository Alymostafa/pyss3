# coding: utf-8
"""
Topic Categorization Tutorial Source Code (Classic Workflow).

(https://pyss3.readthedocs.io/en/latest/tutorials/topic-categorization.html#topic_classic-workflow)
---
"""

# Before we begin, let's import needed modules...
from pyss3 import SS3
from pyss3.util import Dataset
from pyss3.server import Live_Test

from sklearn.metrics import accuracy_score
from os import system

# ... and unzip the "movie_review.zip" dataset inside the `datasets` folder.
system('unzip -u datasets/topic.zip -d datasets/')

# Ok, now we are ready to begin. Let's create a new SS3 instance
clf = SS3()


# What are the default hyperparameter values? let's see
s, l, p, _ = clf.get_hyperparameters()

print("Smoothness(s):", s)
print("Significance(l):", l)
print("Sanction(p):", p)


# Ok, now let's load the training and the test set using the `load_from_files` function
# from `pyss3.util`. Since, in this dataset, there's a single file for each category,
# we will use the argument ``folder_label=False`` to tell PySS3 to use each file as a different
# category and each line inside of it as a different document:
x_train, y_train = Dataset.load_from_files("datasets/topic/train", folder_label=False)
x_test, y_test = Dataset.load_from_files("datasets/topic/test", folder_label=False)


# Let's train our model...
clf.fit(x_train, y_train)


# Note that we don't have to create any document-term matrix! we are using just the
# plain `x_train` documents :D cool uh? (SS3 creates a language model for each category
# and therefore it doesn't need to create any document-term matrices)
#
# Now that the model has been trained, let's test it using the documents in `x_test`
y_pred = clf.predict(x_test)


# Let's see how good our model performed
print("Accuracy:", accuracy_score(y_pred, y_test))


# Not bad using the default hyperparameters values... let's manually analyze
# what this model has actually learned by using the interactive "live test".
# Note that since we are not going to use the `x_test` for this live test(*) but instead
# the documents in "datasets/topic/live_test", we must use the `set_testset_from_files`
# method to tell the server to load documents from there instead.
#
# (*) try it if you want but since `x_test` contains (preprocessed) tweets,
# they don't look really good and clean.
#
# Live_Test.run(clf, x_test, y_test)  # <- this visualization doesn't look really clean and good so,
#                                     #     instead, we will use the documents in "live_test" folder:

Live_Test.set_testset_from_files("datasets/topic/live_test")

Live_Test.run(clf)

# Live test doesn't look bad, however, we will create a "more intelligent" version of this model,
# a version that can recognize variable-length word n-grams "on the fly". Thus, when calling the
# `fit` we will pass an extra argument `n_grams=3` to indicate we want SS3 to learn to recognize
# important words, bigrams, and 3-grams(*). Additionally, we will name our model
# "topic_categorization_3grams" so that we can save it and load it later from the
# `PySS3 Command Line` to perform the hyperparameter optimization to find better
# hyperparameters values.
#
# (*) If you're curious and want to know how this is actually done by SS3,
#     read the paper "t-SS3: a text classifier with dynamic n-grams for early risk detection over
#     text streams" (preprint available [here](https://arxiv.org/abs/1911.06147)).
clf = SS3(name="topic_categorization_3grams")

clf.fit(x_train, y_train, n_grams=3)  # <-- note the n_grams=3 argument here


# As mentioned above, we will save this trained model for later use
clf.save_model()


# Now let's see if the performance has improved...
y_pred = clf.predict(x_test)
print("Accuracy:", accuracy_score(y_pred, y_test))


# Yeah, the accuracy slightly improved but more importantly, we should now see that the model
# has learned "more intelligent patterns" involving sequences of words when using the
# interactive "live test" to observe what our model has learned (like "machine learning",
# "artificial intelligence", "self-driving cars", etc. for the "science&technology" category.
# Let's see...
Live_Test.run(clf)

# Fortunately, our model has learned to recognize these important sequences (such as
# "artificial intelligence" and "machine learning" in doc_2.txt,  "self-driving cars"
# in doc_6.txt, etc.). However, some documents aren’t perfectly classified, for instance,
# doc_3.txt was classified as “science&technology” (as a third topic) which is clearly wrong...
#
# So, one last thing we are going to do is to try yo find better hyperparameter values to improve
# our model's performance. To achieve this, we will perform what its known as
# "Hyperparameter Optimization" using the ``PySS3 Command Line`` tool.

# * At this point you should read the "Hyperparameter Optimization" section of this tutorial.
# (https://pyss3.readthedocs.io/en/latest/tutorials/topic-categorization.html.html#topic_hyperparameter-optimization)
#
# As described in the "Hyperparameter Optimization" section, we found out that the following
# hyperparameter values will improve our classification performance
clf.set_hyperparameters(s=0.32, l=1.24, p=1.1)


# Let's see if it's true...
y_pred = clf.predict(x_test)
print("Accuracy:", accuracy_score(y_pred, y_test))


# The accuracy has improved as expected :)
#
# Let's perform the last check and visualize what our final model has
# learned and how it is classifying the documents...
Live_Test.run(clf)


# Perfect! now the documents are classified properly! (including *doc_3.txt*) :D
#
# ...and that's it, nicely done buddy!
