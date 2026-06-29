from dataclasses import dataclass

from Options import PerGameCommonOptions, Range, TextChoice

MAX_LEVEL = 500


class TargetScore(Range):
	"""Score needed to goal"""
	display_name = "Target Score"
	default = 100
	range_start = 50
	range_end = MAX_LEVEL


class DeathLink(TextChoice):
	"""When you die, everyone who enabled death link dies. Of course, the reverse is true too. If you enter a group name, you are only linked to the people in the same group.

	This can be adjusted later in the client, unless race mode is enabled."""

	display_name = "Death Link"
	default = 0
	option_false = 0
	option_true = 1

	@classmethod
	def get_option_name(cls, value):
		return value if isinstance(value, str) else ('Yes' if value else 'No')


@dataclass
class BallOptions(PerGameCommonOptions):
	target_score: TargetScore
	death_link: DeathLink
