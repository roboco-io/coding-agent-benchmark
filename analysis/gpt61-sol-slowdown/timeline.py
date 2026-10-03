"""호환용 래퍼: 일반화된 analysis/latency/timeline.py(codex|pi|claude)를 그대로 실행한다."""
import runpy, os
runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'latency', 'timeline.py'), run_name='__main__')
