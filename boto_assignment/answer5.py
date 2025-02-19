import boto3
import datetime
import csv

# Initialize AWS clients
ec2 = boto3.client("ec2")
cloudwatch = boto3.client("cloudwatch")
rds = boto3.client("rds")
lambda_client = boto3.client("lambda")
s3 = boto3.client("s3")

# Get the current date
now = datetime.datetime.utcnow()

# 1️⃣ **Identify EC2 instances with low CPU utilization**
def check_ec2_usage():
    underutilized_instances = []
    instances = ec2.describe_instances()

    for reservation in instances["Reservations"]:
        for instance in reservation["Instances"]:
            instance_id = instance["InstanceId"]

            # Get CPU utilization from CloudWatch
            metrics = cloudwatch.get_metric_statistics(
                Namespace="AWS/EC2",
                MetricName="CPUUtilization",
                Dimensions=[{"Name": "InstanceId", "Value": instance_id}],
                StartTime=now - datetime.timedelta(days=30),
                EndTime=now,
                Period=86400,
                Statistics=["Average"],
            )

            avg_cpu = (
                sum(datapoint["Average"] for datapoint in metrics["Datapoints"])
                / len(metrics["Datapoints"])
                if metrics["Datapoints"]
                else 0
            )

            if avg_cpu < 10:  # If CPU utilization is below 10%
                underutilized_instances.append([instance_id, avg_cpu])

    return underutilized_instances


# 2️⃣ **Find RDS instances with no connections for 7+ days**
def check_rds_usage():
    idle_rds_instances = []
    rds_instances = rds.describe_db_instances()

    for db in rds_instances["DBInstances"]:
        db_id = db["DBInstanceIdentifier"]

        # Get database connections from CloudWatch
        metrics = cloudwatch.get_metric_statistics(
            Namespace="AWS/RDS",
            MetricName="DatabaseConnections",
            Dimensions=[{"Name": "DBInstanceIdentifier", "Value": db_id}],
            StartTime=now - datetime.timedelta(days=7),
            EndTime=now,
            Period=86400,
            Statistics=["Average"],
        )

        avg_connections = (
            sum(datapoint["Average"] for datapoint in metrics["Datapoints"])
            / len(metrics["Datapoints"])
            if metrics["Datapoints"]
            else 0
        )

        if avg_connections == 0:  # If no connections in the past 7 days
            idle_rds_instances.append([db_id, avg_connections])

    return idle_rds_instances


# 3️⃣ **Find Lambda functions not used in the last 30 days**
def check_lambda_usage():
    unused_lambdas = []
    functions = lambda_client.list_functions()

    for function in functions["Functions"]:
        function_name = function["FunctionName"]

        # Get invocation count from CloudWatch
        metrics = cloudwatch.get_metric_statistics(
            Namespace="AWS/Lambda",
            MetricName="Invocations",
            Dimensions=[{"Name": "FunctionName", "Value": function_name}],
            StartTime=now - datetime.timedelta(days=30),
            EndTime=now,
            Period=86400,
            Statistics=["Sum"],
        )

        invocations = (
            sum(datapoint["Sum"] for datapoint in metrics["Datapoints"])
            if metrics["Datapoints"]
            else 0
        )

        if invocations == 0:  # If not invoked in the last 30 days
            unused_lambdas.append([function_name, invocations])

    return unused_lambdas


# 4️⃣ **Identify empty or unused S3 buckets**
def check_s3_usage():
    unused_buckets = []
    buckets = s3.list_buckets()["Buckets"]

    for bucket in buckets:
        bucket_name = bucket["Name"]
        objects = s3.list_objects_v2(Bucket=bucket_name)

        if "Contents" not in objects:  # If the bucket has no objects
            unused_buckets.append([bucket_name, "No Objects"])

    return unused_buckets


# 5️⃣ **Generate Report and Save to CSV**
def generate_report():
    ec2_data = check_ec2_usage()
    rds_data = check_rds_usage()
    lambda_data = check_lambda_usage()
    s3_data = check_s3_usage()

    # Save to CSV files
    with open("ec2_low_usage.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["EC2 Instance ID", "Average CPU Usage (%)"])
        writer.writerows(ec2_data)

    with open("rds_idle.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["RDS Instance ID", "Average Connections"])
        writer.writerows(rds_data)

    with open("unused_lambda.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Lambda Function", "Invocations (Last 30 Days)"])
        writer.writerows(lambda_data)

    with open("unused_s3.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["S3 Bucket", "Status"])
        writer.writerows(s3_data)

    print("✅ Cost Optimization Report Generated!")


# Run the script
if __name__ == "__main__":
    generate_report()
