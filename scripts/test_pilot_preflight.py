import unittest
from pilot_preflight import inspect_claude, schedule


class PilotPreflightTests(unittest.TestCase):
    def test_success_exit_does_not_hide_model_fallback(self):
        events=[{'type':'system','subtype':'init','model':'fable'},
                {'type':'assistant','message':{'model':'other','content':[{'type':'text','text':'OK'}]}},
                {'type':'result','is_error':False,'modelUsage':{'fable':{},'other':{}}}]
        result=inspect_claude(events,'fable')
        self.assertFalse(result['eligible'])
        self.assertIn('model_mismatch',result['reasons'])

    def test_usage_missing_does_not_pass(self):
        result=inspect_claude([{'type':'system','subtype':'init','model':'fable'}],'fable')
        self.assertFalse(result['eligible'])

    def test_provider_fallback_event_blocks_even_if_usage_looks_clean(self):
        events=[{'type':'system','subtype':'model_fallback'},
                {'type':'result','is_error':False,'modelUsage':{'fable':{}}}]
        self.assertFalse(inspect_claude(events,'fable')['eligible'])

    def test_matching_model_and_complete_usage_can_pass(self):
        events=[{'type':'result','is_error':False,'usage':{'input_tokens':1,'output_tokens':1},
                 'modelUsage':{'fable':{'inputTokens':1,'outputTokens':1}}}]
        self.assertTrue(inspect_claude(events,'fable')['eligible'])

    def test_overage_blocks_subscription_only_run(self):
        events=[{'type':'rate_limit_event','rate_limit_info':{'isUsingOverage':True}},
                {'type':'result','is_error':False,'usage':{'input_tokens':1,'output_tokens':1},
                 'modelUsage':{'fable':{'inputTokens':1,'outputTokens':1}}}]
        self.assertIn('subscription_overage',inspect_claude(events,'fable')['reasons'])

    def test_incomplete_or_invalid_usage_blocks(self):
        for invalid in ({}, {'input_tokens': None}, {'input_tokens': 1},
                        {'input_tokens': True, 'output_tokens': 1},
                        {'input_tokens': 1, 'output_tokens': -1}):
            with self.subTest(usage=invalid):
                events=[{'type':'result','is_error':False,'usage':invalid,
                         'modelUsage':{'fable':{'inputTokens':1,'outputTokens':1}}}]
                self.assertFalse(inspect_claude(events,'fable')['eligible'])

    def test_incomplete_model_usage_blocks(self):
        events=[{'type':'result','is_error':False,
                 'usage':{'input_tokens':1,'output_tokens':1},'modelUsage':{'fable':{}}}]
        self.assertFalse(inspect_claude(events,'fable')['eligible'])

    def test_explicit_zero_usage_is_complete(self):
        events=[{'type':'result','is_error':False,
                 'usage':{'input_tokens':0,'output_tokens':0},
                 'modelUsage':{'fable':{'inputTokens':0,'outputTokens':0}}}]
        self.assertTrue(inspect_claude(events,'fable')['eligible'])

    def test_schedule_is_balanced_and_reproducible(self):
        runs=schedule(['build','bug','feature','migration'],['fable','astra'],3,20260921)
        self.assertEqual(runs,schedule(['build','bug','feature','migration'],['fable','astra'],3,20260921))
        self.assertEqual(len(runs),24)
        self.assertEqual(len({r['run_id'] for r in runs}),24)
        pairs=[runs[i:i+2] for i in range(0,24,2)]
        self.assertEqual(sum(p[0]['condition']=='fable' for p in pairs),6)
        for pair in pairs:
            self.assertEqual(pair[0]['task'],pair[1]['task'])
            self.assertNotEqual(pair[0]['condition'],pair[1]['condition'])

if __name__=='__main__':
    unittest.main()
