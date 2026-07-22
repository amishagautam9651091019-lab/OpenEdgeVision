from __future__ import annotations

from app.plugins.base import BaseVisionPlugin


class PluginRegistry:
    """
    AI 插件注册中心。

    负责插件注册、查找、加载、卸载和列表查询。
    """

    def __init__(self) -> None:
        self._plugins: dict[str, BaseVisionPlugin] = {}

    def register(
        self,
        plugin: BaseVisionPlugin,
        *,
        replace: bool = False,
    ) -> None:
        plugin_id = plugin.plugin_id

        if plugin_id in self._plugins and not replace:
            raise ValueError(
                f"Plugin already registered: {plugin_id}"
            )

        self._plugins[plugin_id] = plugin

    def unregister(self, plugin_id: str) -> None:
        plugin = self.get(plugin_id)

        if plugin.is_loaded:
            plugin.unload()

        del self._plugins[plugin_id]

    def get(self, plugin_id: str) -> BaseVisionPlugin:
        plugin = self._plugins.get(plugin_id)

        if plugin is None:
            raise KeyError(
                f"Plugin not found: {plugin_id}"
            )

        return plugin

    def list_plugins(self) -> list[BaseVisionPlugin]:
        return list(self._plugins.values())

    def load(self, plugin_id: str) -> BaseVisionPlugin:
        plugin = self.get(plugin_id)
        plugin.load()
        return plugin

    def unload(self, plugin_id: str) -> BaseVisionPlugin:
        plugin = self.get(plugin_id)
        plugin.unload()
        return plugin


plugin_registry = PluginRegistry()