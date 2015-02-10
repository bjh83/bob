import __builtin__

class Rule:
  def __init__(self):
    pass

  def __str__(self):
    fields = set(dir(self)) - set(dir(Rule()))
    string = self.__class__.__name__ + '('
    for field in fields:
      string = string + field + ' = ' + str(getattr(self, field)) + ', '
    string = string + ')'
    return string

  def __repr__(self):
    return str(self)

class Executor:
  def __init__(self):
    self._rules = {}
    self._results = []
    self._CreateRules()

  # Override this to return the appropriate rules.
  def rule_constructors(self):
    pass

  def Execute(self, file_name):
    self._results = []
    self._ExecuteFile(file_name)
    return self._results

  def _CreateRules(self):
    for constructor in self.rule_constructors():
      func = self._CreateRule(constructor)
      self._rules[constructor.__name__] = func

  def _CreateRule(self, constructor):
    field_names = set(dir(constructor())) - set(dir(Rule()))
    def func(**kwargs):
      rule = constructor()
      for name, value in kwargs.items():
        if name in field_names:
          setattr(rule, name, value)
        else:
          raise AttributeError(constructor.__name__ + " has no attribute '" + name + "'")
      self._results.append(rule)
    return func

  def __enter__(self):
    for name, function in self._rules.items():
      setattr(__builtin__, name, function)

  def __exit__(self, type, value, traceback):
    for name in self._rules.keys():
      delattr(__builtin__, name)

  def _ExecuteFile(self, file_name):
    with self:
      execfile(file_name)
