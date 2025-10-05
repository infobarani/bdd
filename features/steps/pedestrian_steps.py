from behave import when, then

@when('the pedestrian button is pressed')
def step_impl(context):
    context.lib.Harness_PressButton()

@then('the pedestrian signal should be {signal}')
def step_impl(context, signal):
    expected = context.PED_MAP[signal]
    actual = context.lib.Harness_GetPedestrianSignal()
    assert actual == expected, f"Ped Signal: Expected {signal}, but got {context.REVERSE_PED_MAP.get(actual, 'Unknown')}"