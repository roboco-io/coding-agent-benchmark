import json
import tempfile
import unittest
from pathlib import Path
from aggregate_tokens import aggregate


def event(mid='a', **overrides):
    usage = dict(input_tokens=10, output_tokens=20,
                 cache_creation_input_tokens=30, cache_read_input_tokens=40)
    usage.update(overrides)
    return {'type': 'assistant', 'message': {'id': mid, 'usage': usage}}


class AggregationTests(unittest.TestCase):
    def run_logs(self, *files):
        with tempfile.TemporaryDirectory() as directory:
            for i, rows in enumerate(files):
                Path(directory, f'{i}.jsonl').write_text(
                    ''.join(json.dumps(row) + '\n' for row in rows))
            return aggregate(Path(directory))

    def test_duplicate_usage_is_counted_once_across_files(self):
        result = self.run_logs([event(), event()], [event(), event('b')])
        self.assertEqual(result['input_tokens'], 20)
        self.assertEqual(result['messages'], 2)
        self.assertEqual(result['duplicates'], 2)
        self.assertEqual(result['token_proxy'], 120)

    def test_conflicting_usage_is_not_guessed(self):
        with self.assertRaises(ValueError):
            self.run_logs([event(), event(output_tokens=21)])

    def test_missing_field_is_unknown_not_zero(self):
        row = event()
        del row['message']['usage']['cache_creation_input_tokens']
        result = self.run_logs([row])
        self.assertIsNone(result['cache_creation_input_tokens'])
        self.assertIsNone(result['token_proxy'])

    def test_explicit_zero_remains_zero(self):
        result = self.run_logs([event(input_tokens=0)])
        self.assertEqual(result['input_tokens'], 0)

    def test_missing_usage_is_visible(self):
        result = self.run_logs([{'type': 'assistant', 'message': {'id': 'a'}}])
        self.assertEqual(result['missing_usage'], 1)
        self.assertIsNone(result['token_proxy'])

    def test_missing_id_cannot_silently_double_count(self):
        row = event()
        del row['message']['id']
        with self.assertRaises(ValueError):
            self.run_logs([row])

    def test_cumulative_format_is_rejected(self):
        with self.assertRaises(ValueError):
            self.run_logs([{'type': 'event_msg', 'payload': {
                'type': 'token_count', 'info': {'total_token_usage': {'input_tokens': 20}}}}])

    def test_reasoning_already_in_output_is_not_added(self):
        result = self.run_logs([event(output_tokens_details={'reasoning_tokens': 15})])
        self.assertEqual(result['output_tokens'], 20)

    def test_invalid_json_is_not_silently_ignored(self):
        with tempfile.TemporaryDirectory() as directory:
            Path(directory, 'bad.jsonl').write_text('{invalid\n')
            with self.assertRaises(ValueError):
                aggregate(Path(directory))

    def test_empty_input_is_not_zero_usage(self):
        with self.assertRaises(ValueError):
            self.run_logs([])


if __name__ == '__main__':
    unittest.main()
