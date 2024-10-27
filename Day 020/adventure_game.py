import json
import random
import time
from typing import List, Dict, Any
import os
from datetime import datetime


class Item:
    def __init__(self, name: str, description: str, power: int = 0):
        self.name = name
        self.description = description
        self.power = power

    def __str__(self):
        return f"{self.name}: {self.description} (Power: {self.power})"

    def to_dict(self) -> Dict[str, Any]:
        return {"name": self.name, "description": self.description, "power": self.power}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Item":
        return cls(**data)


class Character:
    def __init__(self, name: str, health: int = 100):
        self.name = name
        self.health = health
        self.inventory: List[Item] = []
        self.max_health = health

    def add_item(self, item: Item):
        self.inventory.append(item)

    def remove_item(self, item: Item):
        self.inventory.remove(item)

    def get_power(self) -> int:
        return sum(item.power for item in self.inventory)

    def heal(self, amount: int):
        self.health = min(self.health + amount, self.max_health)

    def take_damage(self, amount: int):
        self.health = max(0, self.health - amount)

    def is_alive(self) -> bool:
        return self.health > 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "health": self.health,
            "inventory": [item.to_dict() for item in self.inventory],
            "max_health": self.max_health,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Character":
        character = cls(data["name"], data["health"])
        character.max_health = data["max_health"]
        character.inventory = [
            Item.from_dict(item_data) for item_data in data["inventory"]
        ]
        return character


class Enemy(Character):
    def __init__(self, name: str, health: int, damage: int):
        super().__init__(name, health)
        self.damage = damage

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data["damage"] = self.damage
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Enemy":
        enemy = cls(data["name"], data["health"], data["damage"])
        enemy.inventory = [Item.from_dict(item_data) for item_data in data["inventory"]]
        return enemy


class Room:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.items: List[Item] = []
        self.enemies: List[Enemy] = []
        self.connections: Dict[str, "Room"] = {}

    def add_connection(self, direction: str, room: "Room"):
        self.connections[direction] = room

    def get_available_directions(self) -> List[str]:
        return list(self.connections.keys())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "items": [item.to_dict() for item in self.items],
            "enemies": [enemy.to_dict() for enemy in self.enemies],
        }


