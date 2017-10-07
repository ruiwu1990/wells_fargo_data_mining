from pyspark.ml.classification import LogisticRegression, OneVsRest
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

# load data file.
inputData = spark.read.format("libsvm") \
	.load("/home/host0/Desktop/wf_project/wells_fargo_data_mining/data/test.libsvm")

total_accuracy = 0
for i in range(20):
	# generate the train/test split.
	(train, test) = inputData.randomSplit([0.7, 0.3])
	# instantiate the base classifier.
	lr = LogisticRegression(maxIter=10, tol=1E-6, fitIntercept=True)
	# instantiate the One Vs Rest Classifier.
	ovr = OneVsRest(classifier=lr)
	# train the multiclass model.
	ovrModel = ovr.fit(train)
	# score the model on test data.
	predictions = ovrModel.transform(test)
	# obtain evaluator.
	evaluator = MulticlassClassificationEvaluator(metricName="accuracy")
	# compute the classification error on test data.
	accuracy = evaluator.evaluate(predictions)
	# print("Test Error = %g" % (1.0 - accuracy))
	total_accuracy = total_accuracy + accuracy

print("Test Error = %g" % (1.0 - total_accuracy/20))


inputData = sqlContext.read.format("libsvm").load("/home/host0/Desktop/wf_project/wells_fargo_data_mining/data/test.libsvm")

# data = spark.read.format("libsvm").load('test.libsvm')

# generate the train/test split.
(train, test) = inputData.randomSplit([0.7, 0.3])
# instantiate the base classifier.
lr = LogisticRegression(maxIter=10, tol=1E-6, fitIntercept=True)
# instantiate the One Vs Rest Classifier.
ovr = OneVsRest(classifier=lr)
# train the multiclass model.
ovrModel = ovr.fit(train)
# score the model on test data.
predictions = ovrModel.transform(test)
# obtain evaluator.
evaluator = MulticlassClassificationEvaluator(metricName="accuracy")
# compute the classification error on test data.
accuracy = evaluator.evaluate(predictions)
# print("Test Error = %g" % (1.0 - accuracy))
total_accuracy = total_accuracy + accuracy
