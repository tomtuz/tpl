import json
import logging
import os
from typing import Any

import questionary
from questionary import Choice
from src.core.file_manager import get_config_dir
from src.types.struct import (
    Base,
    Config,
    DependencyTree,
    DependencyTreeItem,
    FileIndex,
    Plugin,
    Preset,
    RootStructure,
    Template,
)

from src.types.repo_struct import (
    RepositoryStruct,
)

from src.repositories.main import get_repositories

logger = logging.getLogger(__name__)


def load_config(file_path: str) -> RootStructure | None:
    try:
        with open(file_path) as f:
            data = json.load(f)

        base_data = data["base"]
        file_index_data = base_data["file_index"]
        dependency_tree_data = file_index_data["dependency_tree"]

        dependency_tree = DependencyTree(
            package=DependencyTreeItem(**dependency_tree_data["package"]),
            build=DependencyTreeItem(**dependency_tree_data["build"]),
            settings=dependency_tree_data["settings"],
            launch=dependency_tree_data["launch"],
            tsconfig=dependency_tree_data["tsconfig"],
            biome=dependency_tree_data["biome"],
            eslint=dependency_tree_data["eslint"],
        )

        file_index = FileIndex(
            updated=file_index_data["updated"],
            index=file_index_data["index"],
            presets={k: Preset(fileArray=v["fileArray"]) for k, v in file_index_data["presets"].items()},
            dependency_tree=dependency_tree,
        )

        templates = {}
        for k, v in base_data["templates"].items():
            if isinstance(v, dict):
                templates[k] = Template(**v)
            else:
                logger.error(f"Invalid template data for key {k}: {v}")

        plugins = {}
        for k, v in base_data["plugins"].items():
            if isinstance(v, dict):
                plugins[k] = Plugin(**v)
            else:
                logger.error(f"Invalid plugin data for key {k}: {v}")

        base = Base(
            config=Config(index=base_data["config"]["index"]),
            file_index=file_index,
            templates=templates,
            plugins=plugins,
        )

        return RootStructure(
            base=base, updated=data["updated"], test_key=data["test_key"], initialized=data["initialized"]
        )
    except FileNotFoundError:
        logger.error(f"Config file not found at {file_path}")
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON in config file at {file_path}")
    except KeyError as e:
        logger.error(f"Missing key in config file: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred while loading the config: {e}")
    return None


def select_items(category: str, items: list[str]) -> list[str] | None:
    choices = [Choice(item) for item in items] + [Choice("Go back", value="__back__")]
    selected = questionary.checkbox(
        f"Select {category} (use arrow keys and space to select, enter to confirm):",
        choices=choices,
    ).ask()
    if selected is None or "__back__" in selected:
        return None
    return selected

def questionary_prompt(prompt, list_options, default):
    value = questionary.select(
        prompt,
        list_options,
        default,
    ).ask()
    return value

def process_dependency_tree(dependency_tree: DependencyTree, preset: list[str]) -> dict[str, Any] | None:
    selections = {}
    for item in preset:
        tree_item = getattr(dependency_tree, item)
        if isinstance(tree_item, DependencyTreeItem):
            selections[item] = {}
            for attr, value in tree_item.__dict__.items():
                if value is not None:
                    result = select_items(f"{item} {attr}", value)
                    if result is None:
                        return None
                    selections[item][attr] = result
        elif isinstance(tree_item, list):
            result = select_items(item, tree_item)
            if result is None:
                return None
            selections[item] = result
    return selections

def cli_spawn_generic_list():
    logger.info("\n-- cli_spawn_generic_list --\n")

    logger.info(f"Loading repositories...")
    root_structure = load_repositories()

    logger.info(f"root_structure: ${root_structure.repositories}")

    if root_structure is None:
        logger.error("Failed to load git repositories. Exiting.")
        return

    # Create a mapping from display titles to actual repository URLs
    choice_map = {f'{repo["name"]} - {repo["url"]}': repo["url"] for repo in root_structure.repositories}

    # Add the "Exit" option
    choices = list(choice_map.keys()) + ["Exit"]

    # Use questionary to select a repository
    selected_repository = questionary.select(
        "Choose a preset (or 'Exit' to quit):",
        choices=choices,
    ).ask()

    if selected_repository == "Exit":
        logger.info("Exiting the CLI selector.")
        return

    # Return the actual repository URL if a repository is selected, otherwise return None
    logger.info(f"Selected preset: {selected_repository}")
    selected_choice = choice_map.get(selected_repository)
    return selected_choice

def load_repositories() -> RepositoryStruct | None:
    try:
        logger.info("\n-- load_repositories --\n")
        repository_struct: RepositoryStruct = get_repositories()

        for repo in repository_struct.repositories:
              logger.info(f"[REPO]: ${repo.items()}")

        logger.info("\n-- file_index --\n")
        file_index = []

        for item in repository_struct.repositories:
            file_index.append(
                dict(
                  key=f"{item['name']} - {item['url']}",
                  value=item,
                )
            )
            # file_index.append(f"{item['name']} - {item['url']}")

        repository_struct.file_index = file_index
        logger.info(f"file_index: ${file_index}")

        return repository_struct

    except Exception as e:
        logger.error(f"An unexpected error occurred while handling RepositoryStruct data: {e}")
    return None


def cli_selector_spawn():
    config_path = os.path.join(get_config_dir(), "config.json")
    logger.info(f"Loading config from: {config_path}")
    root_structure = load_config(config_path)
    if root_structure is None:
        logger.error("Failed to load configuration. Exiting.")
        return

    while True:
        preset_name = questionary.select(
            "Choose a preset (or 'Exit' to quit):",
            choices=list(root_structure.base.file_index.presets.keys()) + ["Exit"],
        ).ask()

        if preset_name == "Exit":
            logger.info("Exiting the CLI selector.")
            return

        logger.info(f"Selected preset: {preset_name}")

        preset = root_structure.base.file_index.presets[preset_name]
        dependency_tree = root_structure.base.file_index.dependency_tree

        selections = process_dependency_tree(dependency_tree, preset.fileArray)
        if selections is None:
            continue

        logger.info("\nYour selections:")
        for category, selected_items in selections.items():
            if isinstance(selected_items, dict):
                logger.info(f"{category}:")
                for subcat, items in selected_items.items():
                    logger.info(f"  {subcat}: {', '.join(items)}")
            else:
                logger.info(f"{category}: {', '.join(selected_items)}")

        if questionary.confirm("Are you satisfied with these selections?").ask():
            logger.info("Selections confirmed. Processing...")
            # Here you would add the logic to process the selections
            break
        else:
            logger.info("Let's try again.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    cli_selector_spawn()
