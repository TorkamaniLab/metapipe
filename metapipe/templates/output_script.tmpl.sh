#! {{shell}}
set -e;

{{options}}

python - <<END
import pickle

with open('{{temp}}', 'rb') as f:
    runtime = pickle.load(f)
    runtime.run()
END
