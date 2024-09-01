class MaterialRoll:
    """
    A class representing a roll of material used in the Pick and Place Machine.

    Attributes:
        _material (str): The name of the material.
        _capacity (int): The initial capacity of the material roll.
        _materials_left (int): The amount of material left in the roll.
    """
    
    def __init__(self, material, capacity):
        """
        Initializes a MaterialRoll instance.

        Args:
            material (str): The name of the material.
            capacity (int): The initial capacity of the material roll.

        Attributes:
            _material (str): The name of the material.
            _capacity (int): The capacity of the material roll.
            _materials_left (int): The current amount of material left in the roll, initially set to capacity.
        """
        self._material = material
        self._capacity = capacity
        self._materials_left = capacity

    def get_material(self):
        """
        Retrieves one unit of material from the roll if available.

        Returns:
            str: The name of the material if there is material left; None if the roll is empty.
        """
        if self._materials_left > 0:
            self._materials_left -= 1
            return self._material
        else:
            return None

    def is_empty(self):
        """
        Checks if the material roll is empty.

        Returns:
            bool: True if the roll is empty, False otherwise.
        """
        return self._materials_left == 0