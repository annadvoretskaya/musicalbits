import dropbox


class Dropbox(object):
    # APP_KEY = '6exvd3wg5jxqryg'
    # APP_SECRET = '1ys2678xcq3y1os'
    ACCESS_TOKEN = 'Cr5oLQcbEcUAAAAAAAAAJLy6rZERx-LTNwzisjYIvOrEWoUj8f-mKKVyDcWtxzMp'
    UPLOAD_FOLDER = '/music/%s'

    def __init__(self):
        self.client = dropbox.client.DropboxClient(Dropbox.ACCESS_TOKEN)

    def upload(self, file):
        # response = None
        # with open(filename, 'rb') as file:
        path = self.client.put_file(Dropbox.UPLOAD_FOLDER % file.name, file)['path']
        context = self.client.media(path)
        context['path'] = path
        return context

    def get_abs_url(self, path):
        tmp = self.client.media(path)
        print tmp
        return tmp['url']
