# example for MATLAB ParFor
parpool('local', str2num(getenv('SLURM_CPUS_PER_TASK'))) % set the default cores
%as number of threads
tic
n = 50;
A = 50;
a = zeros(1,n);
parfor i = 1:n
  a(i) = max(abs(eig(rand(A))));
end
toc
delete(gcp); % you have to delete the parallel region after the work is done
exit;
