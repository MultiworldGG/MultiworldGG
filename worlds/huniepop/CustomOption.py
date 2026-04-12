import abc
import random
import math
import typing

from Options import NumericOption, Option, AssembleOptions


class DictRangeMeta(AssembleOptions):
    def __new__(mcs, name, bases, attrs):
        ret = super().__new__(mcs, name, bases, attrs)
        hello = {
            "single-random":"single-random",
            "single-random-low":"single-random-low",
            "single-random-high":"single-random-high",
            "random":"random",
            "random-low":"random-low",
            "random-high":"random-high",
        }
        if not (ret.range_min == 0 and ret.range_max==1):
            hello.update({
            f"single-random-range-{ret.range_min}-{ret.range_max}": f"single-random-range-{ret.range_min}-{ret.range_max}",
            f"single-random-range-low-{ret.range_min}-{ret.range_max}": f"single-random-range-low-{ret.range_min}-{ret.range_max}",
            f"single-random-range-high-{ret.range_min}-{ret.range_max}": f"single-random-range-high-{ret.range_min}-{ret.range_max}",
            f"random-range-{ret.range_min}-{ret.range_max}":f"random-range-{ret.range_min}-{ret.range_max}",
            f"random-range-low-{ret.range_min}-{ret.range_max}":f"random-range-low-{ret.range_min}-{ret.range_max}",
            f"random-range-high-{ret.range_min}-{ret.range_max}":f"random-range-high-{ret.range_min}-{ret.range_max}",
            })
        ret.options.update(hello)
        ret.name_lookup.update(hello)
        return ret


