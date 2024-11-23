from src.utils.helpers import Logger
from src.types.repo_struct import (
    RepositoryStruct,
)

logger = Logger.create_logger(f"{__name__}.log", __package__, False)

def get_repositories() -> RepositoryStruct:
    ''';
    Returns a RepositoryStruct object containing repository data.
    '''
    logger.info("Fetching repository data")

    try:
        data = RepositoryStruct(
            updated="2023-10-01T12:00:00",
            repositories=[
                {
                    "name": "Python Project Template",
                    "description": "Poetry",
                    "url": "https://github.com/tomtuz/pybase.git"
                },
                {
                    "name": "Another Repository",
                    "description": "Another description",
                    "url": "https://github.com/anotheruser/anotherrepo.git"
                }
            ],
            file_index=[]
        )
        logger.debug("Repository data fetched successfully: %s", data)
        return data
    except Exception as e:
        logger.error("Failed to fetch repository data: %s", e)
        raise

if __name__ == "__main__":
    logger.setLevel("DEBUG")
    try:
        repositories = get_repositories()
        logger.info("Repositories fetched: %s", repositories)
    except Exception as e:
        logger.error("Error in main: %s", e)
