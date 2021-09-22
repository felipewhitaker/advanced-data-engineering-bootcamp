import os
from aws_cdk import core
from aws_cdk import aws_s3 as s3

from data_lake.base import BaseDataLakeBucket, DataLakeLayer

class DataLakeStack(core.Stack):

    def __init__(self, scope: core.Construct, **kwargs):
        self.deploy_env = os.environ["ENVIRONMENT"]
        super().__init__(scope, id = f"{self.deploy_env}-datalake-stack", **kwargs)

        self.datalake_raw_bucket = BaseDataLakeBucket(self, layer = DataLakeLayer.RAW)
        self.datalake_raw_bucket.add_lifecycle_rule(
            transitions = [
                s3.Transition(
                    storage_class = s3.StorageClass.INTELLIGENT_TIERING,
                    transition_after = core.Duration.days(30)
                ),
                s3.Transition(
                    storage_class = s3.StorageClass.GLACIER,
                    transition_after = core.Duration.days(180)
                )
            ]
        )

        self.datalake_processed_bucket = BaseDataLakeBucket(self, layer = DataLakeLayer.PROCESSED)
        self.datalake_curated_bucket = BaseDataLakeBucket(self, layer = DataLakeLayer.CURATED)
