from pyspark.ml import Pipeline
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.feature import IndexToString, StringIndexer, VectorIndexer
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark import SparkContext
import pyspark.sql

import sys

sc = SparkContext()
sqlContext = pyspark.sql.SQLContext(sc)
# load data file.
# inputData = sqlContext.read.format("libsvm").load("/home/host0/Desktop/wf_project/wells_fargo_data_mining/data/test.libsvm")
inputData = sqlContext.read.format("libsvm").load(sys.argv[1])

labelIndexer = StringIndexer(inputCol="label", outputCol="indexedLabel").fit(inputData)
# Automatically identify categorical features, and index them.
# Set maxCategories so features with > 4 distinct values are treated as continuous.
featureIndexer =\
    VectorIndexer(inputCol="features", outputCol="indexedFeatures", maxCategories=4).fit(inputData)

# Train a RandomForest model.
rf = RandomForestClassifier(labelCol="indexedLabel", featuresCol="indexedFeatures", numTrees=10)
# Convert indexed labels back to original labels.
labelConverter = IndexToString(inputCol="prediction", outputCol="predictedLabel",
                               labels=labelIndexer.labels)
# Chain indexers and forest in a Pipeline
pipeline = Pipeline(stages=[labelIndexer, featureIndexer, rf, labelConverter])
# Train model.  This also runs the indexers.
model = pipeline.fit(inputData)
# Make predictions.
saving_list = sys.argv[2].strip().split('+')
saving_list = [float(i) for i in saving_list]
print saving_list
tmp_row = pyspark.sql.Row(features=pyspark.ml.linalg.SparseVector(5,{0: saving_list[0], 1: saving_list[1], 2: saving_list[2], 3: saving_list[3], 4: saving_list[4]}))
new_data = sc.parallelize([tmp_row]).toDF()
predictions = model.transform(new_data)

# print("The user should belong to group: " +str(int(predictions.toPandas()['prediction'].tolist()[0])))
print(str(int(predictions.toPandas()['prediction'].tolist()[0])))

