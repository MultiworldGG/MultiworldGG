from .Options import SM64HackOptions
from .Data import Data, star_like, sm64hack_items
from BaseClasses import CollectionState
import re

itemregex = r"(\|[^|]*\|)" #matches |anything|
macroregex = r"(\|@[^|]*\|)" #matches |@anything|
operand = r"[0-9]"

def evaluate_nested_macros(input: str, macro_dict: dict[str, str]) -> str:
    macros = re.findall(macroregex, input)
    for macro in macros:
        nested_macro_data = macro_dict[macro[2:-1]]
        evaluated_nested_macro = evaluate_nested_macros(nested_macro_data, macro_dict)
        input = input.replace(macro, f"({evaluated_nested_macro})")
    return input

def parse_requirement_string_to_postfix(string: str, macros: dict[str, str]) -> tuple[list[str], list[str]] | None:
    if string is None:
        return None
    if string == "" or string == []:
        return None
    
    string = evaluate_nested_macros(string, macros)
    requirements = re.findall(itemregex, string)
    for index, requirement in enumerate(requirements):
        string = string.replace(requirement, str(index), 1) #easier to keep track of numbers during later calculations
    
    string = re.sub(r" and ", "&", string, flags=re.IGNORECASE)
    string = re.sub(r" or ", "|", string, flags=re.IGNORECASE)
    string = string.replace("\n", "")
    string = string.replace(" ", "")

    stack = []
    result = []
    skip = []
    for index, character in enumerate(string): #converting infix to postfix
        if(index in skip):
            continue
        number = ""
        if(re.match(operand, character)):
            number += character
            while index + 1 < len(string) and re.match(operand, string[index + 1]):
                index += 1
                skip.append(index)
                number += string[index]
            result.append(number)
        elif character == '(':
            stack.append('(')
        elif character == ')':
            while stack[-1] != '(':
                result.append(stack.pop())
            stack.pop()
        else:
            while len(stack) > 0 and character == '|' and stack[len(stack) - 1] == '&':
                result.append(stack.pop())
            stack.append(character)
    while len(stack) > 0:
        result.append(stack.pop())

    return result, requirements

def evaluate_postfix_requirements(postfix: list[str], requirements: list[bool]) -> bool:
    stack = []
    for token in postfix:
        if token == '&': #would use match case if > 2 operators
            value1 = stack.pop()
            value2 = stack.pop()
            stack.append(value1 and value2)
        elif token == '|':
            value1 = stack.pop()
            value2 = stack.pop()
            stack.append(value1 or value2)
        else:
            stack.append(requirements[int(token)])
    return stack.pop()

def check_if_option_enabled(option:str, enabled_options: SM64HackOptions) -> bool:
    match option:
        case "reasonable":
            return enabled_options.logic_difficulty >= 1
        case "obscure":
            return enabled_options.logic_difficulty >= 2
        case "hard":
            return enabled_options.logic_difficulty >= 3
        case "Major Skips":
            return enabled_options.major_skips
        case _:
            return (option in enabled_options.glitches_in_logic and enabled_options.logic_difficulty != 0) or option in enabled_options.hack_specific_options

def check_if_location_exists(requirement_string: str, options: SM64HackOptions, macros: dict[str, str]) -> bool: #this does not check if you can access the zone. making locations not exist if the zone isnt accessible from options sounds too complicated to do, theres workarounds anyway
    result = parse_requirement_string_to_postfix(requirement_string, macros)
    if(result is None): #no requirements = always possible
        return True
    result, requirements = result #unpack tuple
    boolean_array = []
    for requirement in requirements:
        if requirement.startswith("|!"):
            boolean_array.append(check_if_option_enabled(requirement[2:-1], options))
        elif requirement.startswith("|?"):
            boolean_array.append(not check_if_option_enabled(requirement[2:-1], options))
        else:
            boolean_array.append(True) #for this step you assume you have all items and access to every level
    return evaluate_postfix_requirements(result, boolean_array)

