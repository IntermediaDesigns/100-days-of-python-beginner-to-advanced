from typing import Dict, Set, List, Optional, Tuple
from collections import defaultdict, deque
import json
from datetime import datetime
import networkx as nx
import matplotlib.pyplot as plt


class User:
    def __init__(self, id: str, name: str, interests: List[str] = None):
        self.id = id
        self.name = name
        self.interests = interests or []
        self.join_date = datetime.now()

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "interests": self.interests,
            "join_date": self.join_date.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        user = cls(data["id"], data["name"], data["interests"])
        user.join_date = datetime.fromisoformat(data["join_date"])
        return user


class SocialNetwork:
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.connections: Dict[str, Set[str]] = defaultdict(set)
        self.posts: Dict[str, List[dict]] = defaultdict(list)

    def add_user(self, user: User) -> None:
        if user.id not in self.users:
            self.users[user.id] = user
            self.connections[user.id] = set()

    def add_connection(self, user1_id: str, user2_id: str) -> None:
        if user1_id in self.users and user2_id in self.users:
            self.connections[user1_id].add(user2_id)
            self.connections[user2_id].add(user1_id)

    def remove_connection(self, user1_id: str, user2_id: str) -> None:
        if user1_id in self.users and user2_id in self.users:
            self.connections[user1_id].discard(user2_id)
            self.connections[user2_id].discard(user1_id)

    def add_post(self, user_id: str, content: str, tags: List[str] = None) -> None:
        if user_id in self.users:
            post = {
                "content": content,
                "tags": tags or [],
                "timestamp": datetime.now(),
                "likes": set(),
            }
            self.posts[user_id].append(post)

    def like_post(self, user_id: str, author_id: str, post_index: int) -> None:
        if (
            user_id in self.users
            and author_id in self.users
            and 0 <= post_index < len(self.posts[author_id])
        ):
            self.posts[author_id][post_index]["likes"].add(user_id)

    def get_friends(self, user_id: str) -> Set[str]:
        return self.connections.get(user_id, set())

    def get_mutual_friends(self, user1_id: str, user2_id: str) -> Set[str]:
        friends1 = self.get_friends(user1_id)
        friends2 = self.get_friends(user2_id)
        return friends1.intersection(friends2)

    def get_friend_recommendations(self, user_id: str) -> List[Tuple[str, int]]:
        recommendations = defaultdict(int)
        friends = self.get_friends(user_id)

        # Friends of friends get higher weight
        for friend in friends:
            for friend_of_friend in self.get_friends(friend):
                if friend_of_friend != user_id and friend_of_friend not in friends:
                    recommendations[friend_of_friend] += 1

        # Common interests increase recommendation weight
        user_interests = set(self.users[user_id].interests)
        for potential_friend, score in recommendations.items():
            common_interests = len(
                user_interests.intersection(self.users[potential_friend].interests)
            )
            recommendations[potential_friend] += common_interests * 0.5

        return sorted(recommendations.items(), key=lambda x: (-x[1], x[0]))

    def get_shortest_path(self, start_id: str, end_id: str) -> Optional[List[str]]:
        if start_id not in self.users or end_id not in self.users:
            return None

        visited = {start_id}
        queue = deque([(start_id, [start_id])])

        while queue:
            current_id, path = queue.popleft()
            for neighbor in self.connections[current_id]:
                if neighbor == end_id:
                    return path + [neighbor]
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        return None

    def get_connection_strength(self, user1_id: str, user2_id: str) -> float:
        if user1_id not in self.users or user2_id not in self.users:
            return 0.0

        score = 0.0

        # Direct connection
        if user2_id in self.connections[user1_id]:
            score += 1.0

        # Mutual friends
        mutual_friends = len(self.get_mutual_friends(user1_id, user2_id))
        score += mutual_friends * 0.2

        # Common interests
        common_interests = len(
            set(self.users[user1_id].interests).intersection(
                self.users[user2_id].interests
            )
        )
        score += common_interests * 0.1

        # Interactions (likes)
        user1_likes = sum(
            1 for post in self.posts[user2_id] if user1_id in post["likes"]
        )
        user2_likes = sum(
            1 for post in self.posts[user1_id] if user2_id in post["likes"]
        )
        score += (user1_likes + user2_likes) * 0.05

        return score

    def get_network_stats(self) -> dict:
        total_users = len(self.users)
        total_connections = (
            sum(len(connections) for connections in self.connections.values()) // 2
        )
        avg_connections = total_connections * 2 / total_users if total_users > 0 else 0

        return {
            "total_users": total_users,
            "total_connections": total_connections,
            "average_connections": avg_connections,
            "total_posts": sum(len(posts) for posts in self.posts.values()),
            "most_connected": (
                max(self.connections.items(), key=lambda x: len(x[1]))[0]
                if self.users
                else None
            ),
        }

    def visualize_network(self, filename: str = None) -> None:
        G = nx.Graph()

        # Add nodes
        for user_id, user in self.users.items():
            G.add_node(user_id, name=user.name)

        # Add edges
        for user_id, connections in self.connections.items():
            for connection in connections:
                G.add_edge(user_id, connection)

        # Draw the network
        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(G)
        nx.draw(
            G,
            pos,
            with_labels=True,
            node_color="lightblue",
            node_size=500,
            font_size=8,
            labels={node: G.nodes[node]["name"] for node in G.nodes()},
        )

        if filename:
            plt.savefig(filename)
        else:
            plt.show()

    def save_to_file(self, filename: str) -> None:
        data = {
            "users": {uid: user.to_dict() for uid, user in self.users.items()},
            "connections": {
                uid: list(connections) for uid, connections in self.connections.items()
            },
            "posts": {
                uid: [
                    {
                        **post,
                        "likes": list(post["likes"]),
                        "timestamp": post["timestamp"].isoformat(),
                    }
                    for post in user_posts
                ]
                for uid, user_posts in self.posts.items()
            },
        }

        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

    def load_from_file(self, filename: str) -> None:
        with open(filename, "r") as f:
            data = json.load(f)

        self.users = {
            uid: User.from_dict(user_data) for uid, user_data in data["users"].items()
        }
        self.connections = {
            uid: set(connections) for uid, connections in data["connections"].items()
        }
        self.posts = {
            uid: [
                {
                    **post,
                    "likes": set(post["likes"]),
                    "timestamp": datetime.fromisoformat(post["timestamp"]),
                }
                for post in user_posts
            ]
            for uid, user_posts in data["posts"].items()
        }


