from metadata import methods_defined_on

class TypeDict:

    def __init__(self):
        self._map = {}
    
    def put(self, name, signature):
        self._map[name] = signature

    def get(self, name):
        return self._map[name]

class Container:
    """Class with no implementation"""

ct = Container()
types = TypeDict()
while True:
    user_input = input("> ")
    if user_input == "a":
        fn_name = input("Method name> ")
        fn_type = input("Type signature> ")
        fn_impl = input("Lambda impl> ")
        exec(f'{fn_name} = {fn_impl}')
        ct.__setattr__(fn_name, locals()[fn_name])
        types.put(fn_name, fn_type)
        print(f"Defined method {fn_name} :: {fn_type}")
        continue
    elif user_input == "c" or user_input == "call":
        method_names = methods_defined_on(ct)
        if not method_names:
            print("There are currently no methods available to call")
            continue
        call_name = input("Method to call> ")
        signature = types.get(call_name)
        if not signature.startswith("unit"):
            arg = input("Argument> ")
            arg = eval(arg)
            result = ct.__getattribute__(call_name)(arg)
            if not signature.endswith("unit"):
                print(result)
            pass
        else:
            ct.__getattribute__(call_name)()
        continue
    elif user_input == "s":
        method_names = methods_defined_on(ct)
        if not method_names:
            print("There are currently no methods defined")
            continue
        for method_name in method_names:
            type_signature = types.get(method_name)
            print(f"{method_name} :: {type_signature}")
        continue
    elif user_input == "q":
        break
    else:
        print(f"Unrecognized command {user_input}")
        continue
