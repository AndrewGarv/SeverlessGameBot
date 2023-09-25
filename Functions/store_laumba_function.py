import json

game_consoles = ['xbox series x', 'playstation 5', 'nintendo switch']
game_stores = ['eb games', 'best buy', 'classicgamez']
eb_games_types = ['the wonderful 101', 'bayonetta', 'elden ring']
best_buy_types = ['starfield', 'street fighter vi', 'xenoblade Chronicles']
classic_types = ['viewtiful joe', 'alien soldier', 'castlevania']


def validate_order(slots):
    # Validate Consoles
    if not slots['GameConsole']:
        print('Validating GameConsole Slot')

        return {
            'isValid': False,
            'invalidSlot': 'GameConsole'
        }

    if slots['GameConsole']['value']['originalValue'].lower() not in game_consoles:
        print('Invalid Console')

        return {
            'isValid': False,
            'invalidSlot': 'GameConsole',
            'message': 'Please select a {} console.'.format(", ".join(game_consoles))
        }

    # Validate Stores
    if not slots['GameStores']:
        print('Validating GameStores Slot')

        return {
            'isValid': False,
            'invalidSlot': 'GameStores'
        }

    if slots['GameStores']['value']['originalValue'].lower() not in game_stores:
        print('Invalid Store')

        return {
            'isValid': False,
            'invalidSlot': 'GameStores',
            'message': 'Please select from {} a store.'.format(", ".join(game_stores))
        }

    # Validate Game
    if not slots['GameSelection']:
        print('Validating game')

        return {
            'isValid': False,
            'invalidSlot': 'GameSelection'
        }

    # Validate type by type
    if slots['GameStores']['value']['originalValue'].lower() == 'eb games':
        if slots['GameSelection']['value']['originalValue'].lower() not in eb_games_types:
            print('Invalid Game for store')

            return {
                'isValid': False,
                'invalidSlot': 'GameSelection',
                'message': 'Please select a game from {}.'.format(", ".join(eb_games_types))
            }

    if slots['GameStores']['value']['originalValue'].lower() == 'best buy':
        if slots['GameSelection']['value']['originalValue'].lower() not in best_buy_types:
            print('Invalid Game for Best Buy')

            return {
                'isValid': False,
                'invalidSlot': 'GameStores',
                'message': 'Please select a game of {}.'.format(", ".join(best_buy_types))
            }

    if slots['GameStores']['value']['originalValue'].lower() == 'classicgamez':
        if slots['GameSelection']['value']['originalValue'].lower() not in best_buy_types:
            print('Invalid Game for this store')

            return {
                'isValid': False,
                'invalidSlot': 'GameStores',
                'message': 'Please select something older like Alien Soldier'.format(", ".join(classic_types))
            }

    # Valid Order
    return {'isValid': True}


def lambda_handler(event, context):
    print(event)

    bot = event['bot']['name']
    slots = event['sessionState']['intent']['slots']
    intent = event['sessionState']['intent']['name']

    order_validation_result = validate_order(slots)

    if event['invocationSource'] == 'DialogCodeHook':
        if not order_validation_result['isValid']:
            if 'message' in order_validation_result:
                response = {
                    "sessionState": {
                        "dialogAction": {
                            "slotToElicit": order_validation_result['invalidSlot'],
                            "type": "ElicitSlot"
                        },
                        "intent": {
                            "name": intent,
                            "slots": slots
                        }
                    },
                    "messages": [
                        {
                            "contentType": "PlainText",
                            "content": order_validation_result['message']
                        }
                    ]
                }
            else:
                response = {
                    "sessionState": {
                        "dialogAction": {
                            "slotToElicit": order_validation_result['invalidSlot'],
                            "type": "ElicitSlot"
                        },
                        "intent": {
                            "name": intent,
                            "slots": slots
                        }
                    }
                }
        else:
            response = {
                "sessionState": {
                    "dialogAction": {
                        "type": "Delegate"
                    },
                    "intent": {
                        'name': intent,
                        'slots': slots
                    }
                }
            }

    if event['invocationSource'] == 'FulfillmentCodeHook':
        response = {
            "sessionState": {
                "dialogAction": {
                    "type": "Close"
                },
                "intent": {
                    "name": intent,
                    "slots": slots,
                    "state": "Fulfilled"
                }

            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": "Your games are ready."
                }
            ]
        }

    print(response)
    return response