def main():
    network = SocialNetwork()

    while True:
        print("\nSocial Network Analyzer")
        print("1. Add User")
        print("2. Add Connection")
        print("3. Add Post")
        print("4. Like Post")
        print("5. View Friend Recommendations")
        print("6. Find Connection Path")
        print("7. View Network Stats")
        print("8. Visualize Network")
        print("9. Save Network")
        print("10. Load Network")
        print("11. Exit")

        choice = input("\nEnter choice (1-11): ")

        try:
            if choice == "1":
                id = input("Enter user ID: ")
                name = input("Enter name: ")
                interests = input("Enter interests (comma-separated): ").split(",")
                interests = [i.strip() for i in interests if i.strip()]
                user = User(id, name, interests)
                network.add_user(user)
                print("User added successfully!")

            elif choice == "2":
                user1_id = input("Enter first user ID: ")
                user2_id = input("Enter second user ID: ")
                network.add_connection(user1_id, user2_id)
                print("Connection added successfully!")

            elif choice == "3":
                user_id = input("Enter user ID: ")
                content = input("Enter post content: ")
                tags = input("Enter tags (comma-separated): ").split(",")
                tags = [t.strip() for t in tags if t.strip()]
                network.add_post(user_id, content, tags)
                print("Post added successfully!")

            elif choice == "4":
                user_id = input("Enter user ID: ")
                author_id = input("Enter post author ID: ")
                post_index = int(input("Enter post index: "))
                network.like_post(user_id, author_id, post_index)
                print("Post liked successfully!")

            elif choice == "5":
                user_id = input("Enter user ID: ")
                recommendations = network.get_friend_recommendations(user_id)
                print("\nFriend Recommendations:")
                for user_id, score in recommendations[:5]:
                    user = network.users[user_id]
                    print(f"{user.name} (Score: {score:.2f})")

            elif choice == "6":
                start_id = input("Enter start user ID: ")
                end_id = input("Enter end user ID: ")
                path = network.get_shortest_path(start_id, end_id)
                if path:
                    names = [network.users[uid].name for uid in path]
                    print(" -> ".join(names))
                else:
                    print("No connection path found!")

            elif choice == "7":
                stats = network.get_network_stats()
                print("\nNetwork Statistics:")
                for key, value in stats.items():
                    print(f"{key.replace('_', ' ').title()}: {value}")

            elif choice == "8":
                filename = input(
                    "Enter filename to save visualization (or press Enter for display): "
                )
                network.visualize_network(filename if filename else None)

            elif choice == "9":
                filename = input("Enter filename to save: ")
                network.save_to_file(filename)
                print("Network saved successfully!")

            elif choice == "10":
                filename = input("Enter filename to load: ")
                network.load_from_file(filename)
                print("Network loaded successfully!")

            elif choice == "11":
                print("Goodbye!")
                break

        except Exception as e:
            print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
