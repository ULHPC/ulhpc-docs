# Job signals, job resubmission, and checkpoints

Larger jobs can often benefit from checkpoints. Checkpoints allow users to

- split a job into smaller jobs so that the smaller jobs can take advantage of [backfilling](/jobs/priority/#backfill-scheduling), and
- allows the use of the [`besteffort`](/jobs/best-effort/) QoS that is designed for jobs that can be interrupted.

A simple example on how to handle checkpoints on a Python script is provided. You can either modify the script or use an equivalent design on the system of your choice.

!!! tip "Using the `besteffort` queue with checkpoints"

    Currently the `besteffort` QoS is configured with zero [GraceTime](https://slurm.schedmd.com/preempt.html#config), the default value. This means that jobs are given no time when they are preempted to save their state in a checkpoint. Thus, the only way to use checkpoints with the `besteffort` QoS at the moment, is to

    - split your job into smaller jobs,
    - save the state of the smaller jobs regularly, and
    - requeue the smaller jobs until the computation finishes.

    Queueing a relatively small job ensures that not a lot of progress is lost if your job is preempted.

## Saving checkpoints in Python scripts

The `preemptable_job.py` is a Python script that initialized the process of saving a checkpoint when it receives the [signal](https://man7.org/linux/man-pages/man7/signal.7.html) `SIGUSR1`. Signals are an [interprocess communication](https://en.wikipedia.org/wiki/Signal_(IPC)) used in POSIX compliant systems. The script can catch the `SIGUSR1` signal, interrupt the main computation of the program, and write the program state into the disk (persistent storage). To use this script,

- add your algorithm in the try clause of the `work` function,
- save periodically you partial computation outcome to the `process_state` variable,
- define a method to save the `process_state` variable in the `save_checkpoint` function, and
- provide a method `load_checkpoint` to restore the `process_state` from persistent storage.

!!! info "`preemptable_job.py`"

    ```python
    import signal
    import time

    class SaveCheckpoint(SystemExit):
      def __init__(self, frame, signal, code=1):
        # Pass the exit code or message to the base SystemExit class
        super().__init__(code)
        self.frame = frame
        self.signal = signal
        self.code = code

      def log(self):
        print(f"Checkpoint triggered by signal ({self.signal}) with exit code: {self.code}")
        print(f"Interrupting at frame: {self.frame}")

    def load_checkpoint():
      return None # REPLACE WITH: code to rertore the process state from persisten storage

    def save_checkpoint(checkpoint_signal, process_state):
      checkpoint_signal.log()
      print("Saving state...")
      time.sleep(60) # REPLACE WITH: code to save the process state
      print("State saved.")

    def process_signal(sig, frame):
      print("Script recieved signal: ", sig)
      if sig == signal.SIGUSR1:
        raise SaveCheckpoint(frame, sig, code=1)
      else:
        raise SystemExit(f"Exiting due to signal '{sig}' in frame: {frame}")

    def work():
      print("Script started.")
      process_state = load_checkpoint()
      try:
        time.sleep(2*60*60) # REPLACE WITH: code to perform the required calculation
      except SaveCheckpoint as checkpoint_signal:
        save_checkpoint(checkpoint_signal, process_state)
        raise
      print("Script ended.")

    def main():
      signal.signal(signal.SIGTERM, process_signal)
      signal.signal(signal.SIGCONT, process_signal)
      signal.signal(signal.SIGUSR1, process_signal)
      work()

    if __name__ == "__main__":
      main()
    ```

??? info "Exception thrown by signal catching functions"

    Raise the [`SystemExit`](https://docs.python.org/3/library/exceptions.html#SystemExit) exception in Python scripts to exit when writing signal catchers. This exception is the exception raised by the `sys.exit()` function. A call to [`sys.exit()`](https://docs.python.org/3/library/sys.html#sys.exit) is translated into an exception so that clean-up handlers  (finally clauses of try statements) can be executed. The `SystemExit` exception inherits from [`BaseException`](https://docs.python.org/3/library/exceptions.html#BaseException) instead of [`Exception`](https://docs.python.org/3/library/exceptions.html#Exception) so that it is not accidentally caught by code that catches normal exceptions that derive the `Exception` class.

### Submission script that terminates a program gracefully with a checkpoint

The simplest method to use a program with checkpoint capabilities is to allow for graceful termination when the script times out. The following submission script uses the [`--signal`](https://slurm.schedmd.com/sbatch.html#OPT_signal) option of `sbatch`. This option has the format

```text
--signal=[B:]<signal>@<duration [s]>
```

where

- `<signal>` is the value of the signal,
- `<duration [s]>` is the delay between sending `<signal>` to the job and sending `SIGTERM` followed by `SIGKILL` (see the [`--time`](https://slurm.schedmd.com/sbatch.html#OPT_time) option), and
- `[B:]` is an optional parameter that determines whether the signal is sent to the batch shell when `[B:]` is present or the job steps otherwise (exclusive or).

The script for saving a single checkpoint is the following.

!!! info "`checkpoint_submission_script.sh`"

    ```bash
    #!/bin/bash --login
    #SBATCH --nodes=1
    #SBATCH --ntasks-per-node=1
    #SBATCH --ntasks-per-socket=1
    #SBATCH --cpus-per-task=16
    #SBATCH --time=00:5:00
    #SBATCH --partition=batch
    #SBATCH --qos=normal
    #SBATCH --signal=SIGUSR2@300 # Allow 5*60=200s=5min to save the checkpoint
    #SBATCH --job-name=preemptable_job
    #SBATCH --output=%x_%j.out
    #SBATCH --error=%x_%j.err

    module load lang/Python

    srun --ntasks=1 python -u preemptable_job.py
    ```

Saving a single check point is useful for preserving the progress of a job when it is difficult to a priori estimate the job duration, but to take advantage of the `besteffort` QoS, it best if the interrupted job is requeued automatically.

### Submission script to automatically requeue checkpointing programs

Slurm provided the [`--requeue`](https://slurm.schedmd.com/sbatch.html#OPT_requeue) option, that requeues a job if the job exists with non zero status. The job is requeued with the same job ID. This feature is used in the following submission script.

!!! info "`requeueing_submission_script.sh`"

    ```bash
    #!/bin/bash --login
    #SBATCH --nodes=1
    #SBATCH --ntasks-per-node=1
    #SBATCH --ntasks-per-socket=1
    #SBATCH --cpus-per-task=16
    #SBATCH --time=00:5:00
    #SBATCH --partition=batch
    #SBATCH --qos=normal
    #SBATCH --requeue # Resubmit until the jobs exits with a non-zero code (i.e. no checkpoint may be performed)
    #SBATCH --signal=SIGUSR1@300 # Allow 5*60=200s=5min to save the checkpoint
    #SBATCH --job-name=preemptable_job
    #SBATCH --output=%x_%j.out
    #SBATCH --error=%x_%j.err

    module load lang/Python

    srun --ntasks=1 python -u preemptable_job.py
    ```

The script utilizes the fact that any `srun` step where the checkpoint was triggered will exit with a non-zero exit code. The `--requeue` option ensures that the job will be dequeued until there is no checkpoint and the `srun` step will exit with a zero exit code.

### Submission script for complex manipulation during requeueing

Manipulation of script output or script side effect is some times required before requeuing a job. We examine the simple case where we stop resubmitting a script after it had accumulated some running time. This can be a means of preventing faulty scripts that exit persistently with a non-zero exit code frm being resubmitted indefinitely.

!!! info "`monitored_requeueing_submission_script.sh`"

    ```bash
    #!/bin/bash --login
    #SBATCH --nodes=1
    #SBATCH --ntasks-per-node=1
    #SBATCH --ntasks-per-socket=1
    #SBATCH --cpus-per-task=16
    #SBATCH --time=00:5:00
    #SBATCH --partition=batch
    #SBATCH --qos=normal
    #SBATCH --signal=B:SIGUSR2@300 # Send termination signal to batch script instead of job steps
    #SBATCH --requeue
    #SBATCH --job-name=preemptable_job
    #SBATCH --output=%x_%j.out
    #SBATCH --error=%x_%j.err

    declare max_duration=$((24*60*60)) # Run for up to a day of cumulative computation time

    sig_handler()
    {
      local pid="${1}"
      local sig="${2}"
      local elapsed_time_file='elapsed_time.txt'
      local timestamp_end=$(date +%s)

      echo " Termination signal received: ${sig}"
      echo " Signal trapped at - `date`"

      # End the simulation and save the data (needs to be less that 10min)
      kill -s "${sig}" "${pid}"

      declare start_time="0"
      if [ -f "${elapsed_time_file}" ]; then
        previously_elapsed_time=$(cat "${elapsed_time_file}")
      fi

      local iteration_elapsed_time=$((${timestamp_end}-${timestamp_start}))
      local elapsed_time=$((${previously_elapsed_time}+${iteration_elapsed_time}))

      wait "${pid}"
      echo " Termination signal handled at - `date`"

      if [ "${elapsed_time}" -ge "${max_duration}" ]; then
        exit 0
      else
        echo -n "${elapsed_time}" > "${elapsed_time_file}"
        # Exit with non-zero code to requeue
        exit 1
      fi
    }

    register_trap()
    {
      local func="${1}"
      local pid="${2}"
      local forward_sig="${3}"

      local sig=""
      for sig in "${@:4}"; do
        trap "${func} ${pid} ${forward_sig}" "${sig}"
      done
    }

    module load lang/Python

    declare timestamp_start=$(date +%s)
    srun --ntasks=1 python -u preemptable_job.py &
    declare STEP_PID=$!

    # associate the function `sig_handler_USR1` with the USR1 signal
    register_trap 'sig_handler' "${STEP_PID}" SIGUSR1 SIGUSR2

    wait "${STEP_PID}"
    ```

This script sends the termination signal to the batch script instead of the `srun` job steps. The batch scripts then forwards a signal to the jobs steps, waits for the jobs steps, and if the conditions are met terminates with a non-zero exit code so that the job is requeued.

??? warning "Avoid manual resubmission of job scripts"

    It can be tempting to requeue a job script by calling the `sbatch` command during the handling of the exception signal. For instance like the following code snippet.

    ```bash
    if [ "${elapsed_time}" -ge "${max_duration}" ]; then
      exit 0
    else
      # Exit with non-zero code to requeue
      sbatch [<options>] <script>
      exit 0
    fi
    ```

    However, in this case you are responsible for providing all the options to `sbatch` to resubmit your script correctly, including the

    - `<script>`, the path to the submission script, and
    - `[<options>]`, all the optional flags passed to `sbatch`.

    Also the resubmitted job will have a different job ID. You are better of using the `--requeue` option of Slurm that handles this details automatically.

## Sending signals to job scripts manually

When developing scripts that use the `--signal` option, it's quite convenient to test the signal handling manually. The `scancel` command is send a specific signal to the specified job or job step with the `--signal` option. The command

```bash
scancel --signal=<signal> [<job id>[_<array id>][.<step id>]] [...]
```

sends the `<signal>` to the specified job or a single job step within a job.
