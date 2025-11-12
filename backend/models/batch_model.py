class Batch:
    def __init__(self, name, origin, tracking_history=None):
        """
        Initializes a new batch of boba ingredients.

        :param name: The name of the boba ingredient batch.
        :param origin: The origin of the boba ingredient.
        :param tracking_history: A list of tracking steps for the batch (default is empty).
        """
        self.name = name
        self.origin = origin
        self.tracking_history = tracking_history if tracking_history is not None else []

    def add_tracking_step(self, step):
        """
        Adds a tracking step to the batch's tracking history.

        :param step: A description of the tracking step to be added.
        """
        self.tracking_history.append(step)

    def get_tracking_history(self):
        """
        Returns the tracking history of the batch.

        :return: A list of tracking steps.
        """
        return self.tracking_history

    def __repr__(self):
        """
        Returns a string representation of the batch.

        :return: A string describing the batch.
        """
        return f"Batch(name={self.name}, origin={self.origin}, tracking_history={self.tracking_history})"