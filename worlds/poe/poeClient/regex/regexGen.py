import random
import re
from collections import defaultdict, Counter
from typing import Set, List, Tuple, Optional, Dict
import itertools


class RegexBuilder:
    def __init__(self, max_length: int = 250):
        self.max_length = max_length

    def build_regex(self, all_names: Set[str], subset: Set[str]) -> str:
        """
        Generate a regex pattern that matches names in the subset.

        Args:
            all_names: The full set of names (assumed lowercase)
            subset: The subset of names to match (assumed lowercase)

        Returns:
            A regex string with max 250 characters
        """
        if not subset:
            return "$^"  # Matches nothing

        # Analyze the data first
        subset_list = sorted(list(subset))
        non_subset = all_names - subset

        # Try strategies in order of expected efficiency
        strategies = [
            self._discriminating_substring_strategy,
            self._ngram_position_strategy,
            self._wildcard_pattern_strategy,
            self._character_position_strategy,
            self._range_pattern_strategy,
            self._lookahead_strategy,
            self._compact_alternation_strategy,
            self._aggressive_prefix_suffix_strategy,
            self._hybrid_aggressive_strategy
        ]

        best_regex = None
        best_coverage = 0
        best_ratio = 0  # coverage / length ratio

        for strategy in strategies:
            try:
                regex = strategy(subset_list, non_subset, all_names)
                if regex and len(regex) <= self.max_length:
                    # Test coverage
                    pattern = re.compile(f"^{regex}$")
                    matched = [n for n in subset if pattern.match(n)]
                    false_positives = [n for n in non_subset if pattern.match(n)]

                    if not false_positives:  # No false positives
                        coverage = len(matched)
                        ratio = coverage / len(regex)

                        if coverage > best_coverage or (coverage == best_coverage and ratio > best_ratio):
                            best_regex = regex
                            best_coverage = coverage
                            best_ratio = ratio

                            if coverage == len(subset):
                                break
            except:
                continue

        # If no strategy worked perfectly, use combined approach
        if not best_regex or best_coverage < len(subset):
            best_regex = self._multi_strategy_combination(subset_list, non_subset, all_names)

        return best_regex or "$^"

    def _discriminating_substring_strategy(self, subset: List[str], non_subset: Set[str], all_names: Set[str]) -> str:
        """Find minimal substrings that uniquely identify subset members."""
        discriminators = []

        # For each name in subset, find shortest unique substring
        for name in subset:
            found = False
            # Try substrings of increasing length
            for length in range(2, min(len(name) + 1, 6)):
                for i in range(len(name) - length + 1):
                    substring = name[i:i + length]

                    # Check if this substring uniquely identifies names in our subset
                    matches_subset = [n for n in subset if substring in n]
                    matches_non_subset = [n for n in non_subset if substring in n]

                    if matches_subset and not matches_non_subset:
                        # This substring discriminates!
                        discriminators.append((substring, matches_subset))
                        found = True
                        break
                if found:
                    break

        # Sort by efficiency (names covered / pattern length)
        discriminators.sort(key=lambda x: len(x[1]) / (len(x[0]) + 4), reverse=True)  # +4 for .*substring.*

        # Build regex using best discriminators
        used_names = set()
        patterns = []
        total_length = 0

        for substring, names_covered in discriminators:
            new_names = [n for n in names_covered if n not in used_names]
            if new_names:
                # Determine if we need anchors
                needs_start = all(n.startswith(substring) for n in names_covered)
                needs_end = all(n.endswith(substring) for n in names_covered)

                if needs_start and needs_end:
                    pattern = re.escape(substring)
                elif needs_start:
                    pattern = re.escape(substring) + ".*"
                elif needs_end:
                    pattern = ".*" + re.escape(substring)
                else:
                    pattern = ".*" + re.escape(substring) + ".*"

                new_part = pattern if not patterns else "|" + pattern

                if total_length + len(new_part) <= self.max_length:
                    patterns.append(pattern)
                    used_names.update(new_names)
                    total_length += len(new_part)

        return "|".join(patterns) if patterns else ""

    def _ngram_position_strategy(self, subset: List[str], non_subset: Set[str], all_names: Set[str]) -> str:
        """Use n-gram patterns at specific positions."""
        # Analyze 2-gram and 3-gram patterns at different positions
        position_ngrams = defaultdict(lambda: defaultdict(list))

        for name in subset:
            # 2-grams
            for i in range(len(name) - 1):
                ngram = name[i:i + 2]
                position_ngrams[2][(i, ngram)].append(name)

            # 3-grams
            for i in range(len(name) - 2):
                ngram = name[i:i + 3]
                position_ngrams[3][(i, ngram)].append(name)

        # Find discriminating n-grams
        discriminating = []

        for n in [2, 3]:
            for (pos, ngram), names in position_ngrams[n].items():
                # Check if this n-gram at this position is unique to subset
                matches_non_subset = False
                for other in non_subset:
                    if pos < len(other) - n + 1 and other[pos:pos + n] == ngram:
                        matches_non_subset = True
                        break

                if not matches_non_subset and len(names) > 1:
                    discriminating.append((pos, ngram, names))

        # Build patterns
        patterns = []
        used_names = set()
        total_length = 0

        # Sort by efficiency
        discriminating.sort(key=lambda x: len(x[2]) / (x[0] + len(x[1]) + 2), reverse=True)

        for pos, ngram, names in discriminating:
            new_names = [n for n in names if n not in used_names]
            if new_names:
                # Build pattern with position
                if pos == 0:
                    pattern = re.escape(ngram) + ".*"
                else:
                    pattern = f".{{{pos}}}" + re.escape(ngram) + ".*"

                new_part = pattern if not patterns else "|" + pattern

                if total_length + len(new_part) <= self.max_length:
                    patterns.append(pattern)
                    used_names.update(new_names)
                    total_length += len(new_part)

        return "|".join(patterns) if patterns else ""

    def _wildcard_pattern_strategy(self, subset: List[str], non_subset: Set[str], all_names: Set[str]) -> str:
        """Use wildcards aggressively where safe."""
        # Group by length and find common patterns
        length_groups = defaultdict(list)
        for name in subset:
            length_groups[len(name)].append(name)

        patterns = []
        total_length = 0

        for length, names in sorted(length_groups.items(), key=lambda x: -len(x[1])):
            if len(names) < 2:
                continue

            # Find positions where we can use wildcards
            for positions_to_wildcard in range(1, length // 2):
                # Try different combinations of wildcard positions
                for wildcard_positions in itertools.combinations(range(length), positions_to_wildcard):
                    # Build pattern template
                    pattern_parts = []
                    test_patterns = []

                    for name in names:
                        parts = []
                        for i in range(length):
                            if i in wildcard_positions:
                                parts.append('.')
                            else:
                                parts.append(name[i])
                        test_patterns.append(''.join(parts))

                    # Check if all patterns are the same
                    if len(set(test_patterns)) == 1:
                        pattern = test_patterns[0]

                        # Verify no false positives
                        pattern_re = re.compile(f"^{pattern}$")
                        false_positives = any(pattern_re.match(n) for n in non_subset if len(n) == length)

                        if not false_positives:
                            new_part = pattern if not patterns else "|" + pattern

                            if total_length + len(new_part) <= self.max_length:
                                patterns.append(pattern)
                                total_length += len(new_part)
                                break

        return "|".join(patterns) if patterns else ""

    def _character_position_strategy(self, subset: List[str], non_subset: Set[str], all_names: Set[str]) -> str:
        """Build patterns based on character positions."""
        # Analyze character frequency at each position
        max_length = max(len(n) for n in subset) if subset else 0
        position_chars = [defaultdict(list) for _ in range(max_length)]

        for name in subset:
            for i, char in enumerate(name):
                position_chars[i][char].append(name)

        # Find discriminating character positions
        patterns = []
        used_names = set()
        total_length = 0

        # Look for positions where a small set of characters identifies subset
        for min_positions in range(2, 6):
            for positions in itertools.combinations(range(min(max_length, 10)), min_positions):
                # Group names by their characters at these positions
                signature_groups = defaultdict(list)

                for name in subset:
                    if all(pos < len(name) for pos in positions):
                        signature = tuple(name[pos] for pos in positions)
                        signature_groups[signature].append(name)

                # Check each signature group
                for signature, names in signature_groups.items():
                    if len(names) > 1 and all(n not in used_names for n in names):
                        # Build pattern
                        pattern_parts = []
                        last_pos = -1

                        for i, pos in enumerate(positions):
                            if pos == 0:
                                pattern_parts.append(signature[i])
                            else:
                                gap = pos - last_pos - 1
                                if gap == 0:
                                    pattern_parts.append(signature[i])
                                else:
                                    pattern_parts.append(f".{{{gap}}}{signature[i]}")
                            last_pos = pos

                        pattern = ''.join(pattern_parts) + ".*"

                        # Verify no false positives
                        pattern_re = re.compile(f"^{pattern}$")
                        if not any(pattern_re.match(n) for n in non_subset):
                            new_part = pattern if not patterns else "|" + pattern

                            if total_length + len(new_part) <= self.max_length:
                                patterns.append(pattern)
                                used_names.update(names)
                                total_length += len(new_part)

        return "|".join(patterns) if patterns else ""

    def _range_pattern_strategy(self, subset: List[str], non_subset: Set[str], all_names: Set[str]) -> str:
        """Use character ranges where possible."""
        patterns = []
        total_length = 0

        # Group by length and structure
        length_groups = defaultdict(list)
        for name in subset:
            length_groups[len(name)].append(name)

        for length, names in length_groups.items():
            if len(names) < 3:
                continue

            # Analyze each position
            position_ranges = []
            for pos in range(length):
                chars = sorted(set(name[pos] for name in names if pos < len(name)))

                # Check if chars form a contiguous range
                if chars and ord(chars[-1]) - ord(chars[0]) == len(chars) - 1:
                    position_ranges.append((pos, f"[{chars[0]}-{chars[-1]}]"))
                elif len(chars) <= 3:
                    position_ranges.append((pos, f"[{''.join(chars)}]"))
                else:
                    position_ranges.append((pos, None))

            # Build pattern if we have enough ranges
            range_count = sum(1 for _, r in position_ranges if r)
            if range_count >= length // 2:
                pattern_parts = []
                for pos, range_pattern in position_ranges:
                    if range_pattern:
                        pattern_parts.append(range_pattern)
                    else:
                        pattern_parts.append('.')

                pattern = ''.join(pattern_parts)

                # Verify no false positives
                pattern_re = re.compile(f"^{pattern}$")
                if not any(pattern_re.match(n) for n in non_subset if len(n) == length):
                    new_part = pattern if not patterns else "|" + pattern

                    if total_length + len(new_part) <= self.max_length:
                        patterns.append(pattern)
                        total_length += len(new_part)

        return "|".join(patterns) if patterns else ""

    def _lookahead_strategy(self, subset: List[str], non_subset: Set[str], all_names: Set[str]) -> str:
        """Use lookaheads for complex patterns."""
        # Find common patterns that require lookaheads
        patterns = []
        total_length = 0

        # Pattern: starts with X but not XY
        prefix_conflicts = defaultdict(lambda: {'subset': [], 'non_subset': []})

        for name in subset:
            for i in range(2, min(len(name), 5)):
                prefix = name[:i]
                prefix_conflicts[prefix]['subset'].append(name)

        for name in non_subset:
            for i in range(2, min(len(name), 5)):
                prefix = name[:i]
                if prefix in prefix_conflicts:
                    prefix_conflicts[prefix]['non_subset'].append(name)

        # Find prefixes where we can use negative lookahead
        for prefix, groups in prefix_conflicts.items():
            if groups['subset'] and groups['non_subset']:
                # Find what differentiates them
                subset_continuations = set()
                non_subset_continuations = set()

                for name in groups['subset']:
                    if len(name) > len(prefix):
                        subset_continuations.add(name[len(prefix)])

                for name in groups['non_subset']:
                    if len(name) > len(prefix):
                        non_subset_continuations.add(name[len(prefix)])

                # If there's a clear difference
                excluded = non_subset_continuations - subset_continuations
                if excluded and len(excluded) <= 3:
                    excluded_str = ''.join(sorted(excluded))
                    pattern = f"{re.escape(prefix)}(?![{excluded_str}]).*"

                    # Verify correctness
                    pattern_re = re.compile(f"^{pattern}$")
                    matches_subset = [n for n in groups['subset'] if pattern_re.match(n)]
                    matches_non_subset = [n for n in groups['non_subset'] if pattern_re.match(n)]

                    if matches_subset and not matches_non_subset:
                        new_part = pattern if not patterns else "|" + pattern

                        if total_length + len(new_part) <= self.max_length:
                            patterns.append(pattern)
                            total_length += len(new_part)

        return "|".join(patterns) if patterns else ""

    def _compact_alternation_strategy(self, subset: List[str], non_subset: Set[str], all_names: Set[str]) -> str:
        """Build compact alternations using factoring."""
        # Group by common prefixes and suffixes
        prefix_tree = defaultdict(list)
        suffix_tree = defaultdict(list)

        for name in subset:
            for i in range(1, min(len(name), 8)):
                prefix_tree[name[:i]].append(name[i:])
                suffix_tree[name[-i:]].append(name[:-i])

        patterns = []
        used_names = set()
        total_length = 0

        # Build prefix-based patterns
        for prefix, suffixes in sorted(prefix_tree.items(), key=lambda x: -len(x[1])):
            if len(suffixes) > 2:
                names = [prefix + s for s in suffixes]
                if all(n in subset and n not in used_names for n in names):
                    # Check if we can use a compact suffix pattern
                    suffix_pattern = self._build_compact_alternation(suffixes)

                    if suffix_pattern:
                        if suffixes == ['']:  # Just the prefix
                            pattern = re.escape(prefix)
                        else:
                            pattern = re.escape(prefix) + f"({suffix_pattern})"

                        # Verify no false positives
                        pattern_re = re.compile(f"^{pattern}$")
                        if not any(pattern_re.match(n) for n in non_subset):
                            new_part = pattern if not patterns else "|" + pattern

                            if total_length + len(new_part) <= self.max_length:
                                patterns.append(pattern)
                                used_names.update(names)
                                total_length += len(new_part)

        return "|".join(patterns) if patterns else ""

    def _aggressive_prefix_suffix_strategy(self, subset: List[str], non_subset: Set[str], all_names: Set[str]) -> str:
        """Aggressively use prefix/suffix patterns."""
        patterns = []
        used_names = set()
        total_length = 0

        # Try all prefix lengths
        for prefix_len in range(2, 8):
            prefix_groups = defaultdict(list)

            for name in subset:
                if name not in used_names and len(name) >= prefix_len:
                    prefix_groups[name[:prefix_len]].append(name)

            # Sort by group size
            for prefix, group in sorted(prefix_groups.items(), key=lambda x: -len(x[1])):
                if len(group) >= 2:
                    # Check if this prefix is safe
                    non_subset_matches = [n for n in non_subset if n.startswith(prefix)]

                    if not non_subset_matches:
                        # Safe to use prefix.*
                        pattern = re.escape(prefix) + ".*"
                        new_part = pattern if not patterns else "|" + pattern

                        if total_length + len(new_part) <= self.max_length:
                            patterns.append(pattern)
                            used_names.update(group)
                            total_length += len(new_part)
                    else:
                        # Need to be more specific
                        safe_suffixes = []
                        for name in group:
                            suffix = name[len(prefix):]
                            if not any(n.startswith(prefix + suffix) for n in non_subset_matches):
                                safe_suffixes.append(suffix)

                        if len(safe_suffixes) >= len(group) * 0.8:  # Most are safe
                            suffix_pattern = self._build_compact_alternation(safe_suffixes)
                            pattern = re.escape(prefix) + f"({suffix_pattern})"

                            new_part = pattern if not patterns else "|" + pattern

                            if total_length + len(new_part) <= self.max_length:
                                patterns.append(pattern)
                                used_names.update([prefix + s for s in safe_suffixes])
                                total_length += len(new_part)

        return "|".join(patterns) if patterns else ""

    def _hybrid_aggressive_strategy(self, subset: List[str], non_subset: Set[str], all_names: Set[str]) -> str:
        """Combine multiple aggressive strategies."""
        all_patterns = []
        used_names = set()

        # Collect patterns from different strategies with size limits
        strategies = [
            (self._discriminating_substring_strategy, 80),
            (self._ngram_position_strategy, 60),
            (self._aggressive_prefix_suffix_strategy, 60),
            (self._character_position_strategy, 50)
        ]

        for strategy, max_size in strategies:
            try:
                remaining = [n for n in subset if n not in used_names]
                if not remaining:
                    break

                # Get patterns from this strategy
                pattern = strategy(remaining, non_subset, all_names)

                if pattern and len(pattern) <= max_size:
                    # Extract individual patterns
                    parts = pattern.split('|')

                    for part in parts:
                        if len('|'.join(all_patterns + [part])) <= self.max_length:
                            all_patterns.append(part)

                            # Update used names
                            pattern_re = re.compile(f"^{part}$")
                            matched = [n for n in subset if pattern_re.match(n)]
                            used_names.update(matched)
            except:
                continue

        return '|'.join(all_patterns) if all_patterns else ""

    def _multi_strategy_combination(self, subset: List[str], non_subset: Set[str], all_names: Set[str]) -> str:
        """Final fallback combining best patterns from all strategies."""
        candidate_patterns = []

        # Collect all possible patterns with their coverage
        strategies = [
            self._discriminating_substring_strategy,
            self._ngram_position_strategy,
            self._wildcard_pattern_strategy,
            self._character_position_strategy,
            self._aggressive_prefix_suffix_strategy
        ]

        for strategy in strategies:
            try:
                pattern = strategy(subset, non_subset, all_names)
                if pattern:
                    # Break down into individual patterns
                    parts = pattern.split('|')

                    for part in parts:
                        pattern_re = re.compile(f"^{part}$")
                        matched = [n for n in subset if pattern_re.match(n)]
                        false_pos = [n for n in non_subset if pattern_re.match(n)]

                        if matched and not false_pos:
                            efficiency = len(matched) / len(part)
                            candidate_patterns.append((efficiency, part, set(matched)))
            except:
                continue

        # Greedy selection of best patterns
        candidate_patterns.sort(reverse=True, key=lambda x: x[0])

        selected_patterns = []
        covered_names = set()
        total_length = 0

        for efficiency, pattern, names in candidate_patterns:
            new_names = names - covered_names

            if new_names:
                new_part = pattern if not selected_patterns else "|" + pattern

                if total_length + len(new_part) <= self.max_length:
                    selected_patterns.append(pattern)
                    covered_names.update(new_names)
                    total_length += len(new_part)

        return '|'.join(selected_patterns) if selected_patterns else ""

    def _build_compact_alternation(self, alternatives: List[str]) -> str:
        """Build a compact alternation pattern."""
        if not alternatives:
            return ""

        if len(alternatives) == 1:
            return re.escape(alternatives[0])

        # Remove empty strings
        alternatives = [a for a in alternatives if a]

        if not alternatives:
            return ""

        # Try to find common patterns
        if len(set(len(a) for a in alternatives)) == 1:
            # All same length - try character classes
            length = len(alternatives[0])
            char_sets = [set() for _ in range(length)]

            for alt in alternatives:
                for i, char in enumerate(alt):
                    char_sets[i].add(char)

            # Build pattern with character classes
            parts = []
            for char_set in char_sets:
                if len(char_set) == 1:
                    parts.append(re.escape(list(char_set)[0]))
                elif len(char_set) <= len(alternatives) // 2:
                    chars = ''.join(sorted(char_set))
                    parts.append(f"[{chars}]")
                else:
                    # Too many variations, fall back to alternation
                    return '|'.join(re.escape(a) for a in alternatives)

            return ''.join(parts)

        # Different lengths - use standard alternation
        return '|'.join(re.escape(a) for a in alternatives)


def generate_subset_regex(all_names: Set[str], subset: Set[str], max_length: int = 250) -> str:
    """
    Generate a regex pattern that matches names in the subset.
    Assumes all names are lowercase.

    Args:
        all_names: The full set of names (lowercase)
        subset: The subset of names to match (lowercase)
        max_length: Maximum regex length (default: 250)

    Returns:
        A regex string that matches as many names in the subset as possible
    """
    # Ensure lowercase
    all_names = {n.lower() for n in all_names}
    subset = {n.lower() for n in subset}

    builder = RegexBuilder(max_length)
    return builder.build_regex(all_names, subset)


# Example usage and testing
if __name__ == "__main__":
    # Example with some test data
    all_names = {

        "Absolution",
        "Ancestral Cry",
        "Anger",
        "Animate Guardian",
        "Autoexertion",
        "Battlemage's Cry",
        "Berserk",
        "Bladestorm",
        "Blood and Sand",
        "Boneshatter",
        "Chain Hook",
        "Cleave",
        "Consecrated Path",
        "Corrupting Fever",
        "Crushing Fist",
        "Decoy Totem",
        "Defiance Banner",
        "Determination",
        "Devouring Totem",
        "Dominating Blow",
        "Dread Banner",
        "Earthquake",
        "Earthshatter",
        "Enduring Cry",
        "Eviscerate",
        "Exsanguinate",
        "Flame Link",
        "Flesh and Stone",
        "Frozen Legion",
        "General's Cry",
        "Glacial Hammer",
        "Ground Slam",
        "Heavy Strike",
        "Herald of Ash",
        "Herald of Purity",
        "Holy Flame Totem",
        "Ice Crash",
        "Immortal Call",
        "Infernal Blow",
        "Infernal Cry",
        "Intimidating Cry",
        "Leap Slam",
        "Molten Shell",
        "Molten Strike",
        "Perforate",
        "Petrified Blood",
        "Pride",
        "Protective Link",
        "Punishment",
        "Purity of Fire",
        "Rage Vortex",
        "Rallying Cry",
        "Reap",
        "Rejuvenation Totem",
        "Searing Bond",
        "Seismic Cry",
        "Shield Charge",
        "Shield Crush",
        "Shockwave Totem",
        "Smite",
        "Static Strike",
        "Steelskin",
        "Summon Flame Golem",
        "Summon Stone Golem",
        "Sunder",
        "Sweep",
        "Swordstorm",
        "Tectonic Slam",
        "Vengeful Cry",
        "Vigilant Strike",
        "Vitality",
        "Volcanic Fissure",
        "Vulnerability",
        "War Banner",
        "Warlord's Mark",

        "Alchemist's Mark",
        "Ambush",
        "Animate Weapon",
        "Arctic Armour",
        "Artillery Ballista",
        "Barrage",
        "Bear Trap",
        "Blade Blast",
        "Blade Flurry",
        "Blade Trap",
        "Blade Vortex",
        "Bladefall",
        "Blast Rain",
        "Blink Arrow",
        "Blood Rage",
        "Burning Arrow",
        "Caustic Arrow",
        "Charged Dash",
        "Cobra Lash",
        "Cremation",
        "Cyclone",
        "Dash",
        "Desecrate",
        "Detonate Dead",
        "Double Strike",
        "Dual Strike",
        "Elemental Hit",
        "Ensnaring Arrow",
        "Ethereal Knives",
        "Explosive Arrow",
        "Explosive Concoction",
        "Explosive Trap",
        "Fire Trap",
        "Flamethrower Trap",
        "Flicker Strike",
        "Frenzy",
        "Frost Blades",
        "Galvanic Arrow",
        "Glacial Shield Swipe",
        "Grace",
        "Haste",
        "Hatred",
        "Herald of Agony",
        "Herald of Ice",
        "Ice Shot",
        "Ice Trap",
        "Intuitive Link",
        "Lacerate",
        "Lancing Steel",
        "Lightning Arrow",
        "Lightning Strike",
        "Mirror Arrow",
        "Pestilent Strike",
        "Phase Run",
        "Plague Bearer",
        "Poacher's Mark",
        "Poisonous Concoction",
        "Precision",
        "Puncture",
        "Purity of Ice",
        "Rain of Arrows",
        "Reave",
        "Scourge Arrow",
        "Seismic Trap",
        "Shattering Steel",
        "Shrapnel Ballista",
        "Siege Ballista",
        "Smoke Mine",
        "Snipe",
        "Sniper's Mark",
        "Spectral Helix",
        "Spectral Shield Throw",
        "Spectral Throw",
        "Split Arrow",
        "Splitting Steel",
        "Storm Rain",
        "Summon Ice Golem",
        "Temporal Chains",
        "Temporal Rift",
        "Tornado",
        "Tornado Shot",
        "Toxic Rain",
        "Unearth",
        "Vampiric Link",
        "Venom Gyre",
        "Viper Strike",
        "Volatile Dead",
        "Whirling Blades",
        "Wild Strike",
        "Withering Step",

        "Arc",
        "Arcane Cloak",
        "Arcanist Brand",
        "Armageddon Brand",
        "Assassin's Mark",
        "Automation",
        "Ball Lightning",
        "Bane",
        "Blazing Salvo",
        "Blight",
        "Bodyswap",
        "Bone Offering",
        "Brand Recall",
        "Clarity",
        "Cold Snap",
        "Conductivity",
        "Contagion",
        "Conversion Trap",
        "Convocation",
        "Crackling Lance",
        "Creeping Frost",
        "Dark Pact",
        "Despair",
        "Destructive Link",
        "Discharge",
        "Discipline",
        "Divine Ire",
        "Divine Retribution",
        "Elemental Weakness",
        "Energy Blade",
        "Enfeeble",
        "Essence Drain",
        "Eye of Winter",
        "Fireball",
        "Firestorm",
        "Flame Dash",
        "Flame Surge",
        "Flame Wall",
        "Flameblast",
        "Flammability",
        "Flesh Offering",
        "Forbidden Rite",
        "Freezing Pulse",
        "Frost Bomb",
        "Frost Shield",
        "Frost Wall",
        "Frostbite",
        "Frostblink",
        "Frostbolt",
        "Galvanic Field",
        "Glacial Cascade",
        "Herald of Thunder",
        "Hexblast",
        "Hydrosphere",
        "Ice Nova",
        "Ice Spear",
        "Icicle Mine",
        "Incinerate",
        "Kinetic Blast",
        "Kinetic Bolt",
        "Lightning Conduit",
        "Lightning Spire Trap",
        "Lightning Tendrils",
        "Lightning Trap",
        "Lightning Warp",
        "Malevolence",
        "Manabond",
        "Orb of Storms",
        "Penance Brand",
        "Power Siphon",
        "Purifying Flame",
        "Purity of Elements",
        "Purity of Lightning",
        "Pyroclast Mine",
        "Raise Spectre",
        "Raise Zombie",
        "Righteous Fire",
        "Rolling Magma",
        "Scorching Ray",
        "Shock Nova",
        "Sigil of Power",
        "Siphoning Trap",
        "Soul Link",
        "Soulrend",
        "Spark",
        "Spellslinger",
        "Spirit Offering",
        "Storm Brand",
        "Storm Burst",
        "Storm Call",
        "Stormbind",
        "Stormblast Mine",
        "Summon Carrion Golem",
        "Summon Chaos Golem",
        "Summon Holy Relic",
        "Summon Lightning Golem",
        "Summon Raging Spirit",
        "Summon Reaper",
        "Summon Skeletons",
        "Summon Skitterbots",
        "Tempest Shield",
        "Void Sphere",
        "Voltaxic Burst",
        "Vortex",
        "Wave of Conviction",
        "Winter Orb",
        "Wintertide Brand",
        "Wither",
        "Wrath",
        "Zealotry",





        "Added Fire Damage Support",
        "Ancestral Call Support",
        "Arrogance Support",
        "Ballista Totem Support",
        "Behead Support",
        "Bloodlust Support",
        "Bloodthirst Support",
        "Brutality Support",
        "Burning Damage Support",
        "Cast on Melee Kill Support",
        "Cast when Damage Taken Support",
        "Chance to Bleed Support",
        "Cold to Fire Support",
        "Controlled Blaze Support",
        "Corrupting Cry Support",
        "Cruelty Support",
        "Damage on Full Life Support",
        "Elemental Damage with Attacks Support",
        "Empower Support",
        "Endurance Charge on Melee Stun Support",
        "Eternal Blessing Support",
        "Expert Retaliation Support",
        "Fire Penetration Support",
        "Fist of War Support",
        "Flamewood Support",
        "Fortify Support",
        "Generosity Support",
        "Guardian's Blessing Support",
        "Inspiration Support",
        "Iron Grip Support",
        "Iron Will Support",
        "Knockback Support",
        "Less Duration Support",
        "Life Gain on Hit Support",
        "Life Leech Support",
        "Lifetap Support",
        "Maim Support",
        "Melee Physical Damage Support",
        "Melee Splash Support",
        "More Duration Support",
        "Multiple Totems Support",
        "Multistrike Support",
        "Overexertion Support",
        "Pulverise Support",
        "Rage Support",
        "Ruthless Support",
        "Shockwave Support",
        "Spell Totem Support",
        "Stun Support",
        "Trauma Support",
        "Urgent Orders Support",
        "Volatility Support",
        "Added Cold Damage Support",
        "Additional Accuracy Support",
        "Advanced Traps Support",
        "Arrow Nova Support",
        "Barrage Support",
        "Blind Support",
        "Block Chance Reduction Support",
        "Cast On Critical Strike Support",
        "Cast on Death Support",
        "Chain Support",
        "Chance to Flee Support",
        "Chance to Poison Support",
        "Charged Traps Support",
        "Close Combat Support",
        "Cluster Traps Support",
        "Cold Penetration Support",
        "Critical Strike Affliction Support",
        "Culling Strike Support",
        "Deadly Ailments Support",
        "Enhance Support",
        "Faster Attacks Support",
        "Faster Projectiles Support",
        "Focused Ballista Support",
        "Fork Support",
        "Greater Multiple Projectiles Support",
        "Greater Volley Support",
        "Hypothermia Support",
        "Ice Bite Support",
        "Impale Support",
        "Multiple Projectiles Support",
        "Locus Mine Support",
        "Mana Leech Support",
        "Manaforged Arrows Support",
        "Mark On Hit Support",
        "Mirage Archer Support",
        "Momentum Support",
        "Multiple Traps Support",
        "Nightblade Support",
        "Pierce Support",
        "Point Blank Support",
        "Returning Projectiles Support",
        "Rupture Support",
        "Sadism Support",
        "Second Wind Support",
        "Slower Projectiles Support",
        "Swift Affliction Support",
        "Swift Assembly Support",
        "Trap and Mine Damage Support",
        "Trap Support",
        "Vicious Projectiles Support",
        "Vile Toxins Support",
        "Void Manipulation Support",
        "Volley Support",
        "Withering Touch Support",
        "Added Chaos Damage Support",
        "Added Lightning Damage Support",
        "Arcane Surge Support",
        "Archmage Support",
        "Blasphemy Support",
        "Blastchain Mine Support",
        "Bonechill Support",
        "Cast when Stunned Support",
        "Cast while Channelling Support",
        "Charged Mines Support",
        "Combustion Support",
        "Concentrated Effect Support",
        "Controlled Destruction Support",
        "Cursed Ground Support",
        "Decay Support",
        "Devour Support",
        "Efficacy Support",
        "Elemental Army Support",
        "Elemental Focus Support",
        "Elemental Penetration Support",
        "Elemental Proliferation Support",
        "Energy Leech Support",
        "Enlighten Support",
        "Faster Casting Support",
        "Feeding Frenzy Support",
        "Focused Channelling Support",
        "Fresh Meat Support",
        "Frigid Bond Support",
        "Hex Bloom Support",
        "Hextouch Support",
        "High-Impact Mine Support",
        "Ignite Proliferation Support",
        "Immolate Support",
        "Impending Doom Support",
        "Increased Area of Effect Support",
        "Increased Critical Damage Support",
        "Increased Critical Strikes Support",
        "Infernal Legion Support",
        "Infused Channelling Support",
        "Innervate Support",
        "Intensify Support",
        "Item Rarity Support",
        "Lightning Penetration Support",
        "Meat Shield Support",
        "Minefield Support",
        "Minion Damage Support",
        "Minion Life Support",
        "Minion Speed Support",
        "Overcharge Support",
        "Physical to Lightning Support",
        "Pinpoint Support",
        "Power Charge On Critical Support",
        "Predator Support",
        "Prismatic Burst Support",
        "Sacred Wisps Support",
        "Sacrifice Support",
        "Spell Cascade Support",
        "Spell Echo Support",
        "Spellblade Support",
        "Summon Phantasm Support",
        "Swiftbrand Support",
        "Trinity Support",
        "Unbound Ailments Support",
        "Unleash Support",
    }

    # Select a subset
    subset = set()

    for i in range(40):
        subset.add(random.choice(list(all_names)))

    # Generate regex
    all_names = {name.lower() for name in all_names}
    subset = {name.lower() for name in subset}
    regex = generate_subset_regex(all_names, subset)

    print(f"----------------------------------------------------------------------------------")
    print(f"----------------------------------------------------------------------------------")
    print(f"----------------------------------------------------------------------------------")

    print(f"Generated regex ({len(regex)} chars): {regex}")

    # Test the regex
    pattern = re.compile(f"^{regex}$")
    matched = [name for name in subset if pattern.match(name)]
    false_positives = [name for name in all_names - subset if pattern.match(name)]

    print(f"\nMatched {len(matched)}/{len(subset)} names from subset")
    print(f"False positives: {len(false_positives)}")

    if len(matched) < len(subset):
        missed = subset - set(matched)
        print(f"Missed names: {missed}")