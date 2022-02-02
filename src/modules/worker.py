from PySide2.QtCore import QRunnable, QObject, Signal, Slot


class WorkerSignal(QObject):
    started = Signal(str)
    finished = Signal(str)
    error = Signal(str)


class FilterWorker(QRunnable):
    def __init__(self, func, started_emit_arg = "", finished_emit_arg = "", error_emit_arg = "",  *args, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.started_emit_arg = started_emit_arg
        self.finished_emit_arg = finished_emit_arg
        self.error_emit_arg = error_emit_arg
        self.signals = WorkerSignal()

    @Slot()
    def run(self):
        try:
            self.signals.started.emit(self.started_emit_arg)
            self.func(*self.args, **self.kwargs)
        except Exception as e:
            self.signals.error.emit(self.error_emit_arg + "\n" + str(e))
        else:
            self.signals.finished.emit(self.finished_emit_arg)
