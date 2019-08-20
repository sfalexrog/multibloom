# multibloom

## What?

Multibloom is a tool to create debian packages from packages in your ROS workspace.

## Why?

As of the time of writing and to the best of my knowledge, ROS provides two ways of building packages for distributions:

* `bloom-generate` + `fakeroot` to build a single Debian package;

* ROS buildfarm to build everything.

The first option may be cumbersome if you're building several packages, even more so if they are interdependent. The second one takes quite some time to set up and maintain.

`multibloom` aims to be an "in-between" solution that allows you to build several packages at once locally.

## How?

`multibloom` currently supports two "verbs":

* `rosdep` - create a `rosdep.yaml` file from packages in your current workspace. This is more of a hack, but you need this if you're building a package not in the ROS registry.
* `generate` - build actual packages. Currently works only for Debian packages, and you need to install them to your prefix (`/opt/ros/melodic`) before running this. This may change in the future.

Run `multibloom.py rosdep` and save its output to a `.yaml` file. Put this file somewhere in your filesystem (`/etc/ros/rosdep/multibloom.yaml`) and make a reference to it in `/etc/ros/rosdep/sources.list.d/99-local.list` (a line like `yaml file:///etc/ros/rosdep/multibloom.yaml` will suffice). Don't forget to run `rosdep update` to merge this file with `rosdep` database.

`generate` actually runs `bloom-generate` and `fakeroot` for each package, so you may want to hack your `bloom-generate` templates to speed up the process (especially when building with qemu).

These commands must be run from your workspace root (they assume your packages are in the `src` subdirectory in your current working directory).

## Notes

* You might want to hack `bloom` templates. They are located in `/usr/lib/python2.7/dist-packages/bloom/generators/debian/templates/{catkin,cmake,ament_cmake,ament_python}` by default. Make sure your `dh_auto_build` line looks like

    ```text
        dh_auto_build --parallel -- -j4
    ```

    where the number after `-j` is the amount of cores in your system.
* You'll have to build `catkin` package manually since it does not generate required shell scripts by default. Run `bloom-generate` in the `catkin` package directory, then open `debian/rules` file and remove the

    ```text
        -DCATKIN_BUILD_BINARY_PACKAGE="1" \
    ```

    line from the configuration options (this line actually prevents `setup.sh`, `setup.bash` and the likes from being packaged, which in case of `catkin` is the opposite of what you want!)
