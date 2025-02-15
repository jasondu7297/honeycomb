from pydantic import BaseModel, Field

class ModelRegistry(BaseModel):
    _all_models: dict[str, bool] = Field(default_factory=dict) # Maps a model to boolean indicating enabled/disabled

    def is_enabled(self, name: str) -> bool:
        '''Returns True if the model is enabled, False if disabled or not registered.'''
        return self._all_models.get(name, False)

    def enable_model(self, name: str) -> None:
        '''Marks an existing model as enabled. Does nothing if the model is not registered.'''
        if name in self._all_models:
            self._all_models[name] = True

    def disable_model(self, name: str) -> None:
        '''Marks an existing model as disabled. Does nothing if the model is not registered.'''
        if name in self._all_models:
            self._all_models[name] = False
