<p align="center">
<img src="https://github.com/SebastianoF/nilabels/blob/master/logo_low.png" width="350">
</p>

# NiLabels

(ex. [LABelsToolkit](https://github.com/SebastianoF/LABelsToolkit))

NiLabels is a set of tools to automatise simple manipulations and measurements of medical image 
segmentations in nifti format.

### Features

+ Written in Python 2.7
+ Simplifies the access to a range of tools and algorithms for the manipulation of medical image segmentations (see more under [motivations](https://github.com/SebastianoF/nilabels/wiki/Motivations))
+ After importing NiLabels, you can quickly: 
    + check if there are missing labels in a segmentation 
    + count the number of connected components
    + get the corresponding 4D RGB image (with colors provided in ITK-snap or fsl labels descriptor format) 
    + apply rotations and translations to the image header
    + permute or change the segmentation numbering, erase or merge labels 
    + compute Dice's score, covariance distance, Hausdorff distance and normalised symmetric contour distance between segmentations 
    + get the array of values at the voxel below a given label 
    + symmetrise a segmentation 
    + [...and more](https://github.com/SebastianoF/nilabels/wiki/What-you-can-do-with-nilabels)
+ Facade design pattern (see the [docs](https://github.com/SebastianoF/nilabels/wiki/Design-Pattern))

### Not-features (work in progress)

+ Not yet Python 3, back compatible python 2.7
+ Not yet 80% coverage
+ Not yet pip-installable
+ [... and more](https://github.com/SebastianoF/nilabels/wiki/Work-in-Progress)

### Introductory example

Given a segmentation `my_segm.nii.gz` imagine you want to change the labels values from [1, 2, 3, 4, 5, 6] to [2, 12, 4, 7, 5, 6]
and save the result in `my_new_segm.nii.gz`. Then:

```python
import nilabels as nis


nis_app = nis.App()
nis_app.manipulate_labels.relabel('my_segm.nii.gz', 'my_new_segm.nii.gz',  [1, 2, 3, 4, 5, 6], [2, 12, 4, 7, 5, 6])

```

### How to install (in development mode) 


+ Install NiLabels: the current version is not (yet) pip installable. It can be installed in development mode.
To proceed, initialise a virtual environment and execute the following instructions:
```
cd <folder where to clone the code>
git clone https://github.com/SebastianoF/nilabels.git
cd nilabels
pip install -e .
```
In development mode every change made to your local code will be directly affecting the installed library
without reinstalling.


+ Install python requirements in requirements.txt with
    `pip install -r requirements.txt`
in a [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/).

+ For advanced method `symmetrise_wit_registration`, extra examples and quick arrays visualisation with ITK-snap you can
    + Install [NiftySeg](https://github.com/KCL-BMEIS/NiftySeg)
    + Install [NiftyReg](https://github.com/KCL-BMEIS/niftyreg)
    + Install [ITK-snap](http://www.itksnap.org/pmwiki/pmwiki.php?n=Downloads.SNAP3)


### Documentations

+ [Wiki-pages documentation](https://github.com/SebastianoF/nilabels/wiki)


### Code testing

Code testing is a work in progress. We are aiming at reaching the 80% of coverage for the methods acting on numpy arrays and nibabel images, below the facade.
To run the test, `pip install -U pytest` and `pip install coverage` followed by:
```bash
pytest --cov --cov-report html
coverage html
open htmlcov/index.html
```

### Licencing and Copyright

Copyright (c) 2017, Sebastiano Ferraris. NiLabels  (ex. LABelsToolkit) is provided as it is and 
it is available as free open-source software under 
[MIT License](https://github.com/SebastianoF/nilabels/blob/master/LICENCE.txt)


### Acknowledgements

+ This repository is developed within the [GIFT-surg research project](http://www.gift-surg.ac.uk).
+ This work was supported by Wellcome / Engineering and Physical Sciences Research Council (EPSRC) [WT101957; NS/A000027/1; 203145Z/16/Z]. 
Sebastiano Ferraris is supported by the EPSRC-funded UCL Centre for Doctoral Training in Medical Imaging (EP/L016478/1) and Doctoral Training Grant (EP/M506448/1). 
