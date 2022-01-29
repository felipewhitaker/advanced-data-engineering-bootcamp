from aws_cdk import aws_s3 as s3
from aws_cdk import core 

from enum import Enum

class DataLakeLayer(Enum):
    RAW = "raw"
    PROCESSED = "processed"
    CURATED = "curated"

class BaseDataLakeBucket(s3.Bucket):

    def __init__(self, scope: core.Construct, layer: DataLakeLayer, **kwargs):
        self.layer = layer
        self.deploy_env = scope.deploy_env
        self.obj_name = f"s3-thor-{self.deploy_env}-datalake-{self.layer.value}"

        super().__init__(
            scope = scope,
            id = self.obj_name,
            bucket_name = self.obj_name,
            block_public_access = s3.BlockPublicAccess.BLOCK_ALL,
            encryption = s3.BucketEncryption.S3_MANAGED,
            versioned = True,
            removal_policy = core.RemovalPolicy.DESTROY,
            **kwargs
        )

        self.set_default_lifecycle_rules()

    def set_default_lifecycle_rules(self):
        """
        Sets lifecycle rule by default
        """
        self.add_lifecycle_rule(
            abort_incomplete_multipart_upload_after = core.Duration.days(7), enabled=True
        )
        self.add_lifecycle_rule(
            transitions = [
                s3.Transition(
                    storage_class = s3.StorageClass.INTELLIGENT_TIERING,
                    transition_after = core.Duration.days(90),
                )
            ],
            noncurrent_version_transitions = [
                s3.NoncurrentVersionTransition(
                    storage_class = s3.StorageClass.INFREQUENT_ACCESS,
                    transition_after = core.Duration.days(30),
                ),
            ]
        )
        self.add_lifecycle_rule(
            expiration = core.Duration.days(365)
        )
        