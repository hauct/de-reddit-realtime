# import openai
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from config import config

# Function to perform sentiment analysis on a comment
# def sentiment_analysis(comment) -> str:
#     if comment:
#         # Set the OpenAI API key
#         openai.api_key = config['openai']['api_key']
#         # Create a chat completion with the GPT-3.5-turbo model
#         completion = openai.ChatCompletion.create(
#             model='gpt-3.5-turbo',
#             messages = [
#                 {
#                     "role": "system",
#                     "content": """
#                         You're a machine learning model with a task of classifying comments into POSITIVE, NEGATIVE, NEUTRAL.
#                         You are to respond with one word from the option specified above, do not add anything else.
#                         Here is the comment:
                        
#                         {comment}
#                     """.format(comment=comment)
#                 }
#             ]
#         )
#         # Return the content of the first choice
#         return completion.choices[0].message['content']
#     return "Empty"

# Function to start streaming data
def start_streaming(spark):
    topic = 'customers_review'
    try:
        # Read data from a socket source
        stream_df = (spark.readStream.format("socket")
                .option("host", "localhost")
                .option("port", 9999)
                .load()
                )

        # Define the schema for the data
        schema = StructType([
            StructField("review_id", StringType()),
            StructField("user_id", StringType()),
            StructField("business_id", StringType()),
            StructField("stars", FloatType()),
            StructField("date", StringType()),
            StructField("text", StringType())
        ])

        # Parse the JSON data and select the fields
        stream_df = (stream_df
                     .select(from_json(col('value'), schema).alias("data"))
                     .select(("data.*")))

        # UDF to perform sentiment analysis
        # sentiment_analysis_udf = udf(sentiment_analysis, StringType())

        # Add a new column with the sentiment analysis result
        # stream_df = stream_df.withColumn('feedback',
        #                                     when(col('text').isNotNull(), sentiment_analysis_udf(col('text')))
        #                                     .otherwise(None)
        #                                     )

        # Convert the DataFrame to a Kafka source
        kafka_df = stream_df.selectExpr("CAST(review_id AS STRING) AS key", "to_json(struct(*)) AS value")
        
        # Write the data to a Kafka sink
        query = (kafka_df.writeStream
                 .format("kafka")
                 .option("kafka.bootstrap.servers", config['kafka']['bootstrap.servers'])
                 .option("kafka.security.protocol", config['kafka']['security.protocol'])
                 .option('kafka.sasl.mechanism', config['kafka']['sasl.mechanisms'])
                 .option('kafka.sasl.jaas.config',
                         'org.apache.kafka.common.security.plain.PlainLoginModule required username="{username}" '
                         'password="{password}";'.format(
                            username=config['kafka']['sasl.username'],
                            password=config['kafka']['sasl.password']
                        ))
                 .option('checkpointLocation', '/tmp/checkpoint')
                 .option('topic', topic)
                 .start()
                 .awaitTermination()
                 )
        
    except Exception as e:
        print(e)
        
if __name__ == '__main__':
    # Create a SparkSession
    spark_conn = SparkSession.builder.appName("SocketStreamConsumer").getOrCreate()
    # Start streaming data
    start_streaming(spark_conn)
