"""Scope: Reuse the verified installed Blender5.2.1 engine for the shared one-thread bake."""
from pathlib import Path
import argparse,hashlib,json,shutil,subprocess


class ExistingEnginePresentation:
    def run(self,source,output):
        package=Path.cwd()
        output.mkdir(exist_ok=False)
        config=dict(source=str(source),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
            unit_scale=.001,atlas_size=4096,threads=1,samples=16)
        (output/'job.json').write_text(json.dumps(config,indent=2)+'\n')
        worker=package/'aikea-review-unit/scripts/run_blender_bake.py'
        # The CLI owns its argv; adapt only that boundary to the unchanged shared
        # worker. Its real background/Cycles/glTF/version probe still runs.
        code=f'import sys,runpy;sys.path.insert(0,{str(worker.parent)!r});sys.argv=[{str(worker)!r},{str(output)!r}];runpy.run_path({str(worker)!r},run_name="__main__")'
        command=[shutil.which('blender'),'--background','--factory-startup','--threads','1',
                 '--python-exit-code','1','--python-expr',code]
        with (output/'bake.log').open('w') as log:
            subprocess.run(command,stdout=log,stderr=subprocess.STDOUT,check=True)
        print((output/'presentation.json').read_text())


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source',type=Path);parser.add_argument('output',type=Path)
    args=parser.parse_args()
    ExistingEnginePresentation().run(args.source.resolve(),args.output.resolve())
