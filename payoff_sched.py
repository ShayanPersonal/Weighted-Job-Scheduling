#!/usr/bin/env python3
import sys
from bisect import bisect_right

#Find index of rightmost finish time less than or equal to "start" using binary search. Return 0 if none exists.
def find_last_compatible(finish_times, start):
    i = bisect_right(finish_times, start)
    if i:
        return i-1
    else:
      return 0

#For each job in the list, find the previous job with the highest compatible finish time (I.E. with a finish time lesser than or equal to the current job's start time)
def last_compatible_jobs(intervals):
  last_compat_list = [None] * len(intervals)
  finish_times = [job[1] for job in intervals]
  for i, job in enumerate(intervals):
    start = job[0]
    last_compat_list[i] = (find_last_compatible(finish_times, start))
  return last_compat_list
    
#Find best sum of payoffs up to index.
def compute_optimal(intervals, last_compat_list, index):
  print(index)
  if last_compat_list[index] == 0:
    return intervals[index][2]
  return max(intervals[index][2] + compute_optimal(intervals, last_compat_list, last_compat_list[index]), compute_optimal(intervals, last_compat_list, index-1))
  

def brute(intervals):
  last_compat_list = last_compatible_jobs(intervals)
  print(last_compat_list)
  ans = compute_optimal(intervals, last_compat_list, len(intervals) - 1)
  return ans, []
  
def dynamic(intervals):
  return 0, []


#Begin program
intervals = []

#Store jobs as tuples of size 3
for line in sys.stdin:
  job = tuple(int(x) for x in line.strip().split())
  if len(job) != 3:
    continue
  intervals.append(job)
  
#Sort by finish times. Both brute force and dynamic need this.
intervals.sort(key = lambda job: job[1])

#print(intervals)

#We can use brute force to verify our answers. Otherwise, use dynamic programming.
if len(sys.argv) > 1 and sys.argv[1] == "brute":
  print("Using brute force.")
  best_payoff, best_intervals = brute(intervals)
else:
  best_payoff, best_intervals = dynamic(intervals)

#Print the results
print("Maximum Payoff: %d" % best_payoff)
for interval in best_intervals:
    print(interval)