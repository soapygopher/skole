README FOR ASSIGNMENT 3 IN ECSE 526 ARTIFICIAL INTELLIGENCE

Author: Hakon Mork

The code for this assignment is written as a Matlab script. To use
it, simply open it in Matlab and run it.

Make sure that the input images are in a folder called "images" in
the same directory, or else change the string on line 13 as
appropriate.

The code was tested on Mac OS X 10.7.5 using 64-bit Matlab R2012a
with various toolboxes installed, and I think the Statistics
toolbox is required to run the script since I use the
gmdistribution.fit function.

Most of the various datasets and illustrations in the assignment
text were produced by manually changing various parameters in the
code. If you want to replicate the results, the most important ones
are:

Line 16: Set true to solve problem 1 and 2, producing images with
green dots overlaid to represent Gaussian means.

Line 17: Set true to solve problem 3 and 4, producing images
segmented according to a simple heuristic based on the Gaussian
means computed by EM.

Line 18: Set true to produce a nice overlay of the computed
weighted-average Gaussian with contour lines to show how it
corresponds to the image.

Line 29: Input file. Change the string to any imageN_X, where N in
{1, 2, 3} and X in {a, b, c}.

Line 48: Number of clusters. I've mostly used 4 or 5.

Lines 64--76: Initialization for the EM algorithm, if you want to
provide one manually.
