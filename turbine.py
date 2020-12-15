class ManagedMap:
    def put(self, key, value):
        pass

    def get(self, key):
        pass

    def remove(self, key):
        pass


class ManagedList:
    def add(self, key, value):
        pass

    def remove(self, key):
        pass


def transactional(f):
    def new_f():
        print("Transactional")
        f()

    return new_f

def endpoint(f):
    def new_f():
        print("Endpoint")
        f()

    return new_f

class service:
    def discover(self, service_name):
        pass
