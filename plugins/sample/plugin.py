class VisionPlugin:
    def initialize(self, config: dict) -> None:
        self.config = config
    def process(self, frame, metadata: dict) -> list[dict]:
        return []
    def health(self) -> dict:
        return {"status": "ok"}
    def shutdown(self) -> None:
        pass
