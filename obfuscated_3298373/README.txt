To run:

> python checks.py /path/to/responses/json > results
I.e.
> python checks.py data/modified/

See data/original for examples of task json.

data/original: Downloaded json from the 8 task examples.
data/modified: The 8 tasks in original modified to have some quality problems.


-----------
Thoughts:

1. Using edge detection to detect edges in the image and see if the annotations
are close to some of the edges discovered.

2. Adding some known (labelled) images in new image data sets and comparing the
new annotations with known good annotations to understand quality.

3. Check to see if the boxes overlap and check if the occlusion attributes
are set for such images.

4. Comparing the same task results from multiple people and flagging discrepencies.

5. Giving a quality score (like pagerank) to annotators based on
"Good annotators are similar to other good annotators".

6. Understanding the annotation process and what affects the process.
I.e. length of time, speed of annotations/tasks. Tracking these metrics
and creating a model for quality for each task.
