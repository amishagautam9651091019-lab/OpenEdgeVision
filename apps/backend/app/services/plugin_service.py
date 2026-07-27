from __future__ import annotations

from typing import Any

from app.plugins.registry import plugin_registry

from app.schemas.plugin import (
    PluginActionData,
    PluginHealthData,
    PluginListData,
    PluginStatus,
)


class PluginService:
    """
    AI插件业务服务。

    负责：

    - 插件列表
    - 插件状态
    - 生命周期管理
    - 调用插件推理

    不负责：

    - AI结果协议转换

    AI结果统一由：
    DetectionConverter
    完成。
    """



    def list_plugins(
        self,
    ) -> PluginListData:

        plugins = [

            plugin.get_info()

            for plugin
            in plugin_registry.list_plugins()

        ]


        loaded = sum(

            1

            for plugin
            in plugins

            if plugin.status == PluginStatus.LOADED

        )


        available = sum(

            1

            for plugin
            in plugins

            if plugin.status == PluginStatus.AVAILABLE

        )


        return PluginListData(

            total=len(plugins),

            loaded=loaded,

            available=available,

            plugins=plugins,

        )



    def get_plugin(
        self,
        plugin_id: str,
    ):

        plugin = plugin_registry.get(
            plugin_id
        )

        return plugin.get_info()



    def load_plugin(
        self,
        plugin_id: str,
    ) -> PluginActionData:


        plugin = plugin_registry.load(
            plugin_id
        )


        return PluginActionData(

            plugin=plugin.get_info()

        )



    def unload_plugin(
        self,
        plugin_id: str,
    ) -> PluginActionData:


        plugin = plugin_registry.unload(
            plugin_id
        )


        return PluginActionData(

            plugin=plugin.get_info()

        )



    def get_health(
        self,
        plugin_id: str,
    ) -> PluginHealthData:


        plugin = plugin_registry.get(
            plugin_id
        )


        health = plugin.health()


        return PluginHealthData(

            plugin_id=plugin_id,

            healthy=bool(
                health["healthy"]
            ),

            status=plugin.status,

            details=health,

        )



    def predict(
        self,
        *,
        plugin_id: str,
        frame: Any,
        frame_id: int,
        stream_name: str,
    ) -> Any:
        """
        调用AI插件执行推理。

        返回：

        Raw AI Result

        后续由 Converter
        转换为 AI Protocol v1.0
        """


        plugin = plugin_registry.get(
            plugin_id
        )


        if plugin is None:

            raise RuntimeError(
                f"Plugin not found: {plugin_id}"
            )


        if not hasattr(
            plugin,
            "predict"
        ):

            raise RuntimeError(
                f"Plugin {plugin_id} "
                "does not implement predict()"
            )


        return plugin.predict(

            frame=frame,

            frame_id=frame_id,

            stream_name=stream_name,

        )



    def mock_predict(
        self,
        *,
        plugin_id: str,
        stream_name: str,
        frame_id: int,
        frame_width: int,
        frame_height: int,
    ) -> dict:

        """
        Mock推理接口。

        保留用于测试。

        返回Raw AI Result。
        """


        plugin = plugin_registry.get(
            plugin_id
        )


        return plugin.predict(

            frame={

                "width": frame_width,

                "height": frame_height,

            },

            stream_name=stream_name,

            frame_id=frame_id,

        )



plugin_service = PluginService()