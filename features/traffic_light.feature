Feature: Traffic Light Controller

  The controller must manage a two-way intersection with a pedestrian crossing,
  ensuring safe and predictable light sequences.

  Scenario: Normal traffic cycle without interruption
    Given the traffic controller is initialized
    Then the main light should be Green
    And the side light should be Red

    When 20 seconds pass
    Then the main light should be Yellow

    When 4 seconds pass
    Then the main light should be Red

    When 2 seconds pass
    Then the side light should be Green

    When 10 seconds pass
    Then the side light should be Yellow

    When 4 seconds pass
    Then the side light should be Red

    When 2 seconds pass
    Then the main light should be Green


  Scenario: Pedestrian button is pressed during Main Green
    Given the traffic controller is initialized
    When the pedestrian button is pressed
    And 19 seconds pass
    # Still main green, almost time to change
    Then the main light should be Green

    When 1 second passes
    # Total 20s passed, now it should be yellow
    Then the main light should be Yellow

    When 4 seconds pass
    # Total 24s passed, now NS is red
    Then the main light should be Red

    When 2 seconds pass
    # Total 26s passed, after clearance, the pedestrian sequence should start
    Then all vehicle lights should be Red
    And the pedestrian signal should be Walk

    When 10 seconds pass
    # Total 36s passed
    Then the pedestrian signal should be Flashing Don't Walk

    When 6 seconds pass
    # Total 42s passed, ped sequence ends, back to clearance
    Then the pedestrian signal should be Don't Walk
    And all vehicle lights should be Red

    When 2 seconds pass
    # Total 44s passed, clearance is over, side street gets green
    Then the side light should be Green

  Scenario: Pedestrian button is pressed during Side Road Green
    Given the traffic controller is initialized
    # Go to side road green
    When 26 seconds pass
    Then the side light should be Green

    When the pedestrian button is pressed
    And 9 seconds pass
    # Still side green, almost time to change
    Then the side light should be Green

    When 1 second passes
    # Total 10s passed, now it should be yellow
    Then the side light should be Yellow

    When 4 seconds pass
    # Total 14s passed, now EW is red
    Then the side light should be Red

    When 2 seconds pass
    # Total 16s passed, after clearance, the main road should be green
    Then the main light should be Green
    
    When 20 seconds pass
    Then the main light should be Yellow

    When 4 seconds pass
    Then the main light should be Red

    When 2 seconds pass
    # After clearance, the pedestrian sequence should start
    Then all vehicle lights should be Red
    And the pedestrian signal should be Walk

  Scenario: Pedestrian button is pressed during Main Road Yellow
    Given the traffic controller is initialized
    # Go to main road yellow
    When 20 seconds pass
    Then the main light should be Yellow

    When the pedestrian button is pressed
    And 3 seconds pass
    # Still main yellow, almost time to change
    Then the main light should be Yellow

    When 1 second passes
    # Total 4s passed, now it should be red
    Then the main light should be Red

    When 2 seconds pass
    # After clearance, the pedestrian sequence should start
    Then all vehicle lights should be Red
    And the pedestrian signal should be Walk

  Scenario: Multiple pedestrian button presses
    Given the traffic controller is initialized
    When the pedestrian button is pressed
    And 1 second passes
    When the pedestrian button is pressed
    And 1 second passes
    When the pedestrian button is pressed
    And 17 seconds pass
    # Still main green, almost time to change
    Then the main light should be Green

    When 1 second passes
    # Total 20s passed, now it should be yellow
    Then the main light should be Yellow

    When 4 seconds pass
    # Total 24s passed, now NS is red
    Then the main light should be Red

    When 2 seconds pass
    # Total 26s passed, after clearance, the pedestrian sequence should start
    Then all vehicle lights should be Red
    And the pedestrian signal should be Walk
