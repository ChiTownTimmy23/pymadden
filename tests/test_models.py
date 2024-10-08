from pymadden.models import PlayerRating, RatingsResponse


def test_player_rating_model():
    player_data = {
        "college": "University",
        "awareness_rating": 90,
        "throwPower_rating": 85,
        "kickReturn_rating": 70,
        "leadBlock_rating": 60,
        "strength_rating": 80,
        "bCVision_rating": 85,
        "catchInTraffic_rating": 75,
        "playAction_rating": 80,
        "pursuit_rating": 75,
        "plyrAssetname": "JohnDoe",
        "mediumRouteRunning_rating": 80,
        "catching_rating": 85,
        "acceleration_rating": 90,
        "spinMove_rating": 75,
        "height": 72,
        "finesseMoves_rating": 80,
        "spectacularCatch_rating": 85,
        "runBlock_rating": 70,
        "tackle_rating": 65,
        "injury_rating": 90,
        "zoneCoverage_rating": 80,
        "weight": 200,
        "plyrBirthdate": "1/1/1990",
        "runningStyle_rating": "Default Stride Loose",
        "deepRouteRunning_rating": 75,
        "firstName": "John",
        "yearsPro": 5,
        "totalSalary": 5000000,
        "trucking_rating": 70,
        "throwAccuracyShort_rating": 85,
        "position": "QB",
        "jukeMove_rating": 80,
        "playRecognition_rating": 85,
        "shortRouteRunning_rating": 90,
        "status": "published",
        "lastName": "Doe",
        "jerseyNum": 10,
        "breakSack_rating": 80,
        "speed_rating": 90,
        "runBlockPower_rating": 70,
        "jumping_rating": 85,
        "toughness_rating": 90,
        "throwOnTheRun_rating": 80,
        "manCoverage_rating": 75,
        "stiffArm_rating": 75,
        "powerMoves_rating": 70,
        "iteration": "launch-ratings",
        "release_rating": 85,
        "hitPower_rating": 80,
        "throwAccuracyMid_rating": 80,
        "kickAccuracy_rating": 60,
        "passBlockPower_rating": 65,
        "impactBlocking_rating": 70,
        "stamina_rating": 90,
        "carrying_rating": 85,
        "breakTackle_rating": 80,
        "plyrPortrait": 1,
        "kickPower_rating": 70,
        "plyrHandedness": "Right",
        "throwUnderPressure_rating": 80,
        "team": "Team1",
        "signingBonus": 1000000,
        "passBlock_rating": 65,
        "changeOfDirection_rating": 85,
        "press_rating": 75,
        "throwAccuracyDeep_rating": 75,
        "archetype": "QB_Scrambler",
        "blockShedding_rating": 70,
        "runBlockFinesse_rating": 65,
        "teamId": 1,
        "agility_rating": 90,
        "fullNameForSearch": "John Doe",
        "overall_rating": 90,
        "passBlockFinesse_rating": 60,
        "age": 28,
        "primaryKey": 1,
    }
    player_rating = PlayerRating(**player_data)

    assert player_rating.firstName == "John"
    assert player_rating.lastName == "Doe"
    assert player_rating.position == "QB"
    assert player_rating.team == "Team1"
    assert player_rating.overall_rating == 90
    assert player_rating.speed_rating == 90
    assert player_rating.awareness_rating == 90
    assert player_rating.throwPower_rating == 85


