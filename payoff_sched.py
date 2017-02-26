#!/usr/bin/env python3
import sys
from bisect import bisect_right


#Find index of rightmost finish time less than or equal to "start" using binary search. Return -1 if none exists
def find_last_compatible(finish_times, start):
    i = bisect_right(finish_times, start)
    if i:
      return i-1
    return -1
    

#For each job in the list, find the previous job with the highest compatible finish time (I.E. with a finish time lesser than or equal to the current job's start time)
def last_compatible_jobs(intervals):
  finish_times = [job[1] for job in intervals]
  last_compat_list = [find_last_compatible(finish_times, start) for start, _, _ in intervals]
  return last_compat_list


#Recursive function finds best sum of payoffs up to index. Used in brute force
def compute_optimal(intervals, last_compat_list, index):
  if index < 0 or last_compat_list[index] == -1:
    return intervals[index][2]
  return max(intervals[index][2] + compute_optimal(intervals, last_compat_list, last_compat_list[index]), compute_optimal(intervals, last_compat_list, index-1))
  
  
#Brute force for verification
def brute_force(intervals):
  last_compat_list = last_compatible_jobs(intervals)
  ans = compute_optimal(intervals, last_compat_list, len(intervals) - 1)
  return ans, []


#Computes the solution with dynamic programming. Use pre-computed last_compat_list to find subsolutions up to each index.
def dynamic_solution(intervals):
  last_compat_list = last_compatible_jobs(intervals)
  sub_solutions = [None] * (len(intervals) + 1)
  
  #Each index stores the best cost you can get up to that index.
  sub_solutions[0] = 0
  
  #This will store the path to the best solution
  best_intervals = []
  
  #Use previous subsolutions to find next subsolution.
  for index in range(0, len(intervals)):
    cost = intervals[index][2]
    last_compat_index = last_compat_list[index]
    last_cost = sub_solutions[last_compat_index + 1]
    sub_solutions[index + 1] = max(cost + last_cost, sub_solutions[index])
      
  #Find path to solution in reverse order
  index = len(intervals) - 1
  while index != -1:
    if intervals[index][2] + sub_solutions[last_compat_list[index] + 1] > sub_solutions[index]:
      best_intervals.append(intervals[index])
      index = last_compat_list[index]
    else:
      index -= 1
      
  #Order from first to last
  best_intervals.reverse()
    
  #Answer is stored at the end of the list
  return sub_solutions[-1], best_intervals
  
  
#Begin program
def main():
  intervals = []
  
  #Store jobs as tuples of size 3
  for line in sys.stdin:
    job = tuple(int(x) for x in line.strip().split())
    if len(job) != 3:
      continue
    intervals.append(job)
    
  #Sort by finish times. Both brute force and dynamic need this.
  intervals.sort(key = lambda job: job[1])

  #Compute the solution
  if len(sys.argv) > 1 and sys.argv[1] == "brute":
    print("Using brute force.")
    best_payoff, best_intervals = brute_force(intervals)
  else:
    best_payoff, best_intervals = dynamic_solution(intervals)
  
  #Print the results
  print("Maximum Payoff: %d" % best_payoff)
  for interval in best_intervals:
      print("%d %d %d" % interval)
    
    
if __name__ == "__main__":
    main()