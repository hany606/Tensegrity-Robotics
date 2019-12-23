# Dev

This folder has the experiments and the models.

The models that works are:

- jumper
- legz

But due to problem with CMake files, building of the nlohmann_json and the required specific version of g++ that is not compatible with the compilor required for the json library, the library is included inside the model and only one of them can compiled at once.
