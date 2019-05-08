ACTION_PLAN = {
    "name": "test name",
    "description": "test description",
    "_links": {
        "self": {
            "href": "http://localhost:8301/actionPlans/4c27fcbf-e069-44db-a239-99c9cd70a1d0"
        },
        "actionPlan": {
            "href": "http://localhost:8301/actionPlans/4c27fcbf-e069-44db-a239-99c9cd70a1d0"
        },
        "actionRules": {
            "href": "http://localhost:8301/actionPlans/4c27fcbf-e069-44db-a239-99c9cd70a1d0/actionRules"
        }
    }}

ACTION_RULES = {
    "_embedded": {
        "actionRules": [{
            "actionType": "ICL1E",
            "triggerDateTime": "2019-05-08T08:00:00Z",
            "hasTriggered": False,
            "classifiers": None,
            "_links": {
                "self": {
                    "href": "http://localhost:8301/actionRules/156ba07d-37eb-4836-a1fb-3ab1580c1cf9"
                },
                "actionRule": {
                    "href": "http://localhost:8301/actionRules/156ba07d-37eb-4836-a1fb-3ab1580c1cf9"
                },
                "actionPlan": {
                    "href": "http://localhost:8301/actionRules/156ba07d-37eb-4836-a1fb-3ab1580c1cf9/actionPlan"
                }
            }
        }]
    },
    "_links": {
        "self": {
            "href": "http://localhost:8301/actionPlans/4c27fcbf-e069-44db-a239-99c9cd70a1d0/actionRules"
        }
    }
}
