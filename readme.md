# Quad Disc
This plugin creates a disc which consists solely of quads. The disc is fully parametric.

# Installation
To install the plugin perform the following steps:

1. Download the [latest zip from the release folder](release/QuadDisc_01_00.zip).
2. Extract the contents of the zip file into your Cinema 4D plugin directory.
3. Done.

# Usage
After [installing](#installation) the plugin simply create an instance from the *Extensions* menu:

\<screenshot>

Use the parameters to define the topology of the disc. The following schematic helps understanding the parameters:

\<screenshot>

|Parameter|Description|
|-|-|
|Radius|The radius of the disc.|
|Rings|The number of rings around the square.|
|Orientation|The orientation of the generated geometry.|
|Subdivisions|The amount of subdivisions the rings and square have.|
|Smoothing Iterations|The number of iterations to perform smoothing.|
|Smoothing Stiffness|The amount of stiffness for the smoothing.|

# Scene File
This repository also holds a [scene file](./QuadDisc.c4d).

This plugin was developed using a Python generator. The scene file contains a version of the script which works with a Python generator which may be used to play around with the algorithm. Note that this script always orients the geometry in the Z- orientation and that the plugin script has a slightly different code structure.

The scene file also contains a camera setup to generate the plugin icon.

# Disclaimer
This code is provided as-is. I do not take any responsibility for any harm this may cause. You may use this code however you see fit except selling it.

This code was tested with Cinema 4D 2024.1.0.