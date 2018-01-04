import re

from flask import Flask, jsonify, request
from flask.views import MethodView
from marshmallow import Schema, ValidationError, fields, validates

from .piface import PiFaceController

app = Flask(__name__)
controller = PiFaceController()


class PilotwireSchema(Schema):
    modes = fields.String(required=True)

    @validates('modes')
    def validate_modes(self, value):
        # pylint: disable=no-self-use
        regexp = r'[ACEH]{1,4}'
        if not re.fullmatch(regexp, value):
            raise ValidationError(''.join([
                f"Modes string must match {regexp!r} regular expression, ",
                f"received {value!r}"
            ]))


pilotwire_schema = PilotwireSchema()


class PilotwireAPI(MethodView):
    # pylint: disable=no-self-use

    def get(self):
        result = pilotwire_schema.dump(controller)
        return jsonify(result.data)

    def put(self):
        data, errors = pilotwire_schema.load(request.form)
        if errors:
            return jsonify({'errors': errors}), 400
        controller.modes = data['modes']
        return jsonify({
            'message': "Modes successfully set on pilotwire controller.",
            'modes': controller.modes,
        })


app.add_url_rule('/pilotwire', view_func=PilotwireAPI.as_view('pilotwire'))
