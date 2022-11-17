## MapReduce
## Pandas groupBy
## Spark groupBy
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, collect_list, array_contains
from pyspark.sql.types import StructField, IntegerType, StructType, StringType

spark = SparkSession.builder.getOrCreate()

# sqlContext = SparkSession.builder.enableHiveSupport().getOrCreate()

schema = StructType([
    StructField("translation_index_1", IntegerType(), True),
    StructField("original_text", StringType(), True),
    StructField("translation_index_2", IntegerType(), True),
    StructField("translated_text", StringType(), True)
])

df = spark.read.csv("deu_eng.tsv", header=False, schema=schema, sep="\t").drop(*["translation_index_1", "translation_index_2"])
groupedBy = df.groupby("original_text").agg(collect_list('translated_text'))
groupedBy.printSchema()
groupedBy.filter(groupedBy.original_text == "Was ist das?").show(truncate=False)
groupedBy.toPandas().to_json("./groupedByTranslations", orient='records')
# groupedBy.filter(array_contains("collect_list(translated_text)", "What is that?")).show(truncate=False)
# df.printSchema()
# df.show()
