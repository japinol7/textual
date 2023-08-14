from textual.app import App
from textual.command_palette import (
    CommandMatches,
    CommandPalette,
    CommandSource,
    CommandSourceHit,
)
from textual.screen import Screen


class ExampleCommandSource(CommandSource):
    async def hunt_for(self, _: str) -> CommandMatches:
        def gndn() -> None:
            pass

        yield CommandSourceHit(1, "Hit", gndn, "Hit")


class AppWithActiveCommandPalette(App[None]):
    def on_mount(self) -> None:
        self.action_command_palette()


class AppWithNoSources(AppWithActiveCommandPalette):
    pass


async def test_no_app_command_sources() -> None:
    """An app with no sources declared should work fine."""
    async with AppWithNoSources().run_test() as pilot:
        assert pilot.app.query_one(CommandPalette)._sources == set()


class AppWithSources(AppWithActiveCommandPalette):
    COMMAND_SOURCES = {ExampleCommandSource}


async def test_app_command_sources() -> None:
    """Command sources declared on an app should be in the command palette."""
    async with AppWithSources().run_test() as pilot:
        assert (
            pilot.app.query_one(CommandPalette)._sources
            == AppWithSources.COMMAND_SOURCES
        )


class AppWithInitialScreen(App[None]):
    def __init__(self, screen: Screen) -> None:
        super().__init__()
        self._test_screen = screen

    def on_mount(self) -> None:
        self.push_screen(self._test_screen)


class ScreenWithNoSources(Screen[None]):
    def on_mount(self) -> None:
        self.app.action_command_palette()


async def test_no_screen_command_sources() -> None:
    """An app with a screen with no sources declared should work fine."""
    async with AppWithInitialScreen(ScreenWithNoSources()).run_test() as pilot:
        assert pilot.app.query_one(CommandPalette)._sources == set()


class ScreenWithSources(ScreenWithNoSources):
    COMMAND_SOURCES = {ExampleCommandSource}


async def test_screen_command_sources() -> None:
    """Command sources declared on a screen should be in the command palette."""
    async with AppWithInitialScreen(ScreenWithSources()).run_test() as pilot:
        assert (
            pilot.app.query_one(CommandPalette)._sources
            == ScreenWithSources.COMMAND_SOURCES
        )
