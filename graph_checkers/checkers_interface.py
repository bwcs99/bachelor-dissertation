import abc


class CheckerFormalInterface(metaclass=abc.ABCMeta):
    """
    Interfejs zawierający metody, które muszą być implementowane przez klasy sprawdzające, czy dany graf spełnia wymogi
    formalne stawiane przez algorytm.
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'check_graph_connectivity') and
                callable(subclass.check_graph_connectivity) and
                hasattr(subclass, 'check_if_graph_is_directed') and
                callable(subclass.check_if_graph_is_directed) and
                hasattr(subclass, 'check_if_graph_has_weights') and
                callable(subclass.check_if_graph_has_weights) and
                hasattr(subclass, 'check_if_weights_are_nonnegative') and
                callable(subclass.check_if_weights_are_nonnegative) or
                NotImplementedError)

    @abc.abstractmethod
    def check_if_graph_is_empty(self):
        raise NotImplementedError

    @abc.abstractmethod
    def check_graph_connectivity(self):
        raise NotImplementedError

    @abc.abstractmethod
    def check_if_graph_is_directed(self):
        raise NotImplementedError

    @abc.abstractmethod
    def check_if_graph_has_weights(self):
        raise NotImplementedError

    @abc.abstractmethod
    def check_if_weights_are_nonnegative(self):
        raise NotImplementedError
