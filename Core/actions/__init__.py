from Core.settings import GAS_LIST, RRG_LIST


def safe_check(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return f"Check error: {str(e)}"
    return wrapper


class Argument:
    arg_type = None
    arg_default = None
    arg_list = None

    @safe_check
    def check(self, value):
        pass


class FloatArgument(Argument):
    arg_type = float
    arg_default = 0.0

    @safe_check
    def check(self, value):
        value = float(value)


class GasListArgument(Argument):
    arg_type = list
    arg_list = GAS_LIST

    @safe_check
    def check(self, value):
        value = str(value).strip()
        if value not in self.arg_list:
            raise Exception(f"Gas {value} not in gas list")


class RrgListArgument(Argument):
    arg_type = list
    arg_list = RRG_LIST

    @safe_check
    def check(self, value):
        value = str(value).strip()
        if value not in self.arg_list:
            raise Exception(f"Rrg {value} not in rrg list")


class AppAction:
    args_info = []
    args_amount = 0

    def __init__(self, name, args_amount=None):
        self.name = name
        if args_amount is not None:
            self.args_amount = args_amount

    def check_args(self):
        return None


class RrgSelectAction(AppAction):
    args_info = [GasListArgument]
    args_amount = 1


class OpenValveAction(RrgSelectAction):
    pass


class CloseValveAction(RrgSelectAction):
    pass


ACTIONS = [
    AppAction("Pause"),
    OpenValveAction("Open valve"),
    CloseValveAction("Close valve"),
    AppAction("Act 1", args_amount=2),
    AppAction("Act 2", args_amount=3),
    AppAction("Act 3", args_amount=1),
    AppAction("Act 4", args_amount=1),
    AppAction("Act ХХХ", args_amount=1),
]


def get_action_by_name(name):
    for i, action in enumerate(ACTIONS):
        if action.name == name:
            return action, i
    return None, 0
