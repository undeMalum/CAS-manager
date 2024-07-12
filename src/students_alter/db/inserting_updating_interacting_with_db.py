def manage_interaction_with_db(class_to_be_called, parameters_to_be_used) -> (str, str):
    """Handles interaction with database. It creates an objects and then alters db with it."""

    try:
        object_altering_db = class_to_be_called(*parameters_to_be_used)
    except ValueError as exc:
        return "Error", str(exc)
    else:
        object_altering_db.alter()
        return "Completed!", "Operation completed successfully!"