def test_ratings_response_model():
    response_data = {
        "count": 2,
        "docs": [
            {
                "college": "Mock University 1",
                "awareness_rating": 85,
                "throwPower_rating": 90,
                "kickReturn_rating": 75,
                "leadBlock_rating": 65,
                "strength_rating": 85,
                "bCVision_rating": 80,
                "catchInTraffic_rating": 80,
                "playAction_rating": 75,
                "pursuit_rating": 80,
                "plyrAssetname": "MockPlayer1",
                "mediumRouteRunning_rating": 75,
                "catching_rating": 80,
                "acceleration_rating": 85,
                "spinMove_rating": 80,
                "height": 70,
                "finesseMoves_rating": 75,
                "spectacularCatch_rating": 80,
                "runBlock_rating": 75,
                "tackle_rating": 70,
                "injury_rating": 85,
                "zoneCoverage_rating": 75,
                "weight": 190,
                "plyrBirthdate": "2/2/1992",
                "runningStyle_rating": "Default Stride Tight",
                "deepRouteRunning_rating": 70,
                "firstName": "Mock",
                "lastName": "Player1",
                "yearsPro": 3,
                "totalSalary": 3000000,
                "trucking_rating": 75,
                "throwAccuracyShort_rating": 80,
                "position": "WR",
                "jukeMove_rating": 85,
                "playRecognition_rating": 80,
                "shortRouteRunning_rating": 85,
                "status": "published",
                "jerseyNum": 20,
                "breakSack_rating": 75,
                "speed_rating": 85,
                "runBlockPower_rating": 75,
                "jumping_rating": 80,
                "toughness_rating": 85,
                "throwOnTheRun_rating": 75,
                "manCoverage_rating": 70,
                "stiffArm_rating": 80,
                "powerMoves_rating": 75,
                "iteration": "launch-ratings",
                "release_rating": 80,
                "hitPower_rating": 75,
                "throwAccuracyMid_rating": 75,
                "kickAccuracy_rating": 65,
                "passBlockPower_rating": 70,
                "impactBlocking_rating": 75,
                "stamina_rating": 85,
                "carrying_rating": 90,
                "breakTackle_rating": 85,
                "plyrPortrait": 2,
                "kickPower_rating": 65,
                "plyrHandedness": "Right",
                "throwUnderPressure_rating": 75,
                "team": "Mock Team 1",
                "signingBonus": 500000,
                "passBlock_rating": 70,
                "changeOfDirection_rating": 80,
                "press_rating": 70,
                "throwAccuracyDeep_rating": 70,
                "archetype": "RB_Elusive",
                "blockShedding_rating": 65,
                "runBlockFinesse_rating": 70,
                "teamId": 1,
                "agility_rating": 85,
                "fullNameForSearch": "Mock Player2",
                "overall_rating": 95,
                "passBlockFinesse_rating": 65,
                "age": 26,
                "primaryKey": 1,
            },
            {
                "college": "Mock University 2",
                "awareness_rating": 85,
                "throwPower_rating": 90,
                "kickReturn_rating": 75,
                "leadBlock_rating": 65,
                "strength_rating": 85,
                "bCVision_rating": 80,
                "catchInTraffic_rating": 80,
                "playAction_rating": 75,
                "pursuit_rating": 80,
                "plyrAssetname": "MockPlayer2",
                "mediumRouteRunning_rating": 75,
                "catching_rating": 80,
                "acceleration_rating": 85,
                "spinMove_rating": 80,
                "height": 70,
                "finesseMoves_rating": 75,
                "spectacularCatch_rating": 80,
                "runBlock_rating": 75,
                "tackle_rating": 70,
                "injury_rating": 85,
                "zoneCoverage_rating": 75,
                "weight": 190,
                "plyrBirthdate": "2/2/1992",
                "runningStyle_rating": "Default Stride Tight",
                "deepRouteRunning_rating": 70,
                "firstName": "Mock",
                "lastName": "Player2",
                "yearsPro": 3,
                "totalSalary": 3000000,
                "trucking_rating": 75,
                "throwAccuracyShort_rating": 80,
                "position": "RB",
                "jukeMove_rating": 85,
                "playRecognition_rating": 80,
                "shortRouteRunning_rating": 85,
                "status": "published",
                "jerseyNum": 20,
                "breakSack_rating": 75,
                "speed_rating": 85,
                "runBlockPower_rating": 75,
                "jumping_rating": 80,
                "toughness_rating": 85,
                "throwOnTheRun_rating": 75,
                "manCoverage_rating": 70,
                "stiffArm_rating": 80,
                "powerMoves_rating": 75,
                "iteration": "launch-ratings",
                "release_rating": 80,
                "hitPower_rating": 75,
                "throwAccuracyMid_rating": 75,
                "kickAccuracy_rating": 65,
                "passBlockPower_rating": 70,
                "impactBlocking_rating": 75,
                "stamina_rating": 85,
                "carrying_rating": 90,
                "breakTackle_rating": 85,
                "plyrPortrait": 2,
                "kickPower_rating": 65,
                "plyrHandedness": "Right",
                "throwUnderPressure_rating": 75,
                "team": "Mock Team 2",
                "signingBonus": 500000,
                "passBlock_rating": 70,
                "changeOfDirection_rating": 80,
                "press_rating": 70,
                "throwAccuracyDeep_rating": 70,
                "archetype": "RB_Elusive",
                "blockShedding_rating": 65,
                "runBlockFinesse_rating": 70,
                "teamId": 2,
                "agility_rating": 85,
                "fullNameForSearch": "Mock Player2",
                "overall_rating": 92,
                "passBlockFinesse_rating": 65,
                "age": 26,
                "primaryKey": 2,
            },
        ],
    }
    ratings_response = RatingsResponse(**response_data)

    assert ratings_response.count == 2
    assert len(ratings_response.docs) == 2
    assert isinstance(ratings_response.docs[0], PlayerRating)
    assert isinstance(ratings_response.docs[1], PlayerRating)
    assert ratings_response.docs[0].firstName == "Mock"
    assert ratings_response.docs[0].lastName == "Player1"
    assert ratings_response.docs[0].position == "WR"
    assert ratings_response.docs[0].team == "Mock Team 1"
    assert ratings_response.docs[0].overall_rating == 95
    assert ratings_response.docs[1].firstName == "Mock"
    assert ratings_response.docs[1].lastName == "Player2"
    assert ratings_response.docs[1].position == "RB"
    assert ratings_response.docs[1].team == "Mock Team 2"
    assert ratings_response.docs[1].overall_rating == 92
