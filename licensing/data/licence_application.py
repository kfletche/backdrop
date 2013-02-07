import collections

_LicenceApplication = collections.namedtuple('LicenceApplication', 'licence body interaction location')

class LicenceApplication(_LicenceApplication):
    @classmethod
    def from_google_row(cls, path, location):
        split_url = path.rsplit('/')
        
        return cls(split_url[2], split_url[3], split_url[4].partition('-')[0], location)


def from_google_data(data):
    for path, country, num_visits in data:
        for _ in range(int(num_visits)):
            yield LicenceApplication.from_google_row(path, country)