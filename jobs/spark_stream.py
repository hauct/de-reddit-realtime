import openai
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

spark_conn = SparkSession.builder.appName("SocketStreamConsumer").getOrCreate()

def start_streaming(spark):
    try:
        stream_df = (spark.readStream.format("socket")
                .option("host", "localhost")
                .option("port", 9999)
                .load()
                )

        schema = StructType([
            StructField("review_id", StringType()),
            StructField("user_id", StringType()),
            StructField("business_id", StringType()),
            StructField("stars", FloatType()),
            StructField("date", StringType()),
            StructField("text", StringType())
        ])

        stream_df = stream_df.select(from_json(col('value'), schema).alias("data")).select(("data.*"))

        query = stream_df.writeStream.outputMode("append").format("console").start()
        query.awaitTermination()
        # sentiment_analysis_udf = udf(sentiment_analysis, StringType())

        # stream_df = stream_df.withColumn('feedback',
        #                                     when(col('text').isNotNull(), sentiment_analysis_udf(col('text')))
        #                                     .otherwise(None)
        #                                     )
    except Exception as e:
        print(e)
        
if __name__ == '__main__':
    spark_conn = SparkSession.builder.appName("SocketStreamConsumer").getOrCreate()
    start_streaming(spark_conn)