class Game:
    def __init__(self):
        self.player = None
        self.current_room = None
        self.rooms: List[Room] = []
        self.setup_game()

    def setup_game(self):
        # Create items
        sword = Item("Sword", "A sharp blade", 10)
        shield = Item("Shield", "A sturdy shield", 5)
        potion = Item("Health Potion", "Restores 30 health", 0)

        # Create rooms
        entrance = Room(
            "Entrance", "You stand at the entrance of a mysterious dungeon."
        )
        hall = Room("Great Hall", "A vast hall with ancient pillars.")
        treasury = Room("Treasury", "A room filled with treasures and dangers.")

        # Setup connections
        entrance.add_connection("north", hall)
        hall.add_connection("south", entrance)
        hall.add_connection("east", treasury)
        treasury.add_connection("west", hall)

        # Add items to rooms
        entrance.items.append(shield)
        hall.items.append(sword)
        treasury.items.append(potion)

        # Add enemies
        goblin = Enemy("Goblin", 30, 5)
        dragon = Enemy("Dragon", 100, 20)
        hall.enemies.append(goblin)
        treasury.enemies.append(dragon)

        self.rooms = [entrance, hall, treasury]
        self.current_room = entrance

    def start_game(self):
        print("Welcome to the Text Adventure Game!")
        player_name = input("Enter your character's name: ")
        self.player = Character(player_name)
        self.game_loop()

    def save_game(self):
        save_data = {
            "player": self.player.to_dict(),
            "current_room": self.current_room.name,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        filename = f"save_{self.player.name}_{int(time.time())}.json"
        with open(filename, "w") as f:
            json.dump(save_data, f, indent=4)
        print(f"Game saved as {filename}")

    def load_game(self, filename: str):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
                self.player = Character.from_dict(data["player"])
                self.current_room = next(
                    room for room in self.rooms if room.name == data["current_room"]
                )
                print(f"Game loaded from {filename}")
        except FileNotFoundError:
            print("Save file not found.")
        except json.JSONDecodeError:
            print("Invalid save file.")

    def handle_combat(self, enemy: Enemy):
        print(f"\nA {enemy.name} appears!")

        while enemy.is_alive() and self.player.is_alive():
            print(f"\nYour Health: {self.player.health}")
            print(f"{enemy.name}'s Health: {enemy.health}")

            action = input("\nWhat do you do? (attack/run): ").lower()

            if action == "attack":
                damage = self.player.get_power()
                enemy.take_damage(damage)
                print(f"You deal {damage} damage to {enemy.name}")

                if enemy.is_alive():
                    self.player.take_damage(enemy.damage)
                    print(f"{enemy.name} deals {enemy.damage} damage to you")
            elif action == "run":
                if random.random() > 0.5:
                    print("You successfully run away!")
                    return True
                else:
                    print("You fail to run away!")
                    self.player.take_damage(enemy.damage)

            if not self.player.is_alive():
                print("You have been defeated!")
                return False

        if enemy.is_alive():
            return False
        else:
            print(f"You defeated the {enemy.name}!")
            return True

    def game_loop(self):
        while self.player.is_alive():
            print(f"\nLocation: {self.current_room.name}")
            print(self.current_room.description)

            # Show available directions
            print(
                "\nAvailable directions:",
                ", ".join(self.current_room.get_available_directions()),
            )

            # Show items in room
            if self.current_room.items:
                print("\nItems in room:")
                for item in self.current_room.items:
                    print(f"- {item}")

            # Show enemies
            if self.current_room.enemies:
                print("\nEnemies present:")
                for enemy in self.current_room.enemies:
                    print(f"- {enemy.name} (Health: {enemy.health})")

            # Show player status
            print(f"\nYour Status:")
            print(f"Health: {self.player.health}")
            print("Inventory:")
            for item in self.player.inventory:
                print(f"- {item}")

            # Get player action
            action = input(
                "\nWhat would you like to do? (move/take/use/save/load/quit): "
            ).lower()
            print()

            if action == "move":
                direction = input("Which direction? ").lower()
                if direction in self.current_room.connections:
                    # Check for enemies blocking the way
                    if self.current_room.enemies:
                        print("You must defeat the enemies first!")
                        continue

                    self.current_room = self.current_room.connections[direction]
                else:
                    print("You can't go that way!")

            elif action == "take":
                if not self.current_room.items:
                    print("No items to take!")
                    continue

                print("Available items:")
                for i, item in enumerate(self.current_room.items):
                    print(f"{i+1}. {item}")

                try:
                    item_index = (
                        int(input("Enter item number to take (0 to cancel): ")) - 1
                    )
                    if 0 <= item_index < len(self.current_room.items):
                        item = self.current_room.items.pop(item_index)
                        self.player.add_item(item)
                        print(f"Took {item.name}")
                except ValueError:
                    print("Invalid input!")

            elif action == "use":
                if not self.player.inventory:
                    print("No items to use!")
                    continue

                print("Your items:")
                for i, item in enumerate(self.player.inventory):
                    print(f"{i+1}. {item}")

                try:
                    item_index = (
                        int(input("Enter item number to use (0 to cancel): ")) - 1
                    )
                    if 0 <= item_index < len(self.player.inventory):
                        item = self.player.inventory[item_index]
                        if item.name == "Health Potion":
                            self.player.heal(30)
                            self.player.remove_item(item)
                            print("You used the health potion and restored 30 health!")
                except ValueError:
                    print("Invalid input!")

            elif action == "save":
                self.save_game()

            elif action == "load":
                filename = input("Enter save file name: ")
                self.load_game(filename)

            elif action == "quit":
                save = input("Would you like to save first? (y/n): ").lower()
                if save == "y":
                    self.save_game()
                print("Thanks for playing!")
                break

            # Handle enemy encounters
            if self.current_room.enemies:
                enemy = self.current_room.enemies[0]
                survived = self.handle_combat(enemy)
                if survived:
                    if not enemy.is_alive():
                        self.current_room.enemies.remove(enemy)
                else:
                    print("Game Over!")
                    break


def main():
    game = Game()
    while True:
        print("\nText Adventure Game")
        print("1. New Game")
        print("2. Load Game")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            game.start_game()
        elif choice == "2":
            save_files = [
                f
                for f in os.listdir(".")
                if f.startswith("save_") and f.endswith(".json")
            ]
            if save_files:
                print("\nAvailable save files:")
                for i, file in enumerate(save_files):
                    print(f"{i+1}. {file}")
                try:
                    file_index = int(input("Enter save file number: ")) - 1
                    if 0 <= file_index < len(save_files):
                        game.load_game(save_files[file_index])
                        game.game_loop()
                except ValueError:
                    print("Invalid input!")
            else:
                print("No save files found!")
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()