class DictRange(Option[str], abc.ABC, metaclass=DictRangeMeta):
    """when given a list of keys generates a dict of random values for it"""

    default = "single-1000"

    keys = []
    val = {}

    range_min = 0
    range_max = 1


    _OPTS = [
        "single-<value>",  #single value for all items
        "single-random", #single value for all items across full price range
        "single-random-low", #single value for all items across full price range weighted low
        "single-random-middle", #single value for all items across full price range weighted mid
        "single-random-high",  #single value for all items across full price range weighted high
        "single-random-range-<min>-<max>", #single value for all items across <min>-><max> price range
        "single-random-range-low-<min>-<max>", #single value for all items across <min>-><max> price range weighted low
        "single-random-range-middle-<min>-<max>", #single value for all items across <min>-><max> price range weighted med
        "single-random-range-high-<min>-<max>", #single value for all items across <min>-><max> price range weighted high

        "random", #random value for all items across full price range
        "random-low", #random value for all items across full price range weighted low
        "random-middle", #random value for all items across full price range weighted mid
        "random-high",  #random value for all items across full price range weighted high
        "random-range-<min>-<max>", #random value for all items across <min>-><max> price range
        "random-range-low-<min>-<max>", #random value for all items across <min>-><max> price range weighted low
        "random-range-middle-<min>-<max>", #random value for all items across <min>-><max> price range weighted med
        "random-range-high-<min>-<max>", #random value for all items across <min>-><max> price range weighted high
    ]

    def __init__(self, value: str, val=None):
        assert isinstance(val, dict), "val of RandomRange must be a dict"
        assert isinstance(value, str), "value of RandomRange must be a string"
        self.value = value
        self.val = val

    @property
    def current_key(self) -> str:
        return self.value

    @classmethod
    def from_text(cls, text: str) -> "DictRange":
        if text.startswith("single-"):
            if text == "single-random":
                i = random.randint(cls.range_min, cls.range_max)
                l = {}
                for k in cls.keys:
                    l[k] = i
                return cls(text, l)
            elif text == "single-random-low":
                i =cls.triangular(cls.range_min, cls.range_max, 0.0)
                l = {}
                for k in cls.keys:
                    l[k] = i
                return cls(text, l)
            elif text == "single-random-middle":
                i =cls.triangular(cls.range_min, cls.range_max)
                l = {}
                for k in cls.keys:
                    l[k] = i
                return cls(text, l)
            elif text == "single-random-high":
                i =cls.triangular(cls.range_min, cls.range_max, 1.0)
                l = {}
                for k in cls.keys:
                    l[k] = i
                return cls(text, l)
            elif text.startswith("single-random-range"):
                return cls.randomrange(text)
            else:
                textsplit = text.split("-")
                try:
                    i = int(textsplit[1])
                except ValueError:
                    raise ValueError(f"Invalid sub-value {textsplit[1]} in value {text} for option {cls.__name__}")
                if not cls.range_min < i < cls.range_max:
                    raise ValueError(f"Invalid sub-value {textsplit[1]} out of range {cls.range_min}-{cls.range_max} in value {text} for option {cls.__name__}")
                l = {}
                for k in cls.keys:
                    l[k] = i
                return cls(text, l)
        elif text.startswith("random-"):
            if text == "random-low":
                l = {}
                for k in cls.keys:
                    l[k] = cls.triangular(cls.range_min, cls.range_max, 0.0)
                return cls(text, l)
            elif text == "random-middle":
                l = {}
                for k in cls.keys:
                    l[k] = cls.triangular(cls.range_min, cls.range_max)
                return cls(text, l)
            elif text == "random-high":
                l = {}
                for k in cls.keys:
                    l[k] = cls.triangular(cls.range_min, cls.range_max, 1.0)
                return cls(text, l)
            elif text.startswith("random-range"):
                return cls.randomrange(text)
        elif text == "random":
            l = {}
            for k in cls.keys:
                l[k] = random.randint(cls.range_min, cls.range_max)
            return cls(text, l)

        else:
            raise Exception(f"Invalid option {text!r}. Acceptable options are: "
                            f"{', '.join(cls._OPTS)}.")


        return cls(text)

    @classmethod
    def from_any(cls, data: typing.Any) -> "DictRange":
        return cls.from_text(str(data))

    @classmethod
    def get_option_name(cls, value: str) -> str:
        return value

    @classmethod
    def randomrange(cls, text: str) -> "DictRange":
        textsplit = text.split("-")
        try:
            random_range = [int(textsplit[len(textsplit) - 2]), int(textsplit[len(textsplit) - 1])]
        except ValueError:
            raise ValueError(f"Invalid random range {text} for option {cls.__name__}")

        if not random_range[0] < random_range[1]:
            raise ValueError(f"Invalid sub-values {random_range[0]} not less than {random_range[1]} in value {text} for option {cls.__name__}")
        if not cls.range_min <= random_range[0] <= cls.range_max:
            raise ValueError(f"Invalid sub-value {random_range[0]} out of range {cls.range_min}-{cls.range_max} in value {text} for option {cls.__name__}")
        if not cls.range_min <= random_range[1] <= cls.range_max:
            raise ValueError(f"Invalid sub-value {random_range[1]} out of range {cls.range_min}-{cls.range_max} in value {text} for option {cls.__name__}")

        if text.startswith("single-random-range-low-"):
            i = cls.triangular(random_range[0], random_range[1], 0.0)
            l = {}
            for k in cls.keys:
                l[k] = i
            return cls(text, l)
        elif text.startswith("single-random-range-middle-"):
            i = cls.triangular(random_range[0], random_range[1])
            l = {}
            for k in cls.keys:
                l[k] = i
            return cls(text, l)
        elif text.startswith("single-random-range-high-"):
            i = cls.triangular(random_range[0], random_range[1], 1.0)
            l = {}
            for k in cls.keys:
                l[k] = i
            return cls(text, l)
        elif text.startswith("single-random-range-"):
            i = random.randint(random_range[0], random_range[1])
            l = {}
            for k in cls.keys:
                l[k] = i
            return cls(text, l)
        elif text.startswith("random-range-low-"):
            l = {}
            for k in cls.keys:
                l[k] = cls.triangular(random_range[0], random_range[1], 0.0)
            return cls(text, l)
        elif text.startswith("random-range-middle-"):
            l = {}
            for k in cls.keys:
                l[k] = cls.triangular(random_range[0], random_range[1])
            return cls(text, l)
        elif text.startswith("random-range-high-"):
            l = {}
            for k in cls.keys:
                l[k] = cls.triangular(random_range[0], random_range[1], 1.0)
            return cls(text, l)
        elif text.startswith("random-range-"):
            l = {}
            for k in cls.keys:
                l[k] = random.randint(random_range[0], random_range[1])
            return cls(text, l)
        else:
            raise Exception(f"text \"{text}\" did not resolve to a recognized pattern. "
                            f"Acceptable values are: {', '.join(cls._OPTS)}.")


    @staticmethod
    def triangular(lower: int, end: int, tri: float = 0.5) -> int:
        """
        Integer triangular distribution for `lower` inclusive to `end` inclusive.

        Expects `lower <= end` and `0.0 <= tri <= 1.0`. The result of other inputs is undefined.
        """
        # Use the continuous range [lower, end + 1) to produce an integer result in [lower, end].
        # random.triangular is actually [a, b] and not [a, b), so there is a very small chance of getting exactly b even
        # when a != b, so ensure the result is never more than `end`.
        return min(end, math.floor(random.triangular(0.0, 1.0, tri) * (end - lower + 1) + lower))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return other.value == self.value
        elif isinstance(other, str):
            return other == self.value
        else:
            raise TypeError(f"Can't compare {self.__class__.__name__} with {other.__class__.__name__}")
