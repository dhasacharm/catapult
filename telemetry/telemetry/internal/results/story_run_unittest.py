# Copyright 2015 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import unittest

from telemetry.internal.results import story_run
from telemetry.story import shared_state
from telemetry.story import story_set
from telemetry import story as story_module
from telemetry.value import improvement_direction
from telemetry.value import scalar
import time


# pylint: disable=abstract-method
class SharedStateBar(shared_state.SharedState):
  pass

class StoryFoo(story_module.Story):
  def __init__(self, name='', tags=None):
    super(StoryFoo, self).__init__(
        SharedStateBar, name, tags)

class StoryRunTest(unittest.TestCase):
  def setUp(self):
    self.story_set = story_set.StorySet()
    self.story_set.AddStory(StoryFoo(name='foo'))

  @property
  def stories(self):
    return self.story_set.stories

  def testStoryRunFailed(self):
    start_time = time.time()
    run = story_run.StoryRun(self.stories[0])
    run.SetFailed('abc')
    self.assertFalse(run.ok)
    self.assertTrue(run.failed)
    self.assertFalse(run.skipped)
    self.assertEquals(run.failure_str, 'abc')
    self.assertAlmostEqual(run.duration,
                           time.time() - start_time, 1)

    run = story_run.StoryRun(self.stories[0])
    run.AddValue(scalar.ScalarValue(
        self.stories[0], 'a', 's', 1,
        improvement_direction=improvement_direction.UP))
    run.SetFailed('something is wrong')
    self.assertFalse(run.ok)
    self.assertTrue(run.failed)
    self.assertFalse(run.skipped)
    self.assertEquals(run.failure_str, 'something is wrong')

  def testStoryRunSkipped(self):
    start_time = time.time()
    run = story_run.StoryRun(self.stories[0])
    run.SetFailed('oops')
    run.Skip('test')
    self.assertFalse(run.ok)
    self.assertFalse(run.failed)
    self.assertTrue(run.skipped)
    self.assertEquals(run.failure_str, 'oops')
    self.assertAlmostEqual(run.duration,
                           time.time() - start_time, 1)

    run = story_run.StoryRun(self.stories[0])
    run.AddValue(scalar.ScalarValue(
        self.stories[0], 'a', 's', 1,
        improvement_direction=improvement_direction.UP))
    run.Skip('test')
    self.assertFalse(run.ok)
    self.assertFalse(run.failed)
    self.assertTrue(run.skipped)
    self.assertEquals(run.failure_str, None)

  def testStoryRunSucceeded(self):
    start_time = time.time()
    run = story_run.StoryRun(self.stories[0])
    run.SetSucceeded()
    self.assertTrue(run.ok)
    self.assertFalse(run.failed)
    self.assertFalse(run.skipped)
    self.assertEquals(run.failure_str, None)
    self.assertAlmostEqual(run.duration,
                           time.time() - start_time, 1)

    run = story_run.StoryRun(self.stories[0])
    run.AddValue(scalar.ScalarValue(
        self.stories[0], 'a', 's', 1,
        improvement_direction=improvement_direction.UP))
    self.assertTrue(run.ok)
    self.assertFalse(run.failed)
    self.assertFalse(run.skipped)
    self.assertEquals(run.failure_str, None)
