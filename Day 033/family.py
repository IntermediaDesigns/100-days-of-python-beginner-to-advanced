from dataclasses import dataclass, asdict
from typing import List, Optional, Dict
from datetime import datetime
import json
from enum import Enum


class Gender(Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class RelationType(Enum):
    PARENT = "parent"
    CHILD = "child"
    SPOUSE = "spouse"
    SIBLING = "sibling"


@dataclass
class Person:
    id: str
    name: str
    birth_date: datetime
    gender: Gender
    death_date: Optional[datetime] = None
    birth_place: Optional[str] = None
    occupation: Optional[str] = None
    notes: Optional[str] = None

    def to_dict(self) -> Dict:
        data = asdict(self)
        data["birth_date"] = self.birth_date.isoformat()
        data["death_date"] = self.death_date.isoformat() if self.death_date else None
        data["gender"] = self.gender.value
        return data

    @classmethod
    def from_dict(cls, data: Dict) -> "Person":
        data["birth_date"] = datetime.fromisoformat(data["birth_date"])
        if data["death_date"]:
            data["death_date"] = datetime.fromisoformat(data["death_date"])
        data["gender"] = Gender(data["gender"])
        return cls(**data)


class FamilyTreeNode:
    def __init__(self, person: Person):
        self.person = person
        self.parents: List[FamilyTreeNode] = []
        self.children: List[FamilyTreeNode] = []
        self.spouses: List[FamilyTreeNode] = []
        self.siblings: List[FamilyTreeNode] = []


class FamilyTree:
    def __init__(self):
        self.nodes: Dict[str, FamilyTreeNode] = {}
        self.root: Optional[FamilyTreeNode] = None

    def add_person(self, person: Person) -> None:
        if person.id not in self.nodes:
            node = FamilyTreeNode(person)
            self.nodes[person.id] = node
            if not self.root:
                self.root = node

    def add_relation(
        self, person1_id: str, person2_id: str, relation: RelationType
    ) -> None:
        if person1_id not in self.nodes or person2_id not in self.nodes:
            raise ValueError("Person not found in family tree")

        node1 = self.nodes[person1_id]
        node2 = self.nodes[person2_id]

        if relation == RelationType.PARENT:
            if node2 not in node1.parents and len(node1.parents) < 2:
                node1.parents.append(node2)
                node2.children.append(node1)
        elif relation == RelationType.SPOUSE:
            if node2 not in node1.spouses:
                node1.spouses.append(node2)
                node2.spouses.append(node1)
        elif relation == RelationType.SIBLING:
            if node2 not in node1.siblings:
                node1.siblings.append(node2)
                node2.siblings.append(node1)

    def get_ancestors(
        self, person_id: str, max_generations: int = None
    ) -> List[Person]:
        if person_id not in self.nodes:
            return []

        ancestors = []

        def traverse(node: FamilyTreeNode, generation: int = 0):
            if max_generations and generation >= max_generations:
                return
            for parent in node.parents:
                ancestors.append(parent.person)
                traverse(parent, generation + 1)

        traverse(self.nodes[person_id])
        return ancestors

    def get_descendants(
        self, person_id: str, max_generations: int = None
    ) -> List[Person]:
        if person_id not in self.nodes:
            return []

        descendants = []

        def traverse(node: FamilyTreeNode, generation: int = 0):
            if max_generations and generation >= max_generations:
                return
            for child in node.children:
                descendants.append(child.person)
                traverse(child, generation + 1)

        traverse(self.nodes[person_id])
        return descendants

    def find_relationship_path(
        self, person1_id: str, person2_id: str
    ) -> List[tuple[RelationType, Person]]:
        if person1_id not in self.nodes or person2_id not in self.nodes:
            return []

        visited = set()
        path = []

        def dfs(current_id: str, target_id: str) -> bool:
            if current_id == target_id:
                return True

            if current_id in visited:
                return False

            visited.add(current_id)
            current = self.nodes[current_id]

            # Check parents
            for parent in current.parents:
                path.append((RelationType.PARENT, parent.person))
                if dfs(parent.person.id, target_id):
                    return True
                path.pop()

            # Check children
            for child in current.children:
                path.append((RelationType.CHILD, child.person))
                if dfs(child.person.id, target_id):
                    return True
                path.pop()

            # Check spouses
            for spouse in current.spouses:
                path.append((RelationType.SPOUSE, spouse.person))
                if dfs(spouse.person.id, target_id):
                    return True
                path.pop()

            # Check siblings
            for sibling in current.siblings:
                path.append((RelationType.SIBLING, sibling.person))
                if dfs(sibling.person.id, target_id):
                    return True
                path.pop()

            return False

        dfs(person1_id, person2_id)
        return path

    def save_to_file(self, filename: str) -> None:
        data = {
            "people": [node.person.to_dict() for node in self.nodes.values()],
            "relations": [],
        }

        for node in self.nodes.values():
            person_id = node.person.id
            for parent in node.parents:
                data["relations"].append(
                    {
                        "person1": person_id,
                        "person2": parent.person.id,
                        "type": RelationType.PARENT.value,
                    }
                )
            for spouse in node.spouses:
                if person_id < spouse.person.id:  # Avoid duplicates
                    data["relations"].append(
                        {
                            "person1": person_id,
                            "person2": spouse.person.id,
                            "type": RelationType.SPOUSE.value,
                        }
                    )
            for sibling in node.siblings:
                if person_id < sibling.person.id:  # Avoid duplicates
                    data["relations"].append(
                        {
                            "person1": person_id,
                            "person2": sibling.person.id,
                            "type": RelationType.SIBLING.value,
                        }
                    )

        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

    def load_from_file(self, filename: str) -> None:
        with open(filename, "r") as f:
            data = json.load(f)

        self.nodes.clear()
        self.root = None

        # First, create all people
        for person_data in data["people"]:
            person = Person.from_dict(person_data)
            self.add_person(person)

        # Then, establish all relationships
        for relation in data["relations"]:
            self.add_relation(
                relation["person1"], relation["person2"], RelationType(relation["type"])
            )


def main():
    family_tree = FamilyTree()

    while True:
        print("\nFamily Tree Creator")
        print("1. Add Person")
        print("2. Add Relationship")
        print("3. View Ancestors")
        print("4. View Descendants")
        print("5. Find Relationship Path")
        print("6. Save Family Tree")
        print("7. Load Family Tree")
        print("8. Exit")

        choice = input("\nEnter choice (1-8): ")

        try:
            if choice == "1":
                id = input("Enter person ID: ")
                name = input("Enter name: ")
                birth_date = datetime.strptime(
                    input("Enter birth date (YYYY-MM-DD): "), "%Y-%m-%d"
                )
                gender = Gender(input("Enter gender (male/female/other): ").lower())

                death_date_str = input(
                    "Enter death date (YYYY-MM-DD) or press Enter to skip: "
                )
                death_date = (
                    datetime.strptime(death_date_str, "%Y-%m-%d")
                    if death_date_str
                    else None
                )

                birth_place = input("Enter birth place (optional): ") or None
                occupation = input("Enter occupation (optional): ") or None
                notes = input("Enter notes (optional): ") or None

                person = Person(
                    id,
                    name,
                    birth_date,
                    gender,
                    death_date,
                    birth_place,
                    occupation,
                    notes,
                )
                family_tree.add_person(person)
                print("Person added successfully!")

            elif choice == "2":
                person1_id = input("Enter first person ID: ")
                person2_id = input("Enter second person ID: ")
                relation_type = RelationType(
                    input("Enter relationship type (parent/spouse/sibling): ").lower()
                )

                family_tree.add_relation(person1_id, person2_id, relation_type)
                print("Relationship added successfully!")

            elif choice == "3":
                person_id = input("Enter person ID: ")
                generations = input("Enter maximum generations (press Enter for all): ")
                max_gen = int(generations) if generations else None

                ancestors = family_tree.get_ancestors(person_id, max_gen)
                print("\nAncestors:")
                for ancestor in ancestors:
                    print(f"{ancestor.name} (ID: {ancestor.id})")

            elif choice == "4":
                person_id = input("Enter person ID: ")
                generations = input("Enter maximum generations (press Enter for all): ")
                max_gen = int(generations) if generations else None

                descendants = family_tree.get_descendants(person_id, max_gen)
                print("\nDescendants:")
                for descendant in descendants:
                    print(f"{descendant.name} (ID: {descendant.id})")

            elif choice == "5":
                person1_id = input("Enter first person ID: ")
                person2_id = input("Enter second person ID: ")

                path = family_tree.find_relationship_path(person1_id, person2_id)
                if path:
                    print("\nRelationship Path:")
                    for relation, person in path:
                        print(f"→ {relation.value} of {person.name}")
                else:
                    print("No relationship path found.")

            elif choice == "6":
                filename = input("Enter filename to save: ")
                family_tree.save_to_file(filename)
                print("Family tree saved successfully!")

            elif choice == "7":
                filename = input("Enter filename to load: ")
                family_tree.load_from_file(filename)
                print("Family tree loaded successfully!")

            elif choice == "8":
                print("Goodbye!")
                break

        except Exception as e:
            print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
