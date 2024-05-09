import aws_cdk as core
import aws_cdk.assertions as assertions

from calra_example.calra_example_stack import CalraExampleStack

# example tests. To run these tests, uncomment this file along with the example
# resource in calra_example/calra_example_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CalraExampleStack(app, "calra-example")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
