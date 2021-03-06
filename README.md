## DEMCERT - A general purpose tool for modelling uncertainty on gridded spatial data using Gaussian random fields

[![DOI](https://zenodo.org/badge/282487376.svg)](https://zenodo.org/badge/latestdoi/282487376)

Almost every spatial dataset contains a certain amount of uncertainty that is the lack of knowledge about errors in the data. Since our knowledge about the errors in spatial data is usually limited (but we can be relatively sure that errors are very likely to exist) we have to acknowledge that uncertainty persists in our data. Consequently, uncertainty will also have an impact on analysis and modelling that is carried out.

The **purpose** of this small tool is to provide a **stochastic attempt** to model uncertainty of gridded spatial dataset such as Digital Elevation Models (DEMs). **demcert** attempts to model uncertainty by generating **scenarios**, i.e., a set of possible dataset realizations, which account for the level of uncertainty that we assume to be present in the dataset. We then assume that the "true" state lies somewhere in between all those realizations generated and the variation between the single realizations accounts for the potential impact of uncertainty on subsequent analysis and modelling attempts.

The approach we are proposing in **demcert** used **Gausssian random fields** which are convolved by filter kernels to the original data. We assume that uncertainty has a spatial component and that uncertainty mimics **spatial autocorrelation** found in almost all spatial datasets. *N* realizations are thereby created using **Monte Carlo** techniques. The size of the filter kernel can be determined, i.e.,  from semi-variogram analysis.

In the case of DEMs we get a mathematical representation of the Earth's (bare) surface; i.e., we have a raster where the value of each grid cell denotes an elevation value above a reference level (usually the sea surface). We can then define an error as the deviation of the elevation value in the dataset from the "true" value. Such deviations can be caused by errors during the recording of the data, the data processing and the measurement process. Since we do not know about all those errors, uncertainty about the DEM arises.

### Installation
Currently, the only way to install demcert works via cloning from this github repository and
running setup.py in your Python3 shell:

```{cmd}
git clone https://github.com/lukasValentin/demcert.git
cd demcert
python3 setup.py install
```
