import unittest
from unittest import mock

from tasktronaut.errors import NonRetryableProcessError
from .mocks import MockBackend, MockDefinition, MockJob


class BackendTestCase(unittest.TestCase):
    def setUp(self):
        self.backend = MockBackend()
        self.identifier = "foo"
        self.module_name = MockDefinition.__module__
        self.definition_class = MockDefinition.__qualname__

    @mock.patch.object(MockDefinition, "on_started")
    def test_perform_start(self, mock_on_started):
        self.backend.perform_start(
            identifier=self.identifier,
            module_name=self.module_name,
            definition_class=self.definition_class,
        )
        self.assertTrue(mock_on_started.called)

    @mock.patch.object(MockDefinition, "around_task")
    def test_perform_task_around_task(self, mock_around_task):
        self.backend.perform_task(
            job=MockJob(),
            identifier=self.identifier,
            module_name=self.module_name,
            definition_class=self.definition_class,
            function_name=MockDefinition.task_success.__name__,
            description="foo",
            kwargs={},
        )
        self.assertTrue(mock_around_task.called)

    @mock.patch.object(MockDefinition, "mock_hook")
    def test_perform_task_with_no_args(self, mock_hook):
        self.backend.perform_task(
            job=MockJob(),
            identifier=self.identifier,
            module_name=self.module_name,
            definition_class=self.definition_class,
            function_name=MockDefinition.task_with_no_args.__name__,
            description="foo",
            kwargs={},
        )
        self.assertTrue(mock_hook.called)

    @mock.patch.object(MockDefinition, "mock_hook")
    def test_perform_task_with_args(self, mock_hook):
        self.backend.perform_task(
            job=MockJob(),
            identifier=self.identifier,
            module_name=self.module_name,
            definition_class=self.definition_class,
            function_name=MockDefinition.task_with_args.__name__,
            description="foo",
            kwargs={},
        )
        self.assertTrue(mock_hook.called)

    @mock.patch.object(MockDefinition, "mock_hook")
    def test_perform_task_with_context(self, mock_hook):
        self.backend.perform_task(
            job=MockJob(),
            identifier=self.identifier,
            module_name=self.module_name,
            definition_class=self.definition_class,
            function_name=MockDefinition.task_with_context.__name__,
            description="foo",
            kwargs={},
        )
        self.assertTrue(mock_hook.called)

    @mock.patch.object(MockDefinition, "on_failed")
    def test_perform_task_on_failed(self, mock_on_failed):
        self.assertRaises(
            NotImplementedError,
            self.backend.perform_task,
            job=MockJob(),
            identifier=self.identifier,
            module_name=self.module_name,
            definition_class=self.definition_class,
            function_name=MockDefinition.task_fail.__name__,
            description="foo",
            kwargs={},
        )
        self.assertTrue(mock_on_failed.called)

    @mock.patch.object(MockDefinition, "on_failed")
    def test_perform_task_on_failed_no_retry(self, mock_on_failed):
        self.assertRaises(
            NonRetryableProcessError,
            self.backend.perform_task,
            job=MockJob(),
            identifier=self.identifier,
            module_name=self.module_name,
            definition_class=self.definition_class,
            function_name=MockDefinition.task_fail_no_retry.__name__,
            description="foo",
            kwargs={},
        )
        self.assertTrue(mock_on_failed.called)

    @mock.patch.object(MockDefinition, "on_cancelled")
    @mock.patch.object(MockJob, "cancel")
    @mock.patch.object(MockJob, "delete_dependents")
    def test_perform_task_on_cancelled(
        self,
        mock_job_delete_dependents,
        mock_job_cancel,
        mock_on_cancelled,
    ):
        self.backend.perform_task(
            job=MockJob(),
            identifier=self.identifier,
            module_name=self.module_name,
            definition_class=self.definition_class,
            function_name=MockDefinition.task_cancel.__name__,
            description="foo",
            kwargs={},
        )
        self.assertTrue(mock_job_delete_dependents.called)
        self.assertTrue(mock_job_cancel.called)
        self.assertTrue(mock_on_cancelled.called)

    @mock.patch.object(MockDefinition, "on_completed")
    def test_perform_complete(self, mock_on_completed):
        self.backend.perform_complete(
            identifier=self.identifier,
            module_name=self.module_name,
            definition_class=self.definition_class,
        )
        self.assertTrue(mock_on_completed.called)
