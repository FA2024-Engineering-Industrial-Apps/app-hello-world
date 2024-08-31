class MaterialRoll:
    def __init__(self, material, capacity):
        self._material = material
        self._capacity = capacity
        self._materials_left = capacity

    def get_material(self):
        if self._materials_left > 0:
            self._materials_left -= 1
            return self._material
        else:
            return None

    def is_empty(self):
        return self._materials_left == 0