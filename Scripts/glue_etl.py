import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Script generated for node Amazon S3
AmazonS3_node1741713422651 = glueContext.create_dynamic_frame.from_options(format_options={"quoteChar": "\"", "withHeader": True, "separator": ",", "optimizePerformance": False}, connection_type="s3", format="csv", connection_options={"paths": ["s3://s5.0/clientes.csv"], "recurse": True}, transformation_ctx="AmazonS3_node1741713422651")

# Script generated for node AWS Glue Data Catalog
AWSGlueDataCatalog_node1741713425035 = glueContext.write_dynamic_frame.from_catalog(frame=AmazonS3_node1741713422651, database="santy.db", table_name="clientes_csv", transformation_ctx="AWSGlueDataCatalog_node1741713425035")

job.commit()