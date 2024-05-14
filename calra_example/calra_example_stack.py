from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    aws_lambda as _lambda,
    aws_lambda_python_alpha as _lambda_python,
    aws_apigateway as apigateway,
)
from calra_cdk import ResourceBuilder
from constructs import Construct

class CalraExampleStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        builder = ResourceBuilder()
        lambda_path = 'lambdas'

        restapi = apigateway.RestApi(
            self, 'calra-RestApi',
            rest_api_name= 'calra-restApi')
        root_resource = restapi.root

        builder.set_default_timeout(Duration.seconds(60))
        builder.set_default_runtime(_lambda.Runtime.PYTHON_3_10)
        builder.add_common_environment("URL", "http://example.com")
        builder.add_custom_environment("DB_NAME_CATS", "cats")
        builder.add_custom_environment("DB_NAME_DOGS", "dogs")

        builder.build(self, root_resource, lambda_path, print_tree=True)