"""Воркеры для фоновой обработки задач."""

from backend.infrastructure.workers.outbox_worker import OutboxWorker, run_outbox_worker

__all__ = ['OutboxWorker', 'run_outbox_worker']
