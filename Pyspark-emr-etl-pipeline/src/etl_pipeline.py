import boto3
import json
import yaml
import sys
import logging
from pyspark.sql import SparkSession

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_config(config_path):
    logger.info(f"Loading config from {config_path}")
    if config_path.endswith(".yaml") or config_path.endswith(".yml"):
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    elif config_path.endswith(".json"):
        with open(config_path, 'r') as f:
            return json.load(f)
    else:
        raise ValueError("Unsupported config format. Use YAML or JSON.")

def get_rdbms_credentials(secret_name, region_name):
    logger.info(f"Fetching secret {secret_name} from AWS Secrets Manager")
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)
    response = client.get_secret_value(SecretId=secret_name)
    secret = json.loads(response['SecretString'])
    return secret

def get_spark_session(app_name: str):
    return SparkSession.builder         .appName(app_name)         .config("spark.sql.sources.partitionOverwriteMode", "dynamic")         .getOrCreate()

def main(config_path):
    config = load_config(config_path)
    s3_input_path = config['s3_paths']['input']
    s3_output_path = config['s3_paths']['output']
    secret_name = config['database']['secret_name']
    region = config['database']['region']
    table_name = config['database']['table']

    credentials = get_rdbms_credentials(secret_name, region)

    spark = get_spark_session("PySparkETLPipeline")

    try:
        jdbc_url = f"jdbc:{credentials['engine']}://{credentials['host']}:{credentials['port']}/{credentials['dbname']}"
        logger.info(f"Reading table {table_name} from {credentials['host']}")

        df_rdbms = spark.read             .format("jdbc")             .option("url", jdbc_url)             .option("dbtable", table_name)             .option("user", credentials['username'])             .option("password", credentials['password'])             .option("driver", "com.mysql.cj.jdbc.Driver")             .load()

        df_rdbms.write             .mode("overwrite")             .parquet(s3_output_path)

        logger.info("Pipeline completed successfully.")
    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}")
        sys.exit(1)
    finally:
        spark.stop()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        logger.error("Usage: python etl_pipeline.py <config_path>")
        sys.exit(1)

    config_path = sys.argv[1]
    main(config_path)
