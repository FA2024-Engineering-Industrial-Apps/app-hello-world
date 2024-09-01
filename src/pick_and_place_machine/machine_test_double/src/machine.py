import threading
import time
from materialroll import MaterialRoll
from typing import Dict, List, Tuple, Callable

class PickAndPlaceMachine:
    """
    A class representing a Pick and Place Machine used for automated material handling.

    Attributes:
        name (str): The name of the machine.
        _materials (Dict[str, MaterialRoll]): A dictionary storing material names and their corresponding rolls.
        _running (bool): A flag indicating whether the machine is running.
        _thread (threading.Thread): The thread that runs the machine operations.
    """

    def __init__(self, name : str, materials : List[Tuple[str,int]]):
        """
        Initializes a PickAndPlaceMachine instance.

        Args:
            name (str): The name of the machine.
            materials (List[Tuple[str, int]]): A list of tuples where each tuple contains a material name 
                                               and its capacity.

        Attributes:
            _materials (Dict[str, MaterialRoll]): A dictionary initialized with the provided materials and their capacities.
        """
        self.name: str = name
        self._materials: Dict[str, MaterialRoll] = {}
        for material_name, material_capacity in materials:
            self._materials[material_name] = MaterialRoll(material_name,material_capacity)
        self._running: bool = False
        self._thread: threading.Thread = None

    def start(self):
        """
        Starts the machine's operation in a separate thread.
        """
        if not self._running:
            self._running = True
            self._thread = threading.Thread(target=self._run_machine)
            self._thread.start()
            print(f"Started machine: {self.name}...")

    def is_running(self) -> bool:
        """
        Checks if the machine is currently running.

        Returns:
            bool: True if the machine is running, False otherwise.
        """
        return self._running

    def shutdown(self):
        """
        Stops the machine's operation and waits for the thread to finish.
        """
        if self._running:
            self._running = False
            print(f"Stopping machine: {self.name}...")

    def refill_material(self, material : str, capacity : int):
        """
        Refills the specified material roll with the given capacity.

        Args:
            material (str): The name of the material to refill.
            capacity (int): The capacity to refill the material roll with.
        """
        self._materials[material] = MaterialRoll(material, capacity)

    def set_material_used_event_handler(self, event_handler : Callable[[str, int], None]):
        """
        Sets the event handler for when a material is used.

        Args:
            event_handler (Callable[[str, int], None]): A callback function that takes the material name and quantity used.
        """
        self._material_used_event_handler = event_handler

    def set_material_roll_empty_event_handler(self, event_handler : Callable[str, None]):
        """
        Sets the event handler for when a material roll becomes empty.

        Args:
            event_handler (Callable[[str], None]): A callback function that takes the material name of the empty roll.
        """
        self._material_roll_empty_event_handler = event_handler

    def _rolls_not_empty(self) -> bool:
        """
        Checks if all material rolls have materials left.

        Returns:
            bool: True if all rolls have materials, False if any roll is empty.
        """
        result: bool = True
        for roll in self._materials.values():
            result &= not roll.is_empty()
        return result

    def _run_machine(self):
        """
        The internal method that simulates the machine's operation, consuming materials at regular intervals.

        This method runs in a loop while the machine is active and triggers events for material usage and empty rolls.
        """
        while self.is_running():
            time.sleep(5)
            while self._rolls_not_empty() and self.is_running():
                for roll in self._materials.values():
                    current_material = roll.get_material()
                    print(f"Using material {current_material}...")

                    if self._material_used_event_handler != None:
                        self._material_used_event_handler(current_material, 1)
                        
                time.sleep(5)

            if self._material_roll_empty_event_handler != None:
                for material, roll in self._materials.items():
                    if roll.is_empty():
                        print(f"Material roll {material} is empty. Please refill to continue...")
                        self._material_roll_empty_event_handler(material)
        
        print(f"Machine {self.name} stopped...")

    def __repr__(self):
        return f"PickAndPlaceMachine(name='{self.model_name}')"
    
