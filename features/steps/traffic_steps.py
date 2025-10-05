from behave import given

@given('the traffic controller is initialized')
def step_impl(context):
    context.lib.Harness_Init()