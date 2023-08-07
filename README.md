# Cardiovascular Control Model Viewer

description: Viewer specific for the Cardiovascular Control Model on  o²S²PARC. More information about the Cardiovascular Control Model can be found [here](https://github.com/ITISFoundation/CardiovascularControl-DBI). The source code of this viewer is [here](https://github.com/ITISFoundation/cardiocontro-dbi-viewer).


## Usage

```console
$ make help

$ make build
$ make run-local 
$ make tests
```

## Workflow
### Build and test locally
1. The source code shall be copied to the [src](cardiocontrol-dbi-viewer/src/cardiocontrol_dbi_viewer) folder.
2. The [Dockerfile](cardiocontrol-dbi-viewer/src/Dockerfile) shall be modified to compile the source code.
3. The [.osparc](.osparc) is the configuration folder and source of truth for metadata: describes service info and expected inputs/outputs of the service.
4. The [execute](cardiocontrol-dbi-viewer/service.cli/execute) shell script shall be modified to run the service using the expected inputs and retrieve the expected outputs.
5. The test input/output shall be copied to [validation](cardiocontrol-dbi-viewer/validation).
6. The service docker image may be built and tested as ``make build tests`` (see usage above)
7. Optional: if your code requires specific CPU/RAM resources, edit [runtime.yml](.osparc/runtime.yml). In doubt, leave it as default.

### Publish a new version

```console
$ make service-version-patch #or service-version-minor/major
```
Build and the test.
A GitHub CI Action will push the new version to DockerHub.

## Have an issue or question?
Please open an issue [in this repository](https://github.com/ITISFoundation/CardiovascularControl-DBI/issues/).
---
<p align="center">
<image src="https://github.com/ITISFoundation/osparc-simcore-python-client/blob/4e8b18494f3191d55f6692a6a605818aeeb83f95/docs/_media/mwl.png" alt="Made with love at www.z43.swiss" width="20%" />
</p>