def has_star_count(state: CollectionState, player: int, star_count: int) -> bool:
    return (state.count_from_list(star_like, player) + state.count("Star Bundle", player) * 2) >= star_count

def has_blue_star_count(state: CollectionState, player: int, star_count: int) -> bool:
    return (state.count("Blue Star", player) + state.count("Blue Star Bundle", player) * 2) >= star_count

def has_total_star_count(state: CollectionState, player: int, star_count: int) -> bool:
    return (state.count("Blue Star", player) + \
            state.count("Blue Star Bundle", player) * 2 + \
            state.count_from_list(star_like, player) + \
            state.count("Star Bundle", player) * 2) >= star_count


def check_requirement_string(state: CollectionState, 
                             player: int, 
                             requirement_string: str, 
                             options:SM64HackOptions, 
                             data: Data,
                             stardata: tuple[str, int] | None = None,
                             entrancedata: tuple[str, str] | None = None
                             ) -> bool:
    if entrancedata is not None and options.level_tickets:
        for level in entrancedata:
            if not state.has(f"{level} Ticket", player) and not data.locations[level].get("Overworld"):
                return False

    macros = data.locations["Other"]["Macros"]
    result = parse_requirement_string_to_postfix(requirement_string, macros)
    if result is None: #no requirements = always possible
        return True
    result, requirements = result #unpack tuple
    boolean_array = []
    for requirement in requirements:
        if requirement.startswith("|!"):
            boolean_array.append(check_if_option_enabled(requirement[2:-1], options))
        elif requirement.startswith("|?"):
            boolean_array.append(not check_if_option_enabled(requirement[2:-1], options))
        elif requirement.startswith("|#"):
            course, zone = requirement[2:-1].split(':')
            boolean_array.append(state.can_reach_region(f"{course} Zone {zone}", player))
        elif requirement.startswith("|Stars:"):
            star_count = int(requirement[7:-1])
            boolean_array.append(has_star_count(state, player, star_count))
        elif requirement.startswith("|BlueStars:"):
            star_count = int(requirement[11:-1])
            boolean_array.append(has_blue_star_count(state, player, star_count))
        elif requirement.startswith("|TotalStars:"):
            star_count = int(requirement[12:-1])
            boolean_array.append(has_total_star_count(state, player, star_count))
        else:
            item = requirement[1:-1]
            match item:
                case "Actspecific":
                    if stardata == None:
                        boolean_array.append(True) #avoid nesting stuff
                    else:
                        can_get_previous_acts = True
                        for i in range(stardata[1]):
                            can_get_previous_acts &= check_requirement_string(state, player, data.locations[stardata[0]]["Stars"][i]["Requirements"], options, data)
                        boolean_array.append(can_get_previous_acts)
                case "Key 1":
                    boolean_array.append(state.has("Key 1", player) or state.has("Progressive Key", player))
                case "Key 2":
                    boolean_array.append(state.has("Key 2", player) or state.has("Progressive Key", player, 2))
                case "Super Badge":
                    boolean_array.append(state.has("Progressive Stomp Badge", player))
                case "Ultra Badge":
                    boolean_array.append(state.has("Progressive Stomp Badge", player, 2))
                case "Jump":
                    if(options.move_randomization):
                        boolean_array.append(state.has("Progressive Jump", player, 1))
                    else:
                        boolean_array.append(True)
                case "Double Jump":
                    if(options.move_randomization):
                        boolean_array.append(state.has("Progressive Jump", player, 2))
                    else:
                        boolean_array.append(True)
                case "Triple Jump":
                    if(options.move_randomization):
                        boolean_array.append(state.has("Progressive Jump", player, 3))
                    else:
                        boolean_array.append(True)
                case _:
                    if item in sm64hack_items[76:86] and not options.move_randomization:
                        boolean_array.append(True)
                    else:
                        boolean_array.append(state.has(item, player))
    return evaluate_postfix_requirements(result, boolean_array)