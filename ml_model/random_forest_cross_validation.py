from pyspark.ml import Pipeline
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.feature import IndexToString, StringIndexer, VectorIndexer
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.sql import SQLContext
from pyspark import SparkContext

import sys

sc = SparkContext()
sqlContext = SQLContext(sc)
# load data file.
# inputData = sqlContext.read.format("libsvm").load("/home/host0/Desktop/wf_project/wells_fargo_data_mining/data/test.libsvm")
inputData = sqlContext.read.format("libsvm").load(sys.argv[1])

total_accuracy = 0
for i in range(20):
	labelIndexer = StringIndexer(inputCol="label", outputCol="indexedLabel").fit(inputData)
	# Automatically identify categorical features, and index them.
	# Set maxCategories so features with > 4 distinct values are treated as continuous.
	featureIndexer =\
	    VectorIndexer(inputCol="features", outputCol="indexedFeatures", maxCategories=4).fit(inputData)
	# Split the data into training and test sets (30% held out for testing)
	(trainingData, testData) = inputData.randomSplit([0.7, 0.3])
	# Train a RandomForest model.
	rf = RandomForestClassifier(labelCol="indexedLabel", featuresCol="indexedFeatures", numTrees=10)
	# Convert indexed labels back to original labels.
	labelConverter = IndexToString(inputCol="prediction", outputCol="predictedLabel",
	                               labels=labelIndexer.labels)
	# Chain indexers and forest in a Pipeline
	pipeline = Pipeline(stages=[labelIndexer, featureIndexer, rf, labelConverter])
	# Train model.  This also runs the indexers.
	model = pipeline.fit(trainingData)
	# Make predictions.
	predictions = model.transform(testData)
	# Select example rows to display.
	# predictions.select("predictedLabel", "label", "features").show(5)
	# Select (prediction, true label) and compute test error
	evaluator = MulticlassClassificationEvaluator(
	    labelCol="indexedLabel", predictionCol="prediction", metricName="accuracy")
	accuracy = evaluator.evaluate(predictions)
	print "loop "+str(i)+": accuracy is:"+str(accuracy)
	total_accuracy = total_accuracy + accuracy

print("Test Error = " +str(100*(1.0 - total_accuracy/20))+"%")

