from scribe import Scribe
import threading
import queue

class ParScribe(Scribe):
    def __init__(self, language, **kwargs):
        super(ParScribe, self).__init__(language, **kwargs)
        self.queue = queue.Queue(maxsize=3)
        self._start_thread()

    def _start_thread(self):
        def _base_call_wrapper():
            self.queue.put(super(ParScribe, self).get_text_image())

        self.thread = threading.Thread(target=_base_call_wrapper, daemon=True)
        self.thread.start()

    def get_text_image(self, *args, **kwargs):
        self.thread.join()
        self._start_thread()
        return self.queue.get()