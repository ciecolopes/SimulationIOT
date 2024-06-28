from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, TimestampType, DoubleType, IntegerType, ArrayType, MapType

from config import configuration

def main():
    spark = SparkSession.builder.appName("PedeProntoStreaming") \
        .config("spark.jars.packages",
                "org.apache.spark:spark-sql-kafka-0-10_2.13:3.5.0,"
                "org.apache.hadoop:hadoop-aws:3.3.1,"
                "com.amazonaws:aws-java-sdk:1.11.469") \
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
        .config("spark.hadoop.fs.s3a.access.key", configuration.get('AWS_ACCESS_KEY')) \
        .config("spark.hadoop.fs.s3a.secret.key", configuration.get('AWS_SECRET_KEY')) \
        .config('spark.hadoop.fs.s3a.aws.credentials.provider',
                'org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider') \
        .getOrCreate()

    spark.sparkContext.setLogLevel("WARN")

    # Order schema
    orderSchema = StructType([
        StructField("id", StringType(), True),
        StructField("customerId", StringType(), True),
        StructField("timestamp", TimestampType(), True),
        StructField("items", ArrayType(MapType(StringType(), StringType())), True),
        StructField("totalPrice", DoubleType(), True),
    ])

    # Status schema
    statusSchema = StructType([
        StructField("id", StringType(), True),
        StructField("timestamp", TimestampType(), True),
        StructField("status", StringType(), True),
    ])

    # Review schema
    reviewSchema = StructType([
        StructField("id", StringType(), True),
        StructField("timestamp", TimestampType(), True),
        StructField("rating", IntegerType(), True),
        StructField("comments", StringType(), True),
    ])

    def read_kafka_topic(topic, schema):
        return (spark.readStream
                .format('kafka')
                .option('kafka.bootstrap.servers', 'broker:29092')
                .option('subscribe', topic)
                .option('startingOffsets', 'earliest')
              # micro-batch  .option('maxOffsetsPerTrigger', 1000)  # Limita a leitura a 1000 registros por micro-batch
                .load()
                .selectExpr('CAST(value AS STRING)')
                .select(from_json(col('value'), schema).alias('data'))
                .select('data.*')
                .withWatermark('timestamp', '2 minutes')
                )

    def streamWriter(input: DataFrame, checkpointFolder, output):
        return (input.writeStream
                .format('parquet')
                .option('checkpointLocation', checkpointFolder)
                .option('path', output)
                .outputMode('append')
                .start())

    orderDF = read_kafka_topic('order_data', orderSchema).alias('order')
    statusDF = read_kafka_topic('status_data', statusSchema).alias('status')
    reviewDF = read_kafka_topic('review_data', reviewSchema).alias('review')

    # Write streams to S3
    query1 = streamWriter(orderDF, 's3a://spark-streaming-data/checkpoints/order_data',
                          's3a://spark-streaming-data/data/raw/order_data')
    query2 = streamWriter(statusDF, 's3a://spark-streaming-data/checkpoints/status_data',
                          's3a://spark-streaming-data/data/raw/status_data')
    query3 = streamWriter(reviewDF, 's3a://spark-streaming-data/checkpoints/review_data',
                          's3a://spark-streaming-data/data/raw/review_data')

    query1.awaitTermination()
    query2.awaitTermination()
    query3.awaitTermination()

if __name__ == "__main__":
    main()