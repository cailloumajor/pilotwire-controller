import json

from flask import Flask, request
from marshmallow import fields, Schema, validates, ValidationError

from .piface import PiFaceController


app = Flask(__name__)
controller = PiFaceController()


class ModesSchema(Schema):
    modes = fields.String(required=True)

    @validates('modes')
    def validate_modes(self, value):
        if not len(value) == 4:
            raise ValidationError("Must have four characters.")
        if not all([m in ['C', 'E', 'H', 'A'] for m in value]):
            raise ValidationError(
                "Each mode must be one of 'C', 'E', 'H', 'A'."
            )


modes_schema = ModesSchema()


@app.route('/modes')
def get_modes():
    return modes_schema.dumps(controller)


@app.route('/modes', methods=['PUT'])
def set_modes():
    data, errors = modes_schema.load(request.form)
    if errors:
        return json.dumps(errors), 400
    controller.modes = data['modes']
    return "Modes set on pilotwire controller: {}".format(controller.modes)
