import jsonschema

# JSON schema for UserSchema
user_schema = {
    "type": "object",
    "properties": {
        "username": {"type": "string"},
        "birth_year": {"type": "integer"},
        "country": {"type": "string"},
        "currency": {"type": "string"},
        "registration_date": {"type": "string", "format": "date-time"},
        "friends": {"type": "array", "items": {"type": "string"}}
    },
    "required": ["username", "birth_year", "country", "currency", "friends"],
    "additionalProperties": False
}

# JSON schema for EventSchema
event_schema = {
    "type": "object",
    "properties": {
        "begin_timestamp": {"type": "string", "format": "date-time"},
        "country": {"type": "string"},
        "end_timestamp": {"type": "string", "format": "date-time"},
        "league": {"type": "string"},
        "participants": {"type": "array", "items": {"type": "string"}},
        "sport": {"type": "string"}
    },
    "required": ["begin_timestamp", "country", "end_timestamp", "league", "participants", "sport"],
    "additionalProperties": False
}

# JSON schema for CouponSchema
coupon_schema = {
    "type": "object",
    "properties": {
        "selections": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "event_id": {"type": "integer"},
                    "odds": {"type": "number"}
                },
                "required": ["event_id", "odds"]
            }
        },
        "timestamp": {"type": "string", "format": "date-time"},
        "username": {"type": "string"}
    },
    "required": ["selections", "username"],
    "additionalProperties": False
}


# Methods for validating data against JSON schema
def validate_coupon_schema(data):
    """ function to validate coupon schema """

    try:
        jsonschema.validate(data, coupon_schema)
    except jsonschema.ValidationError as err:
        return False, err.message

    return True, "Coupon schema is valid."


def validate_event_schema(data):
    """ function to validate event schema """

    try:
        jsonschema.validate(data, event_schema)
    except jsonschema.ValidationError as err:
        return False, err.message

    return True, "Event schema is valid."


def validate_user_schema(data):
    """ function to validate user schema """
    try:
        jsonschema.validate(data, user_schema)
    except jsonschema.ValidationError as err:
        return False, err.message

    return True, "User schema is valid."


def validate_users_schema(users):
    """ function to validate users schema """
    try:
        for user in users:
            jsonschema.validate(user, user_schema)
    except jsonschema.ValidationError as err:
        return False, err.message

    return True, "Schemas are valid"


def validate_coupons_schema(coupons):
    """ function to validate users schema """
    try:
        for coupon in coupons:
            jsonschema.validate(coupon, coupon_schema)
    except jsonschema.ValidationError as err:
        return False, err.message

    return True, "Schemas are valid"
