## MapReduce
## Pandas groupBy
## Spark groupBy
from pyspark.shell import sc
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, collect_list, array_contains
from pyspark.sql.types import StructField, IntegerType, StructType, StringType
import uuid
from pyspark.sql.functions import udf, lit
import boto3
spark = SparkSession.builder.getOrCreate()
sc.setLogLevel("WARN")
schema = StructType([
    StructField("translation_index_1", IntegerType(), True),
    StructField("original_text", StringType(), True),
    StructField("translation_index_2", IntegerType(), True),
    StructField("translated_text", StringType(), True)
])

df = spark.read.csv("deu_eng.tsv", header=False, schema=schema, sep="\t").drop(*["translation_index_1", "translation_index_2"])
groupedBy = df.groupby("original_text").agg(collect_list('translated_text'))
groupedBy = groupedBy.withColumnRenamed("collect_list(translated_text)", "eng_translation")
uuidUdf = udf(lambda: str(uuid.uuid4()), StringType())
# groupedBy = groupedBy.withColumn("id", uuidUdf())
groupedBy = groupedBy.withColumns({"id": uuidUdf(), "language": lit("deu-eng")})
# groupedBy = groupedBy.withColumn("language", lit("deu-eng"))
groupedBy.printSchema()
groupedBy.filter(groupedBy.original_text == "Was ist das?").show(truncate=False)
groupedBy.toPandas().to_json("./groupedByTranslations.json", orient='records')
# groupedBy.filter(array_contains("collect_list(translated_text)", "What is that?")).show(truncate=False)
# df.printSchema()
# df.show()

# primary key, secondary key