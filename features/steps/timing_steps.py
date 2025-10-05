from behave import when

@when('{seconds:d} second passes')
@when('{seconds:d} seconds pass')
def step_impl(context, seconds):
    # Call Tick() in small increments to simulate time
    ms_to_pass = seconds * 1000
    tick_increment_ms = 10
    for _ in range(ms_to_pass // tick_increment_ms):
        context.lib.Harness_Tick(tick_increment_ms)