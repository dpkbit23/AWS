# AWS
# PySpark EMR ETL Pipeline

This project demonstrates how to run a secure, production-grade PySpark ETL job on AWS EMR using configuration files and AWS Secrets Manager.

---

## 🔧 Features

- ✅ PySpark job that extracts data from an RDBMS (via JDBC)
- ✅ S3 input/output configurable via `config.yaml`
- ✅ Credentials securely retrieved using AWS Secrets Manager
- ✅ Deploy script to run on auto-terminating EMR cluster

---

## 🗂 Project Structure

```
pyspark-emr-etl-pipeline/
├── config/
│   └── config.yaml              # Config file (S3 paths, secret name, region, table)
├── scripts/
│   └── deploy_emr_job.sh       # Shell script to deploy EMR job
└── src/
    └── etl_pipeline.py         # PySpark job that reads config & secrets
```

---

## 🛠 Requirements

- Python 3.7+
- AWS CLI configured
- AWS Secrets Manager secret with RDBMS credentials
- EMR release: 6.15.0+
- PySpark dependencies installed via EMR or bootstrap

---

## 🔐 Example Secret JSON (Secrets Manager)

```json
{
  "username": "db_user",
  "password": "db_password",
  "engine": "mysql",
  "host": "your-db-host.amazonaws.com",
  "port": 3306,
  "dbname": "your_db"
}
```

Store this under a secret name like `rds-mysql-credentials`.

---

## 🚀 Running the Job

1. Upload your PySpark script and config to S3.
2. Run:

```bash
cd scripts
./deploy_emr_job.sh
```

This launches an EMR cluster, runs the job, and auto-terminates the cluster.

---

## 📦 Deployment Notes

- Customize the S3 paths in `config/config.yaml`.
- Modify `scripts/deploy_emr_job.sh` to set your own key pair, log URI, etc.
- Ensure EMR EC2 Role has access to S3 buckets and Secrets Manager.

---

## 🧩 Future Improvements

- Terraform provisioning of EMR & S3
- SSL-encrypted JDBC connection
- Integrated logging/monitoring

---

## 📄 License


