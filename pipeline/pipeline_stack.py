
from variables import owner, repo

from aws_cdk import (
    Stack,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as codepipeline_actions,
    aws_codebuild as codebuild,

)

from constructs import Construct

class PipelineStack(Stack): 

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

       # Create a CodeBuild project
        project = codebuild.Project(self, "spi-test_project",
        build_spec=codebuild.BuildSpec.from_source_filename("codebuild_deployment.yaml"),
        source=codebuild.Source.bit_bucket(
        owner=owner,
        repo= repo

       )
    )

        # # Create a CodePipeline
        # pipeline = codepipeline.Pipeline(self, "MyFirstPipeline",
        # pipeline_name="MyPipeline"
        # )

   
       
        # codepipline stage for source 
        source_output = codepipeline.Artifact()
        source_action = codepipeline_actions.CodeStarConnectionsSourceAction(
        action_name="BitBucket_Source",
        owner=owner,
        repo= repo,
        output=source_output,
        connection_arn="arn:aws:codestar-connections:ap-south-1:679104321736:connection/569edc22-8e0c-4438-a3ae-4c011840a78f"
        )
        


        # Add a CodePipeline stage for CodeBuild
       
        build_action = codepipeline_actions.CodeBuildAction(
        action_name="CodeBuild",
        project=project,
        input=source_output,
        outputs=[codepipeline.Artifact()],  # optional
        execute_batch_build=False,  # optional, defaults to false
       )

        codepipeline.Pipeline(self, "spi-test",
           stages=[codepipeline.StageProps(
           stage_name="Source",
           actions=[source_action]
        ), codepipeline.StageProps(
           stage_name="Build",
           actions=[build_action]
        )
        ]
    )
        