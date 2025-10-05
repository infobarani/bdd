from behave import then

@then('the main light should be {color}')
def step_impl(context, color):
    expected = context.LIGHT_MAP[color]
    actual = context.lib.Harness_GetMainLight()
    assert actual == expected, f"Main Light: Expected {color}, but got {context.REVERSE_LIGHT_MAP.get(actual, 'Unknown')}"

@then('the side light should be {color}')
def step_impl(context, color):
    expected = context.LIGHT_MAP[color]
    actual = context.lib.Harness_GetSideLight()
    assert actual == expected, f"Side Light: Expected {color}, but got {context.REVERSE_LIGHT_MAP.get(actual, 'Unknown')}"

@then('all vehicle lights should be Red')
def step_impl(context):
    main_light = context.lib.Harness_GetMainLight()
    side_light = context.lib.Harness_GetSideLight()
    assert main_light == context.lib.LIGHT_STATE_RED, f"Main Light: Expected Red, but got {context.REVERSE_LIGHT_MAP.get(main_light, 'Unknown')}"
    assert side_light == context.lib.LIGHT_STATE_RED, f"Side Light: Expected Red, but got {context.REVERSE_LIGHT_MAP.get(side_light, 'Unknown')}"