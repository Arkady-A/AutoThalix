======================
How to use the package
======================

Example experiment walk through on how to use the package.
The example experiment can be found here: `AutoThalix_experiments <https://github.com/Arkady-A/AutoThalix_experiments>`__

You can fork/clone the repository and run the example experiment on your machine and add
new experiments locally, or into your fork.

Also, you can clone repository and make it private, if you wish to keep your experiments private.

* `example_experiment/baseline.yml <https://github.com/Arkady-A/AutoThalix_experiments/blob/main/example_experiment/baseline.yaml>`__
    contains the configuration of the example experiment. It is a YAML file, so it is easy to read and modify.
    All variables that will be defined in it will be used as a **default**, unless they are overwritten in the code.

* `example_experiment/main.py <https://github.com/Arkady-A/AutoThalix_experiments/blob/main/example_experiment/main.py>`__
    contains the code of the example experiment. It is a Python file. It is recommended to
    define all parameters in the baseline file and overwrite them in the code. This will make it easier to change the
    experiment parameters.

So the main idea is to define all parameters in the baseline file and overwrite them in the code.
This will make it easier to change the experiment parameters.

