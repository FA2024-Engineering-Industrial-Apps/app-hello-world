import threading
import time
from materialroll import MaterialRoll
from typing import Dict, List, Tuple, Callable

class PickAndPlaceMachine:
    def __init__(self, name : str, materials : List[Tuple[str,int]]):
        self.name: str = name
        self._materials: Dict[str, MaterialRoll] = {}
        for material_name, material_capacity in materials:
            self._materials[material_name] = MaterialRoll(material_name,material_capacity)
        self._running: bool = False
        self._thread: threading.Thread = None

    def start(self):
        if not self._running:
            self._running = True
            self._thread = threading.Thread(target=self._run_machine)
            self._thread.start()
            print(f"Started machine: {self.name}...")

    def is_running(self) -> bool:
        return self._running

    def shutdown(self):
        if self._running:
            self._running = False
            self._thread.join()
            print(f"Stopped machine: {self.name}...")

    def refill_material(self, material : str, capacity : int):
        self._materials[material] = MaterialRoll(material, capacity)

    def set_material_used_event_handler(self, event_handler : Callable[[str, int], None]):
        self._material_used_event_handler = event_handler

    def set_material_roll_empty_event_handler(self, event_handler : Callable[str, None]):
        self._material_roll_empty_event_handler = event_handler

    def _rolls_not_empty(self) -> bool:
        result: bool = True
        for roll in self._materials.values():
            result &= not roll.is_empty()
        return result

    def _run_machine(self):
        while self._running:
            time.sleep(5)
            while self._rolls_not_empty():
                for roll in self._materials.values():
                    current_material = roll.get_material()
                    print(f"Using material {current_material}...")

                    if self._material_used_event_handler != None:
                        self._material_used_event_handler(current_material, 1)

            if self._material_roll_empty_event_handler != None:
                for material, roll in self._materials:
                    if roll.is_empty():
                        print(f"Material roll {material} is empty. Please refill to continue...")
                        self._material_roll_empty_event_handler(material)

    def __repr__(self):
        return f"PickAndPlaceMachine(name='{self.model_name}')"
    
