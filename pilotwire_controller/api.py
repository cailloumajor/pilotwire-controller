import json

from flask import Flask, request
from marshmallow import fields, Schema, validates, ValidationError

from .piface import PiFaceController


app = Flask(__name__)
controller = PiFaceController()


class PilotwireSchema(Schema):
    modes = fields.String(required=True)
    version = fields.String(dump_only=True)

    @validates('modes')
    def validate_modes(self, value):
        if not len(value) > 0:
            raise ValidationError("Must have at least one character.")
        if not len(value) <= 4:
            raise ValidationError("Must have at most four characters.")
        if not all([m in ['C', 'E', 'H', 'A'] for m in value]):
            raise ValidationError(
                "Each mode must be one of 'C', 'E', 'H', 'A'."
            )


pilotwire_schema = PilotwireSchema()


@app.route('/pilotwire')
def get_pilotwire():
    return pilotwire_schema.dumps(controller)


@app.route('/pilotwire', methods=['PUT'])
def set_pilotwire():
    data, errors = pilotwire_schema.load(request.form)
    if errors:
        return json.dumps(errors), 400
    controller.modes = data['modes']
    return "Modes set on pilotwire controller: {}".format(controller.modes)
