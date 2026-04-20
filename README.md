# snakemake-lxplus-example
Snakemake hello world example on LXPLUS and lxbatch

## Setup

This is for LXPLUS 9 but it should be location independent.
However, as the LXPLUS home areas have limited storage, it is recommended that you run this example under your work (e.g. `/afs/cern.ch/work/f/feickert`) directory.

### Install `pixi`

[Install `pixi`](https://pixi.sh/latest/#installation)

```
curl -fsSL https://pixi.sh/install.sh | bash
```

and also [enable the shell autocompletion](https://pixi.sh/latest/#autocompletion)

```
echo 'eval "$(pixi completion --shell bash)"' >> ~/.bashrc
```

and then restart shell or

```
. ~/.bash_profile
```

### Run example

```
pixi run example
```

If you haven't installed the environment yet, `pixi` will run the equivalent of `pixi install` before executing your `pixi run` command.


### Trivial lxbatch example

Make sure you have a valid CERN Kerberos ticket (for example, `klist` should show a
current TGT), then run

```
pixi run lxbatch-example
```

This now uses the native `snakemake-executor-plugin-htcondor` executor with the
workflow profile in `workflow/profiles/lxbatch/profile.v9+.yaml`.

The local demo and the HTCondor demo now share one pixi environment. For local
tasks, the pixi task definition masks HTCondor configuration during Snakemake
startup so that the installed HTCondor executor plugin does not try to resolve a
CERN schedd when you are just running the local example.

The trivial shared-filesystem demonstrator has been verified to submit, run, and
complete successfully with the native `snakemake-executor-plugin-htcondor`.
That means the old cookiecutter profile machinery and `cluster-generic` submit/
status scripts are no longer needed for this example.

On lxplus, this demonstrator has also been verified to work without any
additional pre-submission Kerberos staging helper. In other words, for these
examples, the native executor is sufficient as-is.

This rule writes `local_hello.txt` in the workflow directory via a batch job.
To force a fresh submission, run

```
rm -f local_hello.txt
pixi run lxbatch-example --forcerun hello_lxbatch
```

### EOS example

To probe a more realistic CERN access pattern, there is also a rule that writes
directly to a configurable EOS directory.

Set `EOS_DIR` to the directory you want to write to, for example
`/eos/user/c/clange/snakemake-lxplus-example`, and then run

```
EOS_DIR=/eos/user/c/clange/snakemake-lxplus-example pixi run lxbatch-eos-example
```

The rule writes the file `hello_from_htcondor.txt` into that directory, and
Snakemake now tracks that EOS path itself as the rule output.

To force a fresh submission, run

```
EOS_DIR=/eos/user/c/clange/snakemake-lxplus-example pixi run lxbatch-eos-example --forcerun hello_eos
```

Afterwards, verify the written EOS file with

```
cat /eos/user/c/clange/snakemake-lxplus-example/hello_from_htcondor.txt
```

### EOS read example

There is also a companion rule that reads `hello_from_htcondor.txt` from the
configured EOS directory and copies it back into the workflow as
`results/read_from_eos.txt`.

```
EOS_DIR=/eos/user/c/clange/snakemake-lxplus-example pixi run lxbatch-eos-read-example
```

If `hello_from_htcondor.txt` is not present yet in `EOS_DIR`, Snakemake will
first run `hello_eos` to create it.

To force a fresh submission and overwrite the local result, run

```
rm -f results/read_from_eos.txt
EOS_DIR=/eos/user/c/clange/snakemake-lxplus-example pixi run lxbatch-eos-read-example --forcerun read_eos
```

Afterwards, verify the copied content with

```
cat results/read_from_eos.txt
```
