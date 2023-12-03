![image](https://github.com/YoYoFreakCJ/C4D-QuadDisc/assets/59722190/51224a19-e548-447d-93d3-d7ac9e5e1411)
![Cinema_4D_m3jQZixz2X](https://github.com/YoYoFreakCJ/C4D-QuadDisc/assets/59722190/99de2555-36b0-4221-beee-fbc9ee96f300)


# Quad Disc
This plugin creates a disc which consists solely of quads. The disc is fully parametric.

Especially when trying to keep things parametric you quickly run into issues using the default triangle-based disc which ships with Cinema 4D, especially when it comes to deforming the disc or putting it under a Subdivision Surface. By keeping the topology quad-based these issues can be mitigated.

# Installation
To install the plugin perform the following steps:

1. Download the [latest zip from the release folder](release/QuadDisc_01_00.zip).
2. Extract the contents of the zip file into your Cinema 4D plugin directory (_%APPDATA%_/Maxon Cinema 4D */plugins).
3. Done.

# Usage
After [installing](#installation) the plugin simply create an instance from the *Extensions* menu or the *Command Manager* (Shift + C):
![image](https://github.com/YoYoFreakCJ/C4D-QuadDisc/assets/59722190/1adf97ce-da3c-4541-a796-491234e96c8f)

Use the parameters to define the topology of the disc. The following screenshots help understanding the parameters:

![image](https://github.com/YoYoFreakCJ/C4D-QuadDisc/assets/59722190/a9f30fc1-b266-42e3-8885-0b7d7c7f338e)

![image](https://github.com/YoYoFreakCJ/C4D-QuadDisc/assets/59722190/3f84e02f-88d0-429d-90c0-339935fbde46)

Or just play around with the parameters, you'll figure it out.

|Parameter|Description|
|-|-|
|Radius|The radius of the disc.|
|Rings|The number of ${\textsf{\color{#AC536C}rings}}$ around the square.|
|Orientation|The orientation of the generated geometry.|
|Subdivisions|The amount of ${\textsf{\color{#47ADA5}subdivisions}}$ the rings and square have. For the rings this is per quarter ring.|
|Smoothing Iterations|The number of iterations to perform smoothing on the ${\textsf{\color{#47ADA5}square}}$.|
|Smoothing Stiffness|The amount of stiffness for the smoothing of the ${\textsf{\color{#47ADA5}square}}$.|

# Scene File
This repository also holds a [scene file](./QuadDisc.c4d).

This plugin was developed using a Python generator. The scene file contains a version of the script which works with a Python generator which may be used to play around with the algorithm. Note that this script always orients the geometry in the Z- orientation and that the plugin script has a slightly different code structure.

The scene file also contains a camera setup to generate the plugin icon.

# Disclaimer
This code is provided as-is. I do not take any responsibility for any harm this may cause. You may use this code however you see fit except selling it.

This code was tested with Cinema 4D 2024.1.0.
