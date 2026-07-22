from app.plugins.builtin.mock_detector import MockDetectorPlugin
from app.plugins.registry import plugin_registry


def register_builtin_plugins() -> None:
    """
    注册平台内置插件。

    使用 replace=True，避免开发环境热重载时重复注册。
    """

    plugin_registry.register(
        MockDetectorPlugin(),
        replace=True,
    )