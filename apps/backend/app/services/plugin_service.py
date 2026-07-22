from __future__ import annotations

from app.plugins.registry import plugin_registry
from app.schemas.plugin import (
    DetectionResult,
    PluginActionData,
    PluginHealthData,
    PluginListData,
    PluginStatus,
)


class PluginService:
    """AI 插件业务服务。"""

    def list_plugins(self) -> PluginListData:
        plugins = [
            plugin.get_info()
            for plugin in plugin_registry.list_plugins()
        ]

        loaded = sum(
            1
            for plugin in plugins
            if plugin.status == PluginStatus.LOADED
        )

        available = sum(
            1
            for plugin in plugins
            if plugin.status == PluginStatus.AVAILABLE
        )

        return PluginListData(
            total=len(plugins),
            loaded=loaded,
            available=available,
            plugins=plugins,
        )

    def get_plugin(self, plugin_id: str):
        return plugin_registry.get(plugin_id).get_info()

    def load_plugin(
        self,
        plugin_id: str,
    ) -> PluginActionData:
        plugin = plugin_registry.load(plugin_id)

        return PluginActionData(
            plugin=plugin.get_info()
        )

    def unload_plugin(
        self,
        plugin_id: str,
    ) -> PluginActionData:
        plugin = plugin_registry.unload(plugin_id)

        return PluginActionData(
            plugin=plugin.get_info()
        )

    def get_health(
        self,
        plugin_id: str,
    ) -> PluginHealthData:
        plugin = plugin_registry.get(plugin_id)
        health = plugin.health()

        return PluginHealthData(
            plugin_id=plugin_id,
            healthy=bool(health["healthy"]),
            status=plugin.status,
            details=health,
        )
    def predict(
	    self,
	    *,
	    plugin_id:str,
	    frame,
	    frame_id:int,
	    stream_name:str,
    ):
        "pipepline统一推理入手。"
	
        plugin=self.registry.get_plugin(plugin_id)  
        if plugin is None:
            raise  RuntimeError(
               f"Plugin not found: { plugin_id}"
            )

        if not hasattr(
	        plugin,
	        "predict"
     	):
            raise RuntimeError(
                 f"Plugin not found: { plugin_id}"
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
    ) -> DetectionResult:
        plugin = plugin_registry.get(plugin_id)

        return plugin.predict(
            frame={
                "width": frame_width,
                "height": frame_height,
            },
            stream_name=stream_name,
            frame_id=frame_id,
        )

    def predict(
        self,
        *,
        plugin_id:str,
        frame,
        frame_id:int,
        stream_name:str,
        ):
        plugin=plugin_registry.get(
            plugin_id
            )
        return plugin.predict(
                frame,
                frame_id=frame_id,
                stream_name=stream_name,
                )


plugin_service = PluginService()
