from pickle import DEFAULT_PROTOCOL
import sys, os
from turtle import width
import requests
import json
from PIL import Image
import pprint

class AnnotationTaskChecks(object):
  """Quality checks for Annotations."""

  DEFAULT_PARAMS = {
    'width_limit':400,
    'height_limit':400,
    'do_image_checks':True
  }

  def __init__(self, params={}):
    self.DEFAULT_PARAMS.update(params)

  def _getAnnotations(self, task):
    return task.get('response', {}).get('annotations', [])

  def _getImage(self, url):
    return Image.open(requests.get(url, stream=True).raw)

  def doChecks(self, task):
    # TODO: Checks for the type of task.
    # There may be tasks that are not suitable for the checks here.

    task_severity = 0  # 0 = ok, 1 = warning, 2 = error
    def _updateTaskSeverity(severity):
      nonlocal task_severity
      if task_severity < severity:
        task_severity = severity

    task_checks = {}
    annotation_checks = {}
    #task_checks = {'annotation_checks':annotation_checks}

    boxes = set()
    annotations = self._getAnnotations(task)
    if not annotations:
      task_checks["noAnnotations"] = True
      _updateTaskSeverity(2)

    image_url = task.get('params', {}).get('attachment')
    image = None
    if self.DEFAULT_PARAMS['do_image_checks'] and image_url:
      image = self._getImage(image_url)

    for an in annotations:
      an_check = {}

      # Check if multiple annotations are in the same position
      # after looping over all annotations.
      boxes.add((an['width'], an['height'], an['left'], an['top']))

      # Construction sign
      if (an.get('label') == 'construction_sign'
        and an.get('attributes', {}).get('background_color') != 'orange'):
        an_check['CheckConstructionColorOrange'] = True
        _updateTaskSeverity(1)

      # Too big
      if (an.get('width', 0) > self.DEFAULT_PARAMS['width_limit']
          or an.get('height', 0) > self.DEFAULT_PARAMS['height_limit']):
        an_check['CheckBoxTooBig'] = True
        _updateTaskSeverity(2)

      # Box is the whole image size
      # Q: Does the box have to start at (0,0)?
      if (image
          and an.get('width', 0) >= image.width
          and an.get('height') >= image.height):
        an_check['CheckBoxGeImage'] = True
        _updateTaskSeverity(2)

      if an_check:
        annotation_checks[an['uuid']] = an_check

    if len(boxes) < len(annotations):
      task_checks['CheckDuplicateAnnotationBoxes'] = True
      _updateTaskSeverity(2)

    if task_severity > 0:
      task_checks['severity'] = task_severity

    if annotation_checks:
      task_checks['annotation checks'] = annotation_checks

    return task_checks

def get_tasks(tasksDir):
  tasks = []
  for tf in os.listdir(tasksDir):
    t = json.loads(open(os.path.join(tasksDir, tf)).read())
    tasks.append(t)
  return tasks

if __name__ == "__main__":
  input_dir = sys.argv[1]
  tasks = get_tasks(input_dir)

  task_checks = {}
  atc = AnnotationTaskChecks({'do_image_checks':False})
  #atc = AnnotationTaskChecks()
  for t in tasks:
    tc = atc.doChecks(t)
    if tc:
      task_checks[t['task_id']] = tc

  pprint.pprint(task_checks)
