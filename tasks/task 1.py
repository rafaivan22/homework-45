class BaseTeaException(Exception):
    pass

class Sugar:
    def __init__(self, kind):
        self.kind = self.validate_kind(kind)

    @staticmethod
    def validate_kind(kind):
        valid_kinds = {"brown", "white"}
        if kind not in valid_kinds:
            raise ValueError("Invalid sugar type")
        return kind

class Tea:
    def __init__(self, kind):
        self.kind = self.validate_kind(kind)

    @staticmethod
    def validate_kind(kind):
        valid_kinds = {"black", "green"}
        if kind not in valid_kinds:
            raise ValueError("Invalid tea type")
        return kind

class TeaCup:
    def __init__(self):
        self.sweetness = 0
        self.fullness = 0.0
        self.tea = None

    def pour_water(self, amount=None):
        if amount is None:
            amount = 1.0
        elif not isinstance(amount, float) or not (0 <= amount <= 1):
            raise ValueError("Amount must be a float in the range [0, 1]")

        new_fullness = self.fullness + amount
        if new_fullness > 1:
            raise BaseTeaException("Attempt to pour too much water")
        self.fullness = new_fullness

    def drink(self, amount=None):
        if amount is None:
            amount = self.fullness
        elif not isinstance(amount, float) or not (0 <= amount <= 1):
            raise ValueError("Amount must be a float in the range [0, 1]")

        new_fullness = self.fullness - amount
        if new_fullness < 0:
            raise BaseTeaException("Attempt to drink beyond available amount")
        self.fullness = new_fullness

        if self.fullness == 0:
            self.sweetness = 0
            self.tea = None

    def is_full(self):
        return self.fullness == 1.0

    def __add__(self, other):
        if isinstance(other, Sugar):
            self.sweetness += 1
        elif isinstance(other, Tea):
            self.tea = other.kind
        else:
            raise TypeError("Can only add Sugar or Tea to a TeaCup")
        return self

    def __sub__(self, other):
        if isinstance(other, Sugar):
            if self.sweetness <= 0:
                raise ValueError("Amount of sugar can't be negative")
            self.sweetness -= 1
        else:
            raise TypeError("Can only subtract Sugar from TeaCup")
        return self
