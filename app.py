#!/usr/bin/env python3
import os

import aws_cdk as cdk

from _dyra_task._dyra_task_stack import DyraTaskStack


app = cdk.App()

# call the Stack
DyraTaskStack(app, "DyraTaskStack")

app.synth()
