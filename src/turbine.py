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
        """ This decorator is supposed to do the following: take the AST of f, and analyze it.
        Atomicity: Find all references to turbine function calls. Surround those with try-catch and
        make sure that once an exceptions raised, cancel-out all the previous calls. Big discussion on
        how this will ensure various guarantees such as serializability, etc. We now leave this open.

        Do "commit" only when all functions have executed.
        """
        f()

    return new_f

def endpoint(f):
    def new_f():
        """ This decorator is supposed to configure the gateway such that it registers the functions and creates input topics
        as well as public endpoints for those. Note that a turbine function wihtout an endpoint is considered a "private"
        function, i.e., it is not reachable from outside the system.
        """
        f()

    return new_f

class service:
    def discover(self, service_name):
        pass
