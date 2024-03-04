from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Type


class Roles(Enum):
    """
    Enum to define role types of Nodes in a distributed network.
    """
    ENCRYPTER = "encrypter"
    SENDER = "sender"
    RECEIVER = "receiver"
    WORD_GENERATOR = "word_generator"


class AbstractNode(ABC):
    """
    Abstract base class for a node in a distributed network.
    """

    @abstractmethod
    def __init__(self, identifier: int, role: Roles): ...

    @abstractmethod
    def connect(self, node: Type['AbstractNode']): ...

    @abstractmethod
    def send_message(self, message: str, sender: Type['AbstractNode']): ...

    @abstractmethod
    def set_role(self, role: Roles): ...


class Node(AbstractNode):
    """
    Concrete class representing a node in a network.
    Inherits from "AbstractNode" class.
    """

    def __init__(self, identifier: int, role: Roles):
        """
        Initialize the instance with specified identifier and role.

        :param identifier: Int. A unique identifier for the Node.
        :param role: Enum. Role of the Node.
        """
        self.id = identifier
        self.peers: List[Type['AbstractNode']] = []  # List of connected nodes (peers)
        self.role = role  # Role of the Node

    def connect(self, node: Type['AbstractNode']):
        """
        Establish a connection with another Node.

        :param node: AbstractNode. The Node to establish a connection with.
        """
        if node not in self.peers:
            self.peers.append(node)
            node.connect(self)  # Establish a two-way connection

    def send_message(self, message: str, sender: Type['AbstractNode']):
        """
        Sends a message to all connected nodes except the sender.

        :param message: Str. The message to be sent.
        :param sender: AbstractNode. The Node sending the message.
        """

        for peer in self.peers:

            if peer.role == Roles.RECEIVER:
                peer.receive_message(message, sender)

            elif peer is not self:  # Send message to all peers except the sender
                peer.send_message(message, self)

    def set_role(self, role: Roles):
        """
        Assigns a new role to this Node.

        :param role: Roles. The new role to be assigned.
        """

        if self.role == Roles.WORD_GENERATOR:
            raise ValueError("WordGenerator role cannot be changed.")

        self.role = role

    def __str__(self):
        """
        Returns a string representation of Node.
        """
        return str(f'Node id={self.id}, Role={self.role.value}')


class Encrypter(Node):
    """
    Class representing a Encrypter node in a network.
    Inherits from "Node" class.
    """

    def __init__(self, identifier: int):
        super().__init__(identifier, Roles.ENCRYPTER)

    def encrypt_message(self, message: str) -> str:
        """
        Method definition for encrypting a message.

        :param message: str. The message to be encrypted.
        """
        pass


class Sender(Node):
    """
    Class representing a Sender node in a network.
    Inherits from "Node" class.
    """

    def __init__(self, identifier: int):
        super().__init__(identifier, Roles.SENDER)

    def initiate_message(self, message: str):
        """
        Method definition for initiating a message.

        :param message: str. The message to be initiated.
        """
        pass


class Receiver(Node):
    """
    Class representing a Receiver node in a network.
    Inherits from "Node" class.
    """

    def __init__(self, identifier: int):
        super().__init__(identifier, Roles.RECEIVER)

    def receive_message(self, message: str, sender: 'Node'):
        """
        Method definition for receiving a message.

        :param message: str. The message to be received.
        :param sender: Node. The sender of the message.
        """
        print(f'Receiver id={self.id} received a message from sender id={sender.id}: {message}')


class WordGenerator(Node):
    """
    Class representing a WordGenerator node in a network.
    Inherits from "Node" class.
    """

    def __init__(self, identifier: int):
        super().__init__(identifier, Roles.WORD_GENERATOR)

    def generate_word(self) -> str:
        """
        Method definition for generating a word.

        :returns: str. The generated word.
        """
        pass
