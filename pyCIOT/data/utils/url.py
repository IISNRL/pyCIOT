from os import path


class URL:
    def __init__(self, base_url):
        self.base_url = base_url

        # TODO: Construct expansions and filters with a `Class` so that
        # it would be easier to be used. Now use string as workaround.
        self.expands = []
        self.filters = []

    def add_expand(self, prop):
        """
        Add expand into URL builder
        """
        self.expands.append(self._escape(prop))

    def add_filter(self, target: str, value: str, op: str):
        """
        Add a filter into URL builder

        Parameters:
        ----------
        target
            Search target
        value
            value to which value should match
        op
            eq, le, ge, lt, gt, substring

        """
        if op in {"eq", "le", "ge", "lt", "gt"}:
            self.filters.append(f"{target} {op} '{value}'")
        elif op == "substring":
            self.filters.append(f"substringof('{value}',{target})")
        else:
            raise Exception("Unsuppored operation")

    def get_datastream(self) -> str:
        return path.join(self.base_url, "Datastreams?") + self._escape("&".join(self._get_query()))

    def get_location(self) -> str:
        return path.join(self.base_url, "Locations?") + self._escape("&".join(self._get_query()))

    def _get_query(self):
        return filter(lambda x: x != None, [
            self._get_expand(), self._get_filter(), self._get_count()])

    def _get_expand(self):
        if len(self.expands):
            return f"$expand=" + ",".join(self.expands)
        else:
            return None

    def _get_filter(self):
        if len(self.filters):
            return f"$filter=" + "%20and%20".join(self.filters)
        else:
            return None

    def _get_count(self):
        return f"$count=true"

    def _escape(self, path):
        return path.replace("'", "%27").replace(" ", "%20")
