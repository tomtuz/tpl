from dataclasses import dataclass


@dataclass
class Config:
    index: str


@dataclass
class Preset:
    fileArray: list[str]


@dataclass
class DependencyTreeItem:
    type: list[str] | None = None
    variant: list[str] | None = None
    esbuild: list[str] | None = None


@dataclass
class DependencyTree:
    package: DependencyTreeItem
    build: DependencyTreeItem
    settings: list[str]
    launch: list[str]
    tsconfig: list[str]
    biome: list[str]
    eslint: list[str]


@dataclass
class FileIndex:
    updated: str
    index: str
    presets: dict[str, Preset]
    dependency_tree: DependencyTree


@dataclass
class Template:
    repo: str
    base: str
    variant: str


@dataclass
class Plugin:
    repo: str
    base: str
    variant: str


@dataclass
class Base:
    config: Config
    file_index: FileIndex
    templates: dict[str, Template]
    plugins: dict[str, Plugin]


@dataclass
class RootStructure:
    base: Base
    updated: str
    test_key: str
    initialized: str


# Modify the usage example:
root = RootStructure(
    base=Base(
        config=Config(index=""),
        file_index=FileIndex(
            updated="",
            index="",
            presets={},
            dependency_tree=DependencyTree(
                package=DependencyTreeItem(type=[], variant=[]),
                build=DependencyTreeItem(
                    type=[],
                    variant=[],
                    esbuild=[],
                ),
                settings=[],
                launch=[],
                tsconfig=[],
                biome=[],
                eslint=[],
            ),
        ),
        templates={"": Template(repo="", base="", variant="")},
        plugins={"": Plugin(repo="", base="", variant="")},
    ),
    updated="",
    test_key="",
    initialized="",
)
