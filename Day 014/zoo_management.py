from abc import ABC, abstractmethod


class Animal(ABC):
    def __init__(self, name, age, species, diet):
        self.name = name
        self.age = age
        self.species = species
        self.diet = diet
        self.health = 100

    @abstractmethod
    def make_sound(self):
        pass

    def eat(self, food):
        if food in self.diet:
            print(f"{self.name} the {self.species} is eating {food}")
            self.health += 10
            if self.health > 100:
                self.health = 100
        else:
            print(f"{self.name} the {self.species} doesn't eat {food}")

    def check_health(self):
        print(f"{self.name} the {self.species} has {self.health} health")


class Mammal(Animal):
    def __init__(self, name, age, species, diet, fur_color):
        super().__init__(name, age, species, diet)
        self.fur_color = fur_color

    def groom(self):
        print(f"{self.name} the {self.species} is grooming its {self.fur_color} fur")
        self.health += 5
        if self.health > 100:
            self.health = 100


class Bird(Animal):
    def __init__(self, name, age, species, diet, wingspan):
        super().__init__(name, age, species, diet)
        self.wingspan = wingspan

    def fly(self):
        print(
            f"{self.name} the {self.species} is flying with a wingspan of {self.wingspan} inches"
        )
        self.health += 5
        if self.health < 0:
            self.health = 0


class Reptile(Animal):
    def __init__(self, name, age, species, diet, length):
        super().__init__(name, age, species, diet)
        self.is_venoumos = is_venoumos

    def bask(self):
        print(f"{self.name} the {self.species} is basking in the sun")
        self.health += 5
        if self.health > 100:
            self.health = 100


class Lion(Mammal):
    def __init__(self, name, age):
        super().__init__(name, age, "Lion", ["meat"], "golden")

    def make_sound(self):
        print("Roar!")


class Parrot(Bird):
    def __init__(self, name, age):
        super().__init__(name, age, "Parrot", ["seeds", "fruit"], 20)

    def make_sound(self):
        return "Squawk!"

    def mimic(self, sound):
        print(f"{self.name} the Parrot is mimicking {sound}")


class Snake(Reptile):
    def __init__(self, name, age, is_venomous):
        super().__init__(name, age, "Snake", ["rodents"], is_venomous)

    def make_sound(self):
        return "Hiss!"


class Zoo:
    def __init__(self, name):
        self.name = name
        self.animals = []

    def add_animal(self, animal):
        self.animals.append(animal)
        print(f"{animal.name} the {animal.species} has been added to {self.name}")

    def remove_animal(self, animal):
        if animal in self.animals:
            self.animals.remove(animal)
            print(
                f"{animal.name} the {animal.species} has been removed from {self.name}"
            )
        else:
            print(f"{animal.name} the {animal.species} is not in {self.name}")

    def feed_animals(self, food):
        for animal in self.animals:
            animal.eat(food)

    def zoo_sounds(self):
        for animal in self.animals:
            print(f"{animal.name} the {animal.species} says {animal.make_sound()}")

    def check_health(self):
        for animal in self.animals:
            animal.check_health()


def main():
    zoo = Zoo("PyZoo")

    while True:
        print("\nPyZoo Management System")
        print("1. Add an animal")
        print("2. Remove an animal")
        print("3. Feed animals")
        print("4. Listen to zoo sounds")
        print("5. Check animals' health")
        print("6. Perform special action")
        print("7. Exit")
        print()

        choice = input("Enter your choice: ")

        if choice == "1":
            animal_type = input(
                "Enter the type of animal (Lion, Parrot, Snake): "
            ).lower()
            name = input("Enter the name of the animal: ")
            age = int(input("Enter the age of the animal: "))

            if animal_type == "lion":
                lion = Lion(name, age)
                zoo.add_animal(lion)

            elif animal_type == "parrot":
                parrot = Parrot(name, age)
                zoo.add_animal(parrot)

            elif animal_type == "snake":
                is_venomous = input("Is the snake venomous (yes/no): ").lower()
                snake = Snake(name, age, is_venomous == "yes")
                zoo.add_animal(snake)

            else:
                print("Invalid animal type")
                continue

        elif choice == "2":
            name = input("Enter the name of the animal to remove: ")
            animal_to_remove = next(
                (animal for animal in zoo.animals if animal.name == name), None
            )
            if animal_to_remove:
                zoo.remove_animal(animal_to_remove)
            else:
                print(f"{name} is not in the zoo")

        elif choice == "3":
            food = input("Enter the food to feed the animals: ")
            zoo.feed_animals(food)

        elif choice == "4":
            zoo.zoo_sounds()

        elif choice == "5":
            zoo.check_health()

        elif choice == "6":
            name = input("Enter the name of the animal to perform the special action: ")
            animal = next(
                (animal for animal in zoo.animals if animal.name == name), None
            )
            if animal:
                if isinstance(animal, Mammal):
                    animal.groom()
                elif isinstance(animal, Bird):
                    animal.fly()
                elif isinstance(animal, Reptile):
                    animal.bask()
                if isinstance(animal, Parrot):
                    sound = input("Enter a sound for the parrot to mimic: ")
                    animal.mimic(sound)
            else:
                print(f"{name} is not in the zoo")

        elif choice == "7":
            print("Exiting PyZoo Management System")
            break

        else:
            print("Invalid choice, please try again")


if __name__ == "__main__":
    main()
