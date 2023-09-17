from __future__ import annotations

from typing import Optional, Mapping, Any

class Document():
    def __init__(self, content: str, metadata: Optional[Mapping[str, Any]]) -> None:
        self.content = content
        self.metadata = metadata