# Thoughts on quality checks

## Below are my thoughts on how to improve quality checks of the tasks.

### First, what are the reasons for low quality annotations?
1. Low understanding of the task. (tasker_issue)
2. Lack of diligence/focus for various reasons. (tasker_issue)
This may also change in the same task session (focus decreases over time).
3. Trying to minimize time on a task. (tasker_issue)
4. Some images are more difficult to annotate for various reasons. (image issue)

### Quality check requirement

As a general problem, we would like to assign a score / probability of bad quality to every image task. There may be multiple scores we could assign to every image task, but lets start with a single score.

So we want a model that outputs this score.

### What are the features of the model?

1. Known bad quality of last x tasks.
Use some percentage of known images and score the quality.

2. Time taken to annotate.
A very short time may signal bad quality.

3. Time per annotation.

4. Image difficulty.
This can be judged by comparing the annotations on an image from different taskers and measuring the difference in some way.

5. Time in tasker session.
Over time, quality may decrease.

6. Annotation features:
    - Number of annotations (boxes)
    - Avg size of boxes
    - Time per annotation
    - Total time for task

7. The annotators quality score.

    Overall quality score for an annotator. This score can be calculated by a combination of known image annotation quality and comparison of annotations with another taskers and the heuristic that good annotators tend to produce similar results (like the pagerank algorithm).


### Other not well thought out ideas

- Create a model to estimate the number and attributes of each image just using the image. If this model is good, use its output as a feature in the quality model.