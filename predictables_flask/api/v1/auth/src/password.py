from flask import jsonify


def reset():
    # POST to reset password
    return jsonify({"message": "Password reset endpoint not implemented"}), 501


def reset_confirm():
    # POST to confirm password reset
    return jsonify({"message": "Password reset confirm endpoint not implemented"}), 501


def change():
    # POST to change password
    return jsonify({"message": "Password change endpoint not implemented"}), 501


def change_confirm():
    # POST to confirm password change
    return jsonify({"message": "Password change confirm endpoint not implemented"}), 501


def reset_validate():
    # POST to validate password reset token
    return jsonify({"message": "Password reset validate endpoint not implemented"}), 501


def change_validate():
    # POST to validate password change token
    return (
        jsonify({"message": "Password change validate endpoint not implemented"}),
        501,
    )
