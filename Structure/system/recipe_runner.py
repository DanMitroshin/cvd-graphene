

class RecipeRunner:
    def __init__(self, get_work_status=None):
        self._recipe = None
        self._status = 0
        self.get_work_status = get_work_status

    def _get_work_status(self):
        try:
            self._status = self.get_work_status()
        except:
            pass


    def set_recipe(self, recipe):
        self._recipe = recipe

    def run_recipe(self):
        pass

    # def _run_recipe