class SeasonYearError(Exception):
    """
    An error that will occur if the season year doesn't meet the
    requirements.

    Examples:

        - `2o24` -> `SeasonYearError`.
        - `193` -> `SeasonYearError`.
        - `aaaa` -> `SeasonYearError`.
        - `2024` -> OK.
    """

    def __init__(self, year_txt: str) -> None:
        self.year_txt = year_txt
        super().__init__(
            f"Season year doesn't meet the requirements. "
            f"Expected season year in format `YYYY`, got: `{self.year_txt}`."
        )


class HTMLExtensionError(Exception):
    """
    An error that will occur if the file doesn't have an HTML extension.
    """

    def __init__(self, extension: str) -> None:
        self.extension = extension
        super().__init__(
            f"Unsupported file extension. Expected `html`, got: "
            f"`{self.extension}`."
        )


class FileProcessingError(Exception):
    """An error that will occur if the file can't be processed."""

    def __init__(self, filename: str, e: Exception) -> None:
        self.filename = filename
        self.e = e
        super().__init__(
            f"An error occurred while processing file `{self.filename}`: "
            f"{self.e}."
        )
