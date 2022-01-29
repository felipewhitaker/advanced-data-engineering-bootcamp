#!/usr/bin/env python3
import os

from aws_cdk import core as cdk

# For consistency with TypeScript code, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core

from data_lake.stack import DataLakeStack
from kinesis.stack import KinesisStack

app = core.App()
data_lake_stack = DataLakeStack(app)
kinesis_stack = KinesisStack(app, data_lake_raw_bucket=data_lake_stack.data_lake_raw_bucket)

app.synth()
