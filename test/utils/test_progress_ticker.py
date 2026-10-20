import io
import unittest

from Utils import ProgressTicker


class TestProgressTicker(unittest.TestCase):
    def setUp(self) -> None:
        self.now = 0.0
        self.ticker = ProgressTicker(interval=2.0, clock=lambda: self.now)
        self.out = self.ticker.stream = io.StringIO()

    def run_passes(self, until: float, step: float = 0.5) -> list[float]:
        """Tick once per `step` seconds up to `until`; returns the times a glyph was written."""
        printed = []
        while self.now < until:
            self.now += step
            before = len(self.out.getvalue())
            self.ticker.tick()
            if len(self.out.getvalue()) > before:
                printed.append(self.now)
        return printed

    def test_silent_until_interval_elapses(self) -> None:
        self.assertEqual(self.run_passes(1.5), [])
        self.assertEqual(self.out.getvalue(), "")
        self.assertEqual(self.run_passes(2.0), [2.0])

    def test_at_most_one_glyph_per_interval(self) -> None:
        printed = self.run_passes(20.0, step=0.25)
        self.assertEqual(len(printed), 10)
        for earlier, later in zip(printed, printed[1:]):
            self.assertGreaterEqual(later - earlier, self.ticker.interval)

    def test_glyphs_alternate_one_per_print(self) -> None:
        self.run_passes(10.0)
        self.assertEqual(self.out.getvalue(), "△▲△▲△")

    def test_end_line_restarts_line_and_interval(self) -> None:
        self.run_passes(4.0)
        self.ticker.end_line()
        self.ticker.end_line()
        self.assertEqual(self.out.getvalue(), "△▲\n")
        self.assertEqual(self.run_passes(5.5), [])
        self.assertEqual(self.run_passes(6.0), [6.0])
        self.assertEqual(self.out.getvalue(), "△▲\n△")

    def test_end_line_without_glyphs_writes_nothing(self) -> None:
        self.ticker.end_line()
        self.assertEqual(self.out.getvalue(), "")

    def test_unusable_stream_does_not_raise(self) -> None:
        closed = io.StringIO()
        closed.close()
        streams = {"unset": None, "closed": closed, "ascii": io.TextIOWrapper(io.BytesIO(), encoding="ascii")}
        for name, stream in streams.items():
            with self.subTest(stream=name):
                self.ticker.stream = stream
                self.now += self.ticker.interval
                self.ticker.tick()
                self.ticker.end_line()
                self.assertEqual(self.ticker.line_length, 0)
