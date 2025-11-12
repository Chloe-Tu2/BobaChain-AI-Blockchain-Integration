def format_boba_data(data):
    """
    Formats the raw boba data into a more readable structure.

    Parameters:
    data (dict): The raw data containing boba ingredient information.

    Returns:
    str: A formatted string summarizing the boba ingredient details.
    """
    formatted_data = f"Boba Ingredient: {data.get('name')}\n"
    formatted_data += f"Origin: {data.get('origin')}\n"
    formatted_data += f"Tracking History: {', '.join(data.get('tracking_history', []))}\n"
    return formatted_data


def validate_boba_data(data):
    """
    Validates the boba data to ensure all required fields are present.

    Parameters:
    data (dict): The raw data containing boba ingredient information.

    Returns:
    bool: True if data is valid, False otherwise.
    """
    required_fields = ['name', 'origin', 'tracking_history']
    return all(field in data for field in required_fields)