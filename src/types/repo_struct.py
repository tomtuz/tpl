from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class Repository:
    """
    Represents a repository with a name, description, and URL.
    """

    name: str | None = None
    description: str | None = None
    url: str | None = None


@dataclass
class RepositoryStruct:
    """
    Represents a structure containing repository data.
    """

    updated: str = ""
    repositories: List[Dict[str, Any]] = None
    file_index: List[str] = None

    def __repr__(self) -> str:
        return (
            f"RepositoryStruct(updated={self.updated}, repositories={self.repositories}, file_index={self.file_index})"
        )


# root = RepositoryStruct(
#     updated="",
#     repositories=[],
#     file_index=[]
# )
