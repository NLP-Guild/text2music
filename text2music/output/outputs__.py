import requests

class BaseOutput:
    def __init__(self,*,output_path: str, mp3_url: str = None, mp3_file = None) -> None:
        super().__init__()
        if mp3_url is None and mp3_file is None:
            raise NotImplementedError("You must at least pass either the mp3_url or mp3_file.")
        if mp3_url is not None and mp3_file is not None:
            raise NotImplementedError("You can not pass mp3_url and mp3_file at the same time")

        self.mp3_url = mp3_url
        self.output_path = output_path
        self.mp3_file = mp3_file

    def write(self):
        if self.mp3_url is not None:
            r = requests.get(self.mp3_url, allow_redirects=True)
            open(self.output_path, 'wb').write(r.content)
        elif self.mp3_file is not None:
            raise NotImplementedError('TODO: add mp3 file') # TODO







