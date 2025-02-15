from pydantic import BaseModel, Field
from typing import Dict, Set

class ToolRegistry(BaseModel):
    _all_tools: Dict[str, Set[str]] = Field(default_factory=dict) # Maps a tool to all models that have it enabled

    def is_enabled(self, tool: str, model: str) -> bool:
        '''Check if a tool is enabled for a specific model.'''
        return tool in self._all_tools and model in self._all_tools[tool]

    def enable_tool(self, tool: str, model: str) -> None:
        '''Enable a tool for a specific model.'''
        self._all_tools.setdefault(tool, set()).add(model)

    def disable_tool(self, tool: str, model: str) -> None:
        '''Disable a tool for a specific model.'''
        if tool in self._all_tools and model in self._all_tools[tool]:
            self._all_tools[tool].remove(model)
