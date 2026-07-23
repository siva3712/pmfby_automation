import threading



class BackgroundWorker:

    def __init__(self):
        self.thread = None
        self.running = False
        self.cancelled = False

    def start(self, target, *args):

        if self.running:
            return

        self.running = True

        self.thread = threading.Thread(
            target=self.run,
            args=(target, *args),
            daemon=True
        )

        self.thread.start()

    def run(self, target, *args):

        try:
            target(*args)

        finally:
            self.running = False

    def is_running(self):
        return self.running
    
    ###################################################

    def cancel(self):

        self.cancelled = True

    ##################################################

    def is_cancelled(self):

        return self.cancelled

    ##################